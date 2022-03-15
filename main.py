from typing import Optional

from enum import Enum

import uvicorn
from fastapi import FastAPI, HTTPException

from linkedin_scraper import Scraper

app = FastAPI()
scrapy = Scraper()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/{jobs}")
async def read_item(jobs):
    return scrapy.linkedin_worker('junior-python-jobs')


@app.get("/linkedin/{item_name}")
async def read_item(item_name: str, item_name2: Optional[str] = None, item_name3: Optional[str] = None):
    # junior-python-jobs
    return scrapy.custom_linkedin_worker(item_name, item_name2, item_name3)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
