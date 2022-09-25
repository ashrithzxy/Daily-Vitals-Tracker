from fastapi import APIRouter
from .api import GoogleSheetsApi
from pydantic import BaseModel
from utils.oauth import Oauth

sheetsrouter = APIRouter(prefix="/sheets")

class Data(BaseModel):
    bloodPressure: list[list[int]]
    wbb: list[int]
    wab: list[int]

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