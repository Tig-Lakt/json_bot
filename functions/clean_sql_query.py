

def clean_sql_query(raw_query: str) -> str:
    clean_query = raw_query.replace("```sql", "").replace("```", "")
    return clean_query.strip()