
import logging
from fastapi import Depends, FastAPI

from app.config import DB_FILE
from app.database import AsyncSQLiteDB, get_db
import app.api as api


logging.basicConfig(
    level=logging.DEBUG,  # NOTE: not for production
    format='%(asctime)s %(name)s %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger(__name__)


app = FastAPI(
    docs_url="/docs", 
    redoc_url="/redoc",
    lifespan=api.lifespan,
)

app.include_router(api.router)

@app.get("/")
def root():
    """Demo application root page"""
    return {
        "message": "dev demo root",
        "docs_url": "/docs", 
        "redoc_url": "/redoc", 
        }

