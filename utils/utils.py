import os, json
from datetime import datetime as dt
import httpx

class Utils:
    def __init__(self):
        self.sheetId = os.environ.get("sheetId",None)
        self.spreadSheetId = os.environ.get("google_spreadsheetId")
        self.service_account_oauth_token = os.environ.get("service_account_oauth_token")
        self.currentMonthSheetId = os.environ.get("currentMonthSheetId",None)

    async def getSheetIdForCurrentMonth(self):
        monthYearString = await self.getMonthYearString()
        if self.currentMonthSheetId != monthYearString:
            print("No sheet Id found for current month, setting sheet Id.")
            
            url = f"https://sheets.googleapis.com/v4/spreadsheets/{self.spreadSheetId}"
            headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.service_account_oauth_token}'
            }

            async with httpx.AsyncClient() as client:
                response = httpx.get(url, headers=headers)
            
            spreadsheetProperties = response.json()
            sheetsList = spreadsheetProperties.get("sheets")
            sheetId = None
            for sheet in sheetsList:
                sheetProperty = sheet.get("properties")
                sheetTitle = sheetProperty.get("title")
                if sheetTitle == monthYearString:
                    sheetId = sheetProperty.get("sheetId")
                    break
            print(f"sheetId is: {sheetId}")
            os.environ['currentMonthSheetId'] = str(sheetId)
            print(f"sheetId is: ",sheetId)
            return sheetId
    
    async def getMonthYearString(self):
        print("getMonthYearString from utils")
        today = dt.today().date()
        monthYearString = today.strftime("%b%y")
        # print(f"monthYearString is {monthYearString}")
        return monthYearString