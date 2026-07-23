from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    app_name: str = "InfraPilot AI API"
    app_version: str = "1.0.0"
    debug: bool = True

    # LLM
    llm_provider: str = "openrouter"
    openrouter_api_key: str
    llm_model: str = "openrouter/free"

    # Database
    database_url: str = ""

    # ChromaDB
    chroma_db_path: str = "./chroma_db"

    # Embeddings
    embedding_model: str = "BAAI/bge-small-en-v1.5"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()