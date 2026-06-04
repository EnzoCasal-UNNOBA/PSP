from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT_DIR / "data"
EXPORT_DIR = ROOT_DIR / "exports"

DATA_DIR.mkdir(exist_ok=True)
EXPORT_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "psp_manager.db"

SCHEMA_PATH = ROOT_DIR / "src" / "database" / "schema.sql"