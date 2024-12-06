from abc import ABC, ABCMeta
from typing import Union, Any
from langchain_openai.chat_models.azure import AzureChatOpenAI

from app.config import app_settings
from app.business_logic.llm_client.base import BaseLLM

class AzureOpenAILLM(BaseLLM, metaclass=ABCMeta):
    def __init__(self, **kwargs: Any) -> None:
        # LLM Secrets
        self.__key: str = app_settings.openai_settings.key
        self.__endpoint: str = app_settings.openai_settings.endpoint
        self.__model_deployment_name: str = app_settings.openai_settings.model
        self.__temperature: float = app_settings.openai_settings.temperature if app_settings.openai_settings.temperature else 0.0
        self.__top_p: float = app_settings.openai_settings.top_p if app_settings.openai_settings.top_p else 0.0
        self.__max_token: int = app_settings.openai_settings.max_tokens if app_settings.openai_settings.max_tokens else 1000
        self.__api_version: str = app_settings.openai_settings.preview_api_version
        self.llm_client: AzureChatOpenAI = None

    def _llm_client(self) -> None:
        # Construct parameters for initializing the AzureChatOpenAI model
        azure_model_parm = {
            "openai_api_type": "azure",
            "openai_api_version": self.__api_version,
            "azure_endpoint": self.__endpoint,
            "openai_api_key": self.__key,
            "deployment_name": self.__model_deployment_name,
            "temperature": self.__temperature,
            "max_tokens": self.__max_token,
            "model_kwargs": {
                "top_p": self.__top_p,
                "frequency_penalty": 0,
                "presence_penalty": 0,
                "stop": None
            }
        }
        self.llm_client = AzureChatOpenAI(**azure_model_parm)

    def create(self) -> AzureChatOpenAI:
        self._llm_client()
        return self.llm_client