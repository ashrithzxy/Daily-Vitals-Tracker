from fastapi import APIRouter
from .api import GoogleSheetsApi
from pydantic import BaseModel
from utils.oauth import Oauth
from typing import List

sheetsrouter = APIRouter(prefix="/sheets")

class Data(BaseModel):
    bloodPressure: List[List[int]]
    wbb: List[int]
    wab: List[int]

@sheetsrouter.put("")
async def update(Data: Data):
    gSheets = GoogleSheetsApi()
    response = await gSheets.updateSheet(Data.dict())
    print(response)
    return response

@sheetsrouter.get("/oauth",include_in_schema=False)
async def oauth():
    gSheetsOauth = Oauth()
    response = await gSheetsOauth.setAccessToken()
    # print(response)
    return "200"
