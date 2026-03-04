from datetime import datetime
from config.constants import SYSTEM_PROMPT_TEMPLATE
from config.config import CLIENT_OA


def get_sql_from_llm(user_query: str) -> str:
    prompt = SYSTEM_PROMPT_TEMPLATE.format(now=datetime.now().strftime("%Y-%m-%d %H:%M"))

    response = CLIENT_OA.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_query}
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip()