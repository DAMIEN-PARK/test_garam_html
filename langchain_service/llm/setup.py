from langchain_openai import ChatOpenAI
import core.config as config


# 현재는 OpenAI 모델만 지원하도록 고정한다.
def get_llm(provider="openai", model=None, api_key: str = None, temperature: float = 0.7):
    if provider != "openai":
        raise ValueError("현재는 OpenAI 제공자만 지원합니다.")

    model_name = model or config.DEFAULT_CHAT_MODEL
    return ChatOpenAI(
        api_key=api_key,
        model_name=model_name,
        temperature=temperature,
    )


def get_backend_agent(provider="openai", model=None):
    if provider != "openai":
        raise ValueError("현재는 OpenAI 제공자만 지원합니다.")

    model_name = model or config.DEFAULT_CHAT_MODEL
    return ChatOpenAI(
        openai_api_key=config.EMBEDDING_API,
        model_name=model_name,
        temperature=0.7,
    )

