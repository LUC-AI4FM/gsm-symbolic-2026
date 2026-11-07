"""Inference routes. Each returns (text, stop_reason, usage dict, model_version or None).

- bedrock: Amazon Bedrock Converse through the AWS CLI. In our setup the CLI is wrapped by an
  audited proxy; set GSMSYM_AWS_CMD (default "aws") to the command prefix you use.
- alcf: the ALCF inference service (OpenAI-compatible chat completions). The bearer token comes
  from the ALCF helper named by GSMSYM_ALCF_TOKEN_CMD and is kept in memory only.
No credential, header or account identifier is ever written to the logs.
"""
import json
import random
import re
import os
import shlex
import subprocess
import threading
import time
import urllib.error
import urllib.request

AWS_CMD = shlex.split(os.environ.get("GSMSYM_AWS_CMD", "aws"))
REGION = os.environ.get("GSMSYM_AWS_REGION", "us-east-1")


class RouteError(RuntimeError):
    pass


TRANSIENT = ("Throttling", "ServiceUnavailable", "Bad Gateway", "502", "503", "504", "timed out",
             "ModelNotReady", "Connection reset")


def _aws(cmd):
    """Run an AWS CLI call; retry transient failures; return stdout. Errors keep only the AWS message."""
    for attempt in range(10):
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        except subprocess.TimeoutExpired:
            continue
        if r.returncode == 0:
            return r.stdout
        err = (r.stderr or r.stdout)[-600:]
        if any(t in err for t in TRANSIENT):
            time.sleep(min(90, 3 * 2 ** attempt) * (0.5 + random.random()))
            continue
        m = re.search(r"\((\w+Exception)\)[^:]*:\s*([^\n]*)", err)
        raise RouteError(f"{m.group(1)}: {m.group(2)[:240]}" if m else "AWS call failed (details suppressed)")
    raise RouteError("transient failures: retries exhausted")


def bedrock(model_id, prompt, *, max_tokens, temperature=0.0, stop=("\nQ:",)):
    msgs = [{"role": "user", "content": [{"text": prompt}]}]
    cfg = {"maxTokens": max_tokens}
    if temperature is not None:
        cfg["temperature"] = temperature
    if stop:
        cfg["stopSequences"] = list(stop)
    cmd = AWS_CMD + ["bedrock-runtime", "converse", "--region", REGION, "--model-id", model_id,
                     "--messages", json.dumps(msgs), "--inference-config", json.dumps(cfg), "--output", "json"]
    d = json.loads(_aws(cmd))
    content = d["output"]["message"]["content"]
    text = "".join(c.get("text", "") for c in content)
    reasoning = sum(1 for c in content if "reasoningContent" in c)
    u = d.get("usage", {})
    return text, d.get("stopReason"), {"input": u.get("inputTokens"), "output": u.get("outputTokens"),
                                        "reasoning_blocks": reasoning}, None


def bedrock_completion(model_id, prompt, *, max_tokens, temperature=0.0, stop=None):
    """Raw text completion (no chat template) for Meta Llama models, as in the paper's open-model setup."""
    body = {"prompt": prompt, "max_gen_len": max_tokens, "temperature": temperature}
    cmd = AWS_CMD + ["bedrock-runtime", "invoke-model", "--region", REGION, "--model-id", model_id,
                     "--cli-binary-format", "raw-in-base64-out", "--body", json.dumps(body), "/dev/stdout"]
    d, _ = json.JSONDecoder().raw_decode(_aws(cmd).lstrip())
    return d["generation"], d.get("stop_reason"), {"input": d.get("prompt_token_count"),
                                                   "output": d.get("generation_token_count")}, None


class _AlcfToken:
    def __init__(self):
        self._lock, self._tok, self._at = threading.Lock(), None, 0.0

    def get(self, refresh=False):
        with self._lock:
            if refresh or self._tok is None or time.time() - self._at > 1800:
                cmd = os.environ.get("GSMSYM_ALCF_TOKEN_CMD")
                if not cmd:
                    raise RouteError("set GSMSYM_ALCF_TOKEN_CMD to the ALCF access-token helper")
                r = subprocess.run(shlex.split(cmd), capture_output=True, text=True, timeout=120)
                tok = r.stdout.strip()
                if r.returncode or not tok or any(c.isspace() for c in tok):
                    raise RouteError("ALCF token helper failed (output suppressed)")
                self._tok, self._at = tok, time.time()
            return self._tok


_TOKEN = _AlcfToken()
ALCF = "https://inference-api.alcf.anl.gov/resource_server/{cluster}/v1/chat/completions"


def alcf(model_id, prompt, *, cluster, max_tokens, temperature=0.0, stop=("\nQ:",), seed=42, completion=False):
    """Chat completions, or with completion=True raw text completion (/v1/completions, no chat template)."""
    if completion:
        body = {"model": model_id, "prompt": prompt, "max_tokens": max_tokens, "temperature": temperature, "seed": seed}
    else:
        body = {"model": model_id, "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens, "temperature": temperature, "seed": seed}
    if stop:
        body["stop"] = list(stop)
    data = json.dumps(body).encode()
    refreshed = False
    for attempt in range(8):
        url = ALCF.format(cluster=cluster)
        if completion:
            url = url.replace("/chat/completions", "/completions")
        req = urllib.request.Request(url, data=data, method="POST",
                                     headers={"Content-Type": "application/json",
                                              "Authorization": "Bearer " + _TOKEN.get()})
        try:
            with urllib.request.urlopen(req, timeout=900) as resp:
                d = json.loads(resp.read())
            ch = d["choices"][0]
            u = d.get("usage") or {}
            text = ch.get("text", "") if completion else (ch["message"].get("content") or "")
            return (text, ch.get("finish_reason"),
                    {"input": u.get("prompt_tokens"), "output": u.get("completion_tokens")}, d.get("model"))
        except urllib.error.HTTPError as e:
            if e.code == 401 and not refreshed:
                _TOKEN.get(refresh=True)
                refreshed = True
                continue
            if e.code in (408, 429, 500, 502, 503, 504):
                time.sleep(min(120, 5 * 2 ** attempt))
                continue
            raise RouteError(f"ALCF HTTP {e.code}") from None
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            time.sleep(min(120, 5 * 2 ** attempt))
    raise RouteError("ALCF retries exhausted")
