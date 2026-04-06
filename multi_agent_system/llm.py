import os
import time
from google import genai

MODELS = [
    "gemini-2.0-flash-001",
    "gemini-2.5-flash",
    "gemini-2.0-flash-lite-001",
]

def ask_llm(system_prompt: str, user_message: str) -> str:
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return "ERROR: GEMINI_API_KEY not set"

    client = genai.Client(api_key=api_key)
    full_prompt = f"{system_prompt}\n\nUser: {user_message}\nAssistant:"
    print(f"\n🔵 SENDING TO LLM: {user_message}")

    for model in MODELS:
        try:
            print(f"🔄 Trying model: {model}")
            response = client.models.generate_content(
                model=model,
                contents=full_prompt
            )
            print(f"🟢 SUCCESS with {model}")
            return response.text.strip()
        except Exception as e:
            err = str(e)
            if "429" in err or "RESOURCE_EXHAUSTED" in err:
                print(f"⚠️ Quota exhausted for {model}, trying next...")
                time.sleep(2)
                continue
            elif "404" in err or "not found" in err.lower():
                print(f"⚠️ Model {model} not available, trying next...")
                continue
            else:
                print(f"🔴 Error with {model}: {err[:80]}")
                continue

    return "⏳ All models are currently at quota limit. Please wait a few minutes and try again."
