from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException

from linkedin_scraper import Scraper

app = FastAPI()
scrapy = Scraper()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# @app.get("/{jobs}")
# async def read_item(jobs):
#     return scrapy.linkedin_worker('junior-python-jobs')


@app.get("/linkedin/{item_name}")
async def read_item(tag: str, tag2: Optional[str] = None, tag3: Optional[str] = None, tag4: Optional[str] = None):
    # junior-python-jobs
    return scrapy.custom_linkedin_worker(tag, tag2, tag3, tag4)


@app.get("/nofluffjobs/{item_name}")
async def read_item(technology: str, seniority: Optional[str] = None, second_tech: Optional[str] = None):
    return scrapy.no_fluff_jobs_worker(technology, seniority, second_tech)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
