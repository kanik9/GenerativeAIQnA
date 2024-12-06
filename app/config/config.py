import os
from typing_extensions import Self
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import (
    BaseModel,
    confloat,
    conint,
    conlist,
    Field,
    field_validator,
    model_validator,
    PrivateAttr,
    ValidationError,
    ValidationInfo
)
from typing import Optional

# Global Constants
DOTENV_PATH = os.environ.get("DOTENV_PATH", os.path.join(os.path.dirname(os.path.dirname(__name__)), ".env"))

MINIMUM_SUPPORTED_AZURE_OPENAI_PREVIEW_API_VERSION = "2024-05-01-preview"

# Important Constants securly reading from .env file
class _AzureOpenAISettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="AZURE_OPENAI_",
        env_file=DOTENV_PATH,
        extra="ignore",
        env_ignore_empty=True
    )
    model: str

    key: Optional[str] = None
    resource: Optional[str] = None
    endpoint: Optional[str] = None
    temperature: float = 0
    top_p: float = 0
    max_tokens: int = 1000
    preview_api_version: str = MINIMUM_SUPPORTED_AZURE_OPENAI_PREVIEW_API_VERSION

    @model_validator(mode="after")
    def checking_azure_openai_endpoint(self):
        if self.endpoint:
            return Self

        elif self.resource:
            self.endpoint = f"https://{self.resource}.openai.azure.com"
            return Self

        raise ValidationError("AZURE_OPENAI_ENDPOINT or AZURE_OPENAI_RESOURCE is required")



# Creating Pydantic Base Models class
class _AppSettings(BaseModel):
    """
    Complete Encapsulated class of App Settings
    """
    openai_settings: _AzureOpenAISettings = _AzureOpenAISettings()

app_settings = _AppSettings()
