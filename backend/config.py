import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


class Settings:
    def __init__(self):
        self.OPENAI_API_KEY = self._required("OPENAI_API_KEY")

        self.OPENAI_CHAT_MODEL = os.getenv(
            "OPENAI_CHAT_MODEL",
            "gpt-4o-mini"
        )

        self.OPENAI_EMBEDDING_MODEL = os.getenv(
            "OPENAI_EMBEDDING_MODEL",
            "text-embedding-3-small"
        )

        self.CHROMA_COLLECTION = os.getenv(
            "CHROMA_COLLECTION",
            "docutrace_knowledge_base"
        )

        self.CHROMA_DB_PATH = os.getenv(
            "CHROMA_DB_PATH",
            str(BASE_DIR / "chroma_db")
        )

    @staticmethod
    def _required(name):
        value = os.getenv(name)

        if not value:
            raise RuntimeError(
                f"Missing required environment variable: {name}"
            )

        return value


settings = Settings()