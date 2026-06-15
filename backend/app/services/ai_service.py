"""AI service abstraction layer.

Wraps AI provider calls behind a clean interface so that:
1. Provider-specific logic lives in one place (not duplicated per route).
2. Switching providers requires changing only this module.
3. Error handling and retries are centralized.
"""

from typing import Any

import httpx
from openai import AsyncOpenAI

from app.core.config import settings
from app.core.exceptions import AIServiceError

_client: AsyncOpenAI | None = None


def _get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        _client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            http_client=httpx.AsyncClient(timeout=60.0),
        )
    return _client


async def generate_analysis(
    prompt: str,
    context: str = "",
    temperature: float = 0.2,
) -> str:
    """Send an analysis prompt to the AI model and return the response text."""
    client = _get_client()
    messages: list[dict[str, Any]] = []
    if context:
        messages.append({"role": "system", "content": context})
    messages.append({"role": "user", "content": prompt})

    try:
        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=messages,
            temperature=temperature,
        )
        content = response.choices[0].message.content
        return content or ""
    except Exception as e:
        raise AIServiceError(f"AI request failed: {e}") from e


async def generate_sql(
    question: str,
    schema_description: str,
) -> str:
    """Generate a SQL query from a natural-language question."""
    prompt = (
        f"Given this database schema:\n{schema_description}\n\n"
        f"Write a SQL query to answer: {question}\n"
        "Return ONLY the SQL query, no explanation."
    )
    return await generate_analysis(prompt, context="You are a SQL expert.")


async def summarize_data(
    data_sample: str,
    question: str = "Provide a brief summary of this data.",
) -> str:
    """Summarize a data sample using AI."""
    prompt = f"Data sample:\n{data_sample}\n\nQuestion: {question}"
    return await generate_analysis(
        prompt, context="You are a data analyst. Be concise."
    )
