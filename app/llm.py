import httpx

from config import settings
from app.prompts import SYSTEM_PROMPT


class LLMClient:
    async def complete(self, prompt: str) -> str:
        if not settings.llm_api_key or not settings.llm_model:
            return "LLM is not configured. Add LLM_API_KEY and LLM_MODEL to the environment."

        url = settings.llm_base_url.rstrip("/") + "/chat/completions"

        headers = {
            "Authorization": f"Bearer {settings.llm_api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": settings.llm_model,
            "messages": [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        }

        async with httpx.AsyncClient(timeout=90) as client:
            response = await client.post(
                url,
                headers=headers,
                json=payload,
            )

            response.raise_for_status()

            data = response.json()

            return data["choices"][0]["message"]["content"]
