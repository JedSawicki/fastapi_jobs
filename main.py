from fastapi import FastAPI, HTTPException

from linkedin_scraper import Scraper

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/{job}")
async def read_item(job):
    jobs = Scraper('junior-python-jobs')
    return jobs.linkedin_worker()
