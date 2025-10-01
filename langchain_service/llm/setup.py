from __future__ import annotations

from functools import lru_cache
from typing import Iterable, Optional

from langchain_openai import ChatOpenAI

import core.config as config


def _parse_openai_models(raw_models: str) -> tuple[str, ...]:
    models: Iterable[str] = (m.strip() for m in raw_models.split(","))
    return tuple(sorted({m for m in models if m}))


@lru_cache(maxsize=1)
def _openai_model_catalog() -> tuple[str, ...]:
    return _parse_openai_models(config.OPENAI_MODELS or "") or (config.DEFAULT_CHAT_MODEL,)


def _default_openai_model() -> str:
    candidates = _openai_model_catalog()
    preferred = config.DEFAULT_CHAT_MODEL.strip()
    if preferred and preferred in candidates:
        return preferred
    return candidates[0]


def ensure_openai_model(model: Optional[str]) -> str:
    """Return a valid OpenAI 모델 이름."""

    if model:
        normalized = model.strip()
        if normalized:
            catalog = _openai_model_catalog()
            if normalized in catalog:
                return normalized
    return _default_openai_model()


def ensure_openai_provider(_: Optional[str]) -> str:
    """현재 단계에서는 OpenAI 제공자만 허용한다."""

    return "openai"


def llm_kwargs_for_model(
    *,
    fast_response_mode: bool,
    model_name: Optional[str] = None,
    provider_name: Optional[str] = None,
) -> dict:
    """AI 모델 설정에서 사용할 LLM 파라미터를 반환한다."""

    kwargs: dict = {
        "provider": ensure_openai_provider(provider_name),
        "model": ensure_openai_model(model_name),
        "temperature": 0.2 if fast_response_mode else 0.3,
    }
    if fast_response_mode:
        kwargs["max_tokens"] = 512
    return kwargs


def get_llm(
    provider: str = "openai",
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    temperature: float = 0.7,
    **kwargs,
):
    """지정된 사양에 맞는 OpenAI LLM 인스턴스를 생성한다."""

    ensure_openai_provider(provider)
    model_name = ensure_openai_model(model)
    final_api_key = api_key or config.OPENAI_API or config.DEFAULT_API_KEY

    return ChatOpenAI(
        api_key=final_api_key,
        model_name=model_name,
        temperature=temperature,
        **kwargs,
    )

