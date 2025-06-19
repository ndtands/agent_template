import os
from typing import Union

from dotenv import dotenv_values, load_dotenv
from langchain_openai.chat_models import AzureChatOpenAI

if os.path.exists(".env"):
    load_dotenv()
    config = dotenv_values(".env")


class ChatGPT4oMiniModel:
    azure_endpoint: Union[str, None]
    api_key: Union[str, None]
    api_version: Union[str, None]
    azure_deployment: Union[str, None]
    timeout: Union[float, None]

    def __init__(self) -> None:
        self.azure_endpoint = config.get(
            "SEARCH-AGENT-AZURE-OPENAI-GPT4O-MINI-ENDPOINT"
        )
        self.api_key = config.get("SEARCH-AGENT-AZURE-OPENAI-GPT4O-MINI-API-KEY")
        self.api_version = config.get(
            "SEARCH-AGENT-AZURE-OPENAI-GPT4O-MINI-API-VERSION",
            "2024-08-01-preview",
        )
        # self.api_version = "2024-08-01-preview"
        self.azure_deployment = config.get(
            "SEARCH-AGENT-AZURE-OPENAI-GPT4O-MINI-DEPLOYMENT-NAME"
        )
        self.timeout = float(config.get("TIMEOUT", 60 * 5))


LLM = {
    "basic": AzureChatOpenAI(
        **ChatGPT4oMiniModel().__dict__,
        temperature=0,
        model="gpt-4o-mini",
    ),
    "vision": None,
}
