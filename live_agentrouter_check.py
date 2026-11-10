#!/usr/bin/env python3
"""Live Connectivity Test for AgentRouter.org (supports both /v1/responses and /v1/chat/completions)."""

import os
import sys
from dotenv import load_dotenv
from openai import OpenAI, APIStatusError, APIConnectionError


def main() -> int:
    load_dotenv(override=True)
    api_key = (os.getenv("AGENTROUTER_API_KEY") or os.getenv("OPENAI_API_KEY") or "").strip()
    base_url = os.getenv("AGENTROUTER_BASE_URL", "https://agentrouter.org/v1").strip()
    model = os.getenv("AI_MODEL", "gpt-5.6-sol").strip()

    if not api_key or "your-agentrouter-api-key" in api_key:
        print("[ERROR] Please set your real AGENTROUTER_API_KEY in `.env`.")
        return 1

    print(f"Connecting to {base_url} with model '{model}' (Key: {api_key[:6]}...{api_key[-4:]})...")

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
        default_headers={
            "User-Agent": "RooCode/3.34.8",
            "HTTP-Referer": "https://github.com/RooVetGit/Roo-Cline",
            "X-Title": "Roo Code",
        },
    )

    try:
        # Try the modern OpenAI Responses API (/v1/responses) first (required by gpt-5.6-sol)
        resp = client.responses.create(
            model=model,
            instructions="You are the aicheck0 verification assistant.",
            input="Reply with 'AgentRouter connection verified!'",
        )
        output_text = getattr(resp, "output_text", None) or str(resp)
        print("Response:", output_text)
        return 0
    except APIStatusError as exc:
        # If a different model only supports /v1/chat/completions, fallback automatically
        if exc.status_code in (400, 404):
            try:
                chat_resp = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are the aicheck0 verification assistant."},
                        {"role": "user", "content": "Reply with 'AgentRouter connection verified!'"},
                    ],
                    max_tokens=32,
                )
                print("Response:", chat_resp.choices[0].message.content)
                return 0
            except APIStatusError as chat_exc:
                print(f"\n[HTTP {chat_exc.status_code}] Server responded with: {chat_exc.message}")
                return 1
        print(f"\n[HTTP {exc.status_code}] Server responded with: {exc.message}")
        return 1
    except APIConnectionError as exc:
        print(f"\n[CONNECTION ERROR] Could not reach {base_url}: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
