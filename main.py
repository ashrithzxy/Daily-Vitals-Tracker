from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import gSheetsRouter
from fastapi.middleware.cors import CORSMiddleware
from utils.oauth import Oauth
from utils.utils import Utils

app = FastAPI(
    title="Daily Vitals Tracker",
    docs_url=None,
    redoc_url=None,
    description="""A FastAPI application that serves APIs which update a google sheet with blood pressure related data.

A family member has been tasked to monitor their blood pressure, pulse and weight daily. 
Currently they are taking the readings and updating a Google Sheet on their phone. Now, 
we all know working with an excel sheet on a tiny mobile screen is a tedious task. 
In order to make this ordeal suck less, I figured why not make an API which handles 
the "updating the Google Sheets" part and the only thing left to do is give this API the data.
    
"""
)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(gSheetsRouter.sheetsrouter)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def setOauth():
    gSheetsOauth = Oauth()
    await gSheetsOauth.setAccessToken()
    utilsObj = Utils()
    await utilsObj.getSheetIdForCurrentMonth()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html",{"request":request})