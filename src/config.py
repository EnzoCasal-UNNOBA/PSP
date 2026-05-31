from pathlib import Path

# Raíz del proyecto (psp-manager/)
ROOT_DIR = Path(__file__).resolve().parent.parent

# Directorios de trabajo
DATA_DIR = ROOT_DIR / "data"
EXPORT_DIR = ROOT_DIR / "exports"

# Crear directorios si no existen
DATA_DIR.mkdir(exist_ok=True)
EXPORT_DIR.mkdir(exist_ok=True)

# Base de datos SQLite
DB_PATH = DATA_DIR / "psp_manager.db"

# Esquema SQL
SCHEMA_PATH = ROOT_DIR / "src" / "database" / "schema.sql"