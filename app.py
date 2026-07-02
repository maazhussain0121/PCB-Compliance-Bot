from fastapi import FastAPI
from router import response

app = FastAPI(title = "PCB Compliance Bot")


app.include_router(response.router)
