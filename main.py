from typing import Optional, List
from pydantic import Json
import random
import uvicorn
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from models import Offer

from scraper import Scraper

app = FastAPI()
scrapy = Scraper()

templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")

db: List[Offer] = []

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    
    return templates.TemplateResponse('index.html', {"request": request})


@app.post("/scraper/post/offers")
async def write_offers(request: Request, technology: str, seniority: Optional[str] = None, second_tech: Optional[str] = None):
    key_list = [technology, seniority, second_tech]
    while len(key_list) != 4:
        key_list.append(None)
    try:
        offers = scrapy.grand_scraper(key_list[0], key_list[1], key_list[2])
        
    except IndexError:
        print('Index ERROR')
        raise HTTPException(status_code=404, detail="Items not found")
    
    for elem in offers:
        db.append(elem)

    return db

@app.get('/scraper/get/offers')
async def fetch_offers():
    if len(db):
        return db
    else:
       raise HTTPException(status_code=404, detail="Items not found") 


@app.get('/scraper/get/jooble')
async def fetch_offers_jooble(technology: str, seniority: Optional[str] = None, second_tech: Optional[str] = None):
    jooble_offers = scrapy.jooble_jobs_worker(technology, seniority, second_tech)
    
    return jooble_offers

@app.get('/scraper/get/indeed')
async def fetch_offers_indeed(technology: str, seniority: Optional[str] = None, second_tech: Optional[str] = None):
    indeed_offers = scrapy.indeed_jobs_worker(technology, seniority, second_tech)
    
    return indeed_offers

@app.get('/scraper/get/linkedin')
async def fetch_offers_linkedin(technology: str, seniority: Optional[str] = None, second_tech: Optional[str] = None):
    linkedin_offers = scrapy.linkedin_worker(technology, seniority, second_tech)
    
    return linkedin_offers

@app.get('/scraper/get/jobted')
async def fetch_offers_jooble(technology: str, seniority: Optional[str] = None, second_tech: Optional[str] = None):
    jobted_offers = scrapy.jobted_jobs_worker(technology, seniority, second_tech)
    
    return jobted_offers

@app.get('/scraper/get/nofluff')
async def fetch_offers_jooble(technology: str, seniority: Optional[str] = None, second_tech: Optional[str] = None):
    nofluff_offers = scrapy.no_fluff_jobs_worker(technology, seniority, second_tech)
    
    return nofluff_offers

@app.get("/scraper", response_class=HTMLResponse)
async def get_form_scraper(request: Request):
    return templates.TemplateResponse('item.html', {"request": request})


@app.post("/scraper", response_class=HTMLResponse)
async def post_form_scraper(request: Request, key_words: str = Form(...)):
    key_list = []
    keys = key_words.split()
    for key in keys:
        key_list.append(key)
    while len(key_list) != 4:
        key_list.append(None)
    try:
        offers = scrapy.grand_scraper(key_list[0], key_list[1], key_list[2])
        
    except IndexError:
        print('Index ERROR')
        raise HTTPException(status_code=404, detail="Items not found")
       
    
    return templates.TemplateResponse('item.html', {"request": request, "offers": offers})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
