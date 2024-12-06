from typing import Any
from abc import ABCMeta
from langchain_core.prompts import PromptTemplate
from langchain_openai.chat_models import AzureChatOpenAI
from langchain.runnables.openai_functions import Runnable
from langchain.chains.combine_documents import create_stuff_documents_chain

from app.business_logic.llm_chain.base import BaseLLMChain
from app.business_logic.llm_client import AzureOpenAILLM
from app.business_logic.prompt_templates import QNA_PROMPT_TEMPLATE


class ContextQNAChain(BaseLLMChain, metaclass=ABCMeta):
    def __init__(self, **kwargs: Any) -> None:
        self.__qna_prompt_template: PromptTemplate = QNA_PROMPT_TEMPLATE
        self.__llm_client: AzureChatOpenAI = AzureOpenAILLM().create()
        self.__llm_chain_object: Runnable = None
        
    def _llm_chain(self):
        self.__llm_chain_object = self.__qna_prompt_template | self.__llm_client
    
    def create(self) -> Runnable:
        self._llm_chain()
        return self.__llm_chain_object