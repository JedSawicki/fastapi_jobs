from enum import Enum

import uvicorn
from fastapi import FastAPI, HTTPException

from linkedin_scraper import Scraper

app = FastAPI()
scrapy = Scraper()


class ModelName(str, Enum):
    first = "junior"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/dbjobs/{model_name}")
async def read_item(model_name: ModelName):
    # junior-python-jobs
    if model_name == ModelName.first:
        return scrapy.custom_linkedin_worker(model_name.value, '', '')


@app.get("/{jobs}")
async def read_item(jobs):
    return scrapy.linkedin_worker('junior-python-jobs')


@app.get("/linkedin/{job}")
async def read_item(job: str):
    # junior-python-jobs
    return scrapy.linkedin_worker(job)


@app.get("/customjobs/{test1}")
async def read_item():
    # junior-python-jobs
    return scrapy.custom_linkedin_worker('senior', 'tester', '')


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
