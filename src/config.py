from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    tiktoken_tokenizer: str = "cl100k_base"
    input_csv: Path = BASE_DIR / "data" / "coffee_sales.csv"
    output_csv: Path = BASE_DIR / "data" / "embeddings.csv"
    host: str = "0.0.0.0"
    port: int = 8000
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()