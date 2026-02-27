import psycopg2
import os

def get_connection():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL not found")
        return None
    return psycopg2.connect(database_url)