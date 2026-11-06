"""Model registry. Prices are Amazon Bedrock us-east-1 on-demand list prices (USD per 1M tokens,
regional "us." profile where applicable) read from the AWS Price List API on 2026-11-06.
ALCF and Claude Code subagent routes cost no cash."""

MODELS = {
    # --- anchor: a model the paper evaluated -------------------------------------------------
    "llama3-8b-instruct": dict(route="bedrock_completion", id="meta.llama3-8b-instruct-v1:0",
                               released="2024-04", price=(0.30, 0.60), max_tokens=512),
    # --- 2026 models reachable on Bedrock -----------------------------------------------------
    "deepseek-v3.2": dict(route="bedrock", id="deepseek.v3.2", released="2026-02", price=(0.62, 1.85), max_tokens=2048),
    "glm-5": dict(route="bedrock", id="zai.glm-5", released="2026-03", price=(1.00, 3.20), max_tokens=2048),
    "nemotron-super-3-120b": dict(route="bedrock", id="nvidia.nemotron-super-3-120b", released="2026-03",
                                  price=(0.15, 0.65), max_tokens=2048),
    "minimax-m2.5": dict(route="bedrock", id="minimax.minimax-m2.5", released="2026-03", price=(0.30, 1.20),
                         max_tokens=4096, reasoning=True),
    "kimi-k3.1": dict(route="bedrock", id="us.moonshotai.kimi-k3.1", released="2026-11", price=(3.30, 16.50),
                      max_tokens=8192, temperature=None, reasoning=True),
    "kimi-k3": dict(route="bedrock", id="us.moonshotai.kimi-k3", released="2026-08", price=(3.30, 16.50),
                    max_tokens=8192, temperature=None, reasoning=True),
    "mistral-large-3": dict(route="bedrock", id="mistral.mistral-large-3-675b-instruct", released="2025-12",
                            price=(0.50, 1.50), max_tokens=2048),
    "nova-2-lite": dict(route="bedrock", id="us.amazon.nova-2-lite-v1:0", released="2025-12", price=(0.33, 2.75),
                        max_tokens=2048),
    # --- ALCF (no cash cost) -------------------------------------------------------------------
    "gemma-4-31b-it": dict(route="alcf", cluster="sophia/vllm", id="google/gemma-4-31B-it", released="2026", price=(0, 0),
                           max_tokens=2048),
    "gpt-oss-120b": dict(route="alcf", cluster="sophia/vllm", id="openai/gpt-oss-120b", released="2025-08", price=(0, 0),
                         max_tokens=8192, reasoning=True),
    "mistral-large-4": dict(route="alcf", cluster="tara/api", id="mistral-large-4", released="2026", price=(0, 0),
                            max_tokens=2048),
    "nemotron-3-ultra": dict(route="alcf", cluster="tara/api", id="nemotron-3-ultra", released="2026", price=(0, 0),
                             max_tokens=4096),
    "llama-3.1-8b-instruct": dict(route="alcf", cluster="sophia/vllm", id="meta-llama/Meta-Llama-3.1-8B-Instruct",
                                  released="2024-07", price=(0, 0), max_tokens=1024),
}


def cost(model, usage):
    pin, pout = MODELS[model]["price"]
    return ((usage.get("input") or 0) * pin + (usage.get("output") or 0) * pout) / 1e6
