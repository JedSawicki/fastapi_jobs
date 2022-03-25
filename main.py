from typing import Optional, List
from pydantic import Json

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import Offer

from linkedin_scraper import Scraper

app = FastAPI()
scrapy = Scraper()

templates = Jinja2Templates(directory='templates')

db: List[Offer] = []

@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/get/linkedin/{tag}")
async def read_item(tag: str, tag2: Optional[str] = None, tag3: Optional[str] = None, tag4: Optional[str] = None):
    offers = scrapy.linkedin_worker(tag, tag2, tag3, tag4)
    for elem in offers:
        db.append(elem)
    # junior-python-jobs
    return scrapy.linkedin_worker(tag, tag2, tag3, tag4)


@app.get("/get/nofluffjobs/{technology}")
async def read_item(request: Request, technology: str, seniority: Optional[str] = None, second_tech: Optional[str] = None):
    offers = scrapy.no_fluff_jobs_worker(technology, seniority, second_tech)
    for elem in offers:
        db.append(elem)
    
    return scrapy.no_fluff_jobs_worker(technology, seniority, second_tech)


@app.get('/get/db')
async def fetch_offers():
    return db;

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
