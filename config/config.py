from openai import OpenAI
from utils.get_data import get_bot_token, get_openai_api_key, get_db_connection_params


TOKEN = get_bot_token()
OPENAI_API_KEY = get_openai_api_key()
DB_CONN = get_db_connection_params()

CLIENT_OA = OpenAI(api_key=OPENAI_API_KEY)