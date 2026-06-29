from pathlib import Path

# ==========================================
# Project Root
# ==========================================

APP_DIR = Path(__file__).resolve().parent.parent

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

BACKEND_DIR = APP_DIR.parent

VECTOR_DB_DIR = BACKEND_DIR / "chroma_db"