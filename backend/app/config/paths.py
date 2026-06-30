from pathlib import Path

# ==========================================
# Project Root (ANCHOR)
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

BACKEND_DIR = PROJECT_ROOT / "backend"

APP_DIR = BACKEND_DIR / "app"

# ==========================================
# Knowledge
# ==========================================

KNOWLEDGE_DIR = APP_DIR / "knowledge"

METADATA_DIR = KNOWLEDGE_DIR / "metadata"

DICTIONARY_DIR = KNOWLEDGE_DIR / "dictionary"

# ==========================================
# Metadata Files
# ==========================================

CATALOG_FILE = METADATA_DIR / "catalog.json"

DICTIONARY_CATALOG_FILE = METADATA_DIR / "dictionary_catalog.json"

MERGED_CATALOG_FILE = METADATA_DIR / "merged_catalog.json"

# ==========================================
# Dictionary
# ==========================================

DICTIONARY_PDF = DICTIONARY_DIR / "dictionary.pdf"

# ==========================================
# Vector Database
# ==========================================

VECTOR_DB_DIR = BACKEND_DIR / "chroma_db"