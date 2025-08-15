
import logging
from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import APIRouter, Form, Body, Depends, HTTPException, FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from app.database import get_db, AsyncSQLiteDB
from app.short_url import is_valid_url, ival_code, make_short_url

logger = logging.getLogger(__name__)

router = APIRouter()


class ShortenResponse(BaseModel):
    short_url: str

@router.post("/api/v1/shorten")
async def shorten(url: Annotated[str, Form(..., description="original url to be shortened")], 
                  db: AsyncSQLiteDB = Depends(get_db)) -> ShortenResponse:
    if not is_valid_url(url):
        raise HTTPException(status_code=400, detail=f"incorrect url submitted: {url}")
    ival = await db.next_ival()
    code = ival_code(ival)
    await db.insert_url(code, url)
    logger.debug(f"shorten: {url=} {code=}")
    return {"short_url": make_short_url(code)}


@router.get("/s/{code}", 
            responses={
                307:{"description": "redirect to original url"},
                404:{"description": "short code not found"},
                })
async def redir_by_code(code: str, 
                        db: AsyncSQLiteDB = Depends(get_db)):
    url = await db.do_redir(code)
    if url is None:
        raise HTTPException(status_code=404, detail=f"short code not found: {code}")
    logger.debug(f'Redirect to {url=}')
    return RedirectResponse(url=url)


class StatsResponse(BaseModel):
    orig_url: str
    created_at :str
    redir_count: int

@router.get("/api/v1/stats/{code}")
async def get_stats(code: str, 
                   db: AsyncSQLiteDB = Depends(get_db)) -> StatsResponse:
    stats = await db.get_stats(code)
    if stats is None:
        raise HTTPException(status_code=404, detail=f"short code not found: {code}")
    logger.debug(f"Stats for {code=} {stats}")
    return stats


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("init db")
    db = get_db()
    await db.create_tables()
    yield
    logger.info("shutdown")
