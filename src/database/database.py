import sqlite3

from src.config import DB_PATH


def get_connection():
    conn = sqlite3.connect(DB_PATH)

    conn.execute("PRAGMA foreign_keys = ON")

    return conn