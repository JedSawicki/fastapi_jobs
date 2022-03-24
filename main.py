from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from linkedin_scraper import Scraper

app = FastAPI()
scrapy = Scraper()

templates = Jinja2Templates(directory='templates')

@app.get("/")
async def root():
    return {"message": "Hello World"}


# @app.get("/{jobs}")
# async def read_item(jobs):
#     return scrapy.linkedin_worker('junior-python-jobs')


@app.get("/linkedin/{tag}")
async def read_item(tag: str, tag2: Optional[str] = None, tag3: Optional[str] = None, tag4: Optional[str] = None):
    # junior-python-jobs
    return scrapy.linkedin_worker(tag, tag2, tag3, tag4)


@app.get("/nofluffjobs/{technology}", response_class=HTMLResponse)
async def read_item(request: Request, technology: str, seniority: Optional[str] = None, second_tech: Optional[str] = None):
    element = scrapy.no_fluff_jobs_worker(technology, seniority, second_tech)[0]
    
    element['request'] = request
    return templates.TemplateResponse('item.html', element)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
