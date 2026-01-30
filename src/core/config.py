from pydantic_settings import BaseSettings


class LLMSettings(BaseSettings):
    api_base: str = 'https://api.openai.com/v1'
    api_key: str = 'EMPTY'
    model_name: str = 'gpt-4o-mini'

    class Config:
        env_prefix = "OPENAI_"


class Settings(BaseSettings):
    llm: LLMSettings = LLMSettings()
    log_level: str = 'INFO'

    class Config:
        env_prefix = ""


settings = Settings()