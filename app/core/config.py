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

    # Embeddings
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    # ChromaDB
    # ChromaDB
    chroma_persist_directory: str = "./data/chroma_db"
    chroma_collection_name: str = "infrapilot_knowledge_base"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

settings=Settings()