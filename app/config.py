
import os

DB_FILE = os.getenv("DB_FILE", "./var/pyurls.db")

SHORT_URL_BASE = os.getenv("SHORT_URL_BASE", "http://localhost:8000")

NEXT_SEQ = os.getenv("NEXT_SEQ")
