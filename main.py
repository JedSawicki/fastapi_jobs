from typing import Optional, List
from pydantic import Json

import uvicorn
import random
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from models import Offer

from linkedin_scraper import Scraper

app = FastAPI()
scrapy = Scraper()

templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")

db: List[Offer] = []

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/get/offers")
async def read_items(request: Request, technology: str, seniority: Optional[str] = None, second_tech: Optional[str] = None):
    linkedin_offers = scrapy.linkedin_worker(technology, seniority, second_tech, None)
    nofluff_offers = scrapy.no_fluff_jobs_worker(technology, seniority, second_tech)
    offers = linkedin_offers + nofluff_offers
    random.shuffle(offers)
    print(offers)
    
    for elem in offers:
        db.append(elem)

    return db

@app.get('/get/db')
async def fetch_offers():
    return db


@app.get("/form", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse('item.html', {"request": request})


@app.post("/form", response_class=HTMLResponse)
async def post_from(request: Request, key_words: str = Form(...)):
    offers = []
    print(f'technology: {key_words}')
    key_list = []
    res = len(key_words.split())
    keys = key_words.split()
    print(keys[0])
    for key in keys:
        if key is not None:
            key_list.append(key)
        else:
            key_list.append(None)
    while len(key_list) != 4:
        key_list.append(None)
    print(key_list)
    try:
        linkedin_offers = scrapy.linkedin_worker(key_list[0], key_list[1], key_list[2], None)
        nofluff_offers = scrapy.no_fluff_jobs_worker(key_list[0], key_list[1], key_list[2])
        offers = linkedin_offers + nofluff_offers
        random.shuffle(offers)
        
    except IndexError:
        print('Index ERROR')
       
    
    return templates.TemplateResponse('item.html', {"request": request, "offers": offers}  )

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
