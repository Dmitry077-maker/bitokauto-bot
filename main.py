import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# Актуальная ссылка на наш веб-сервис на Render
WEB_URL = "https://bitokauto-bot.onrender.com"

@app.get("/", response_class=HTMLResponse)
async def root():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>BitokAuto.ua Backend is running! index.html not found.</h1>"
