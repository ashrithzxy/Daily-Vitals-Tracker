import os, json
from datetime import datetime as dt
import httpx

class GoogleSheetsApi:
    def __init__(self):
        self.spreadSheetId = os.environ.get("google_spreadsheetId")
        self.googleApiKey = os.environ.get("google_api_key")
        self.service_account_oauth_token = os.environ.get("service_account_oauth_token")
        # print(f'spreadSheetId: {self.spreadSheetId}')
        # print(f'googleApiKey: {self.googleApiKey}')
        # print(f'service_account_oauth_token: {self.service_account_oauth_token}')

    async def getSpreadSheetValues(self,monthYearString):

        range = monthYearString+"!A:F"

        url = f"https://sheets.googleapis.com/v4/spreadsheets/{self.spreadSheetId}/values/{range}?key={self.googleApiKey}"

        headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {self.service_account_oauth_token}'
        }

        async with httpx.AsyncClient() as client:
            response = httpx.get(url, headers=headers)
        
        spreadsheetValues = response.json()
        # print(f'get spreadsheet valuee: {spreadsheetValues}')
        return spreadsheetValues

    async def getNextCellMap(self, spreadSheetValues):
        valueList = spreadSheetValues.get("values")
        totalRowCount = len(valueList)
        dataRowCount = totalRowCount - 1
        nextStart = "A" + str(dataRowCount+2)
        nextEnd = "F" + str(dataRowCount+5)
        # print(f"start: {nextStart}, end: {nextEnd}")
        return nextStart, nextEnd

    async def getMonthYearString(self):
        today = dt.today().date()
        monthYearString = today.strftime("%b%y")
        # print(f"monthYearString is {monthYearString}")
        return monthYearString

    async def updateSheet(self, data):
        data = await self.generateData(data)
        monthYearString = await self.getMonthYearString()
        spreadsheetValues = await self.getSpreadSheetValues(monthYearString)
        nextStart, nextEnd = await self.getNextCellMap(spreadsheetValues)
        
        # range = f"Oct22!{nextStart}%3A{nextEnd}"
        range = f"{monthYearString}!{nextStart}%3A{nextEnd}"

        url = f"https://sheets.googleapis.com/v4/spreadsheets/{self.spreadSheetId}/values/{range}?&key={self.googleApiKey}"

        params = {
                    "includeValuesInResponse":True,
                    "valueInputOption":"USER_ENTERED"
                    }

        payload = json.dumps({
                                "majorDimension": "ROWS",
                                # "range": f"Oct22!{nextStart}:{nextEnd}",
                                "range" : f"{monthYearString}!{nextStart}:{nextEnd}",
                                "values": data
                                })
        headers = {
        'Authorization': f'Bearer {self.service_account_oauth_token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
        }

        async with httpx.AsyncClient() as client:
            query = await client.put(url, headers=headers, data=payload, params=params)
        
        response = query.json()
        return response
    
    async def generateData(self,data):
        bpList = data.get("bloodPressure")
        wbb = data.get("wbb",[0,0,0])
        wab = data.get("wab",[0,0,0])
        today = dt.today().date()
        todayString = today.strftime("%d.%m.%Y")
        rowId = today.day
        returnList = []
        rowCount = 1
        for i in range(3):
            rowList = [""]
            rowList.append(wbb[i])
            rowList.append(wab[i])
            rowList.extend(bpList[i])
            returnList.append(rowList)
            rowCount+=1
        
        returnList = await self.addLastRow(returnList,rowId)
        returnList[0][0] = todayString
        # print(f"returnList is: {returnList}")
        return returnList

    async def addLastRow(self,dataList,rowId):
        totalSys = 0
        totalDia = 0
        totalPul = 0
        totalWbb = 0
        totalWab = 0
        # print(dataList)
        for i in dataList:
            totalWbb += i[1]
            totalWab += i[2]
            totalSys += i[3]
            totalDia += i[4]
            totalPul += i[5]
        
        avgWbb = round(totalWbb/3,2)
        avgWab = round(totalWab/3,2)
        avgSys = round(totalSys/3,2)
        avgDia = round(totalDia/3,2)
        avgPul = round(totalPul/3,2)
        dataList.append([rowId,avgWbb,avgWab,avgSys,avgDia,avgPul])
        # print("data list in addLastRow() is: ",dataList)
        return dataList