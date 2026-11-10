#!/usr/bin/env python3
"""Live Connectivity Test for AgentRouter.org API Key."""

import os
import sys
from dotenv import load_dotenv
from openai import OpenAI


def main() -> int:
    load_dotenv()
    api_key = os.getenv("AGENTROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("AGENTROUTER_BASE_URL", "https://api.agentrouter.org/v1")
    model = os.getenv("AI_MODEL", "deepseek-chat")

    if not api_key or "your-agentrouter-api-key" in api_key:
        print("[ERROR] Please copy `.env.example` to `.env` and set your AGENTROUTER_API_KEY.")
        return 1

    print(f"Connecting to {base_url} with model '{model}'...")
    client = OpenAI(api_key=api_key, base_url=base_url)
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are the aicheck0 verification assistant."},
            {"role": "user", "content": "Reply with 'AgentRouter connection verified!'"},
        ],
        max_tokens=32,
    )
    print("Response:", resp.choices[0].message.content)
    return 0


if __name__ == "__main__":
    sys.exit(main())
