import os
import sys
import logging
from dotenv import load_dotenv


PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_PATH)
dotenv_path = os.path.join(PROJECT_PATH, ".env")
load_dotenv(dotenv_path)

logging.basicConfig(level=logging.INFO)


def get_bot_token() -> str:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        logging.error("Ошибка: Переменная окружения TELEGRAM_BOT_TOKEN не задана.")
        return None 
    return token


def get_openai_api_key() -> str:
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        logging.error("Ошибка: Переменная окружения OPENAI_API_KEY не задана.")
        return None 
    return openai_api_key


def get_db_connection_params() -> list[str]:
    try:
        host = os.environ.get("DB_HOST")
        port = os.environ.get("DB_PORT")
        database = os.environ.get("DB_NAME")
        user = os.environ.get("DB_USER")
        password = os.environ.get("DB_PASSWORD")

        return [host, port, database, user, password]
    
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        return []

