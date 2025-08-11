import os
from typing import Optional, Dict, Any
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
MODEL = os.getenv("HINT_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")

SYSTEM_PROMPT = (
    "You are a friendly DSA tutor for beginners. "
    "Give progressive hints only. "
    "Levels: 1=nudge, 2=approach idea, 3=step-by-step outline, 4=pseudocode. "
    "Avoid giving full code unless the user explicitly requests a solution."
)

_client: Optional[InferenceClient] = None

def _client_or_error():
    global _client
    if HF_API_TOKEN is None:
        raise RuntimeError("Missing HF_API_TOKEN. Add it to your .env")
    if _client is None:
        _client = InferenceClient(api_key=HF_API_TOKEN)
    return _client

def make_prompt(problem: Dict[str, Any], user_attempt: str, level: int) -> str:
    title = problem.get("title", "Unknown")
    patterns = ", ".join(problem.get("patterns", []))
    signature = problem.get("signature", "")
    samples = problem.get("samples", [])
    sample = samples[0] if samples else {}
    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"Problem: {title}\n"
        f"Patterns: {patterns}\n"
        f"Signature: {signature}\n"
        f"Sample input: {sample.get('input')}\n"
        f"Current attempt (may be empty):\n{user_attempt or '[no attempt]'}\n\n"
        f"Provide Hint Level {level} now. Keep it concise and beginner-friendly."
    )

def generate_hint(problem: Dict[str, Any], user_attempt: str, level: int = 1) -> str:
    if level not in (1,2,3,4):
        level = 1
    try:
        client = _client_or_error()
        prompt = make_prompt(problem, user_attempt, level)
        resp = client.text_generation(
            prompt,
            model=MODEL,
            max_new_tokens=220,
            temperature=0.3,
            top_p=0.9,
        )
        return resp.strip()
    except Exception as e:
        return f"⚠️ Could not generate hint: {e}"
