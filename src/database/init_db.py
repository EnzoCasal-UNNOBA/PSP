from src.database.database import get_connection
from src.config import SCHEMA_PATH


def initialize_database():

    with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
        schema = file.read()

    conn = get_connection()

    cursor = conn.cursor()

    cursor.executescript(schema)

    conn.commit()

    conn.close()


if __name__ == "__main__":
    initialize_database()

    print("Base de datos creada correctamente.")