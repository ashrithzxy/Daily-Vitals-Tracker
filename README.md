# Blood Pressure GSheet API

A FastAPI application that serves APIs which update a google sheet with blood pressure related data.

A family member has been tasked to monitor their blood pressure, pulse and weight daily. 
Currently they are taking the readings and updating a Google Sheet on their phone. Now, 
we all know working with an excel sheet on a tiny mobile screen is a tedious task. 
In order to make this ordeal suck less, I figured why not make an API which handles 
the "updating the Google Sheets" part and the only thing left to do is give this API the data.

This application should do the following:
1. Create a new sheet at the beginning of every month and add column headers.
2. Calculate avg blood pressure and weight.
3. Account for no weight data. 
4. Update records for given date if data already exists.

## Phase I

Assuptions:
- Spreadsheet and month sheet aleady exist with column headers.

Requirements:
- Add data at the end of sheet.

## Phast II

Assumptions:
- Spreadsheet exists, month sheet doesn't exist.
- BP is taken in the morning and at night.

# Phase III

Assumptions:
- (Check if this is possible) Spreadsheet doesn't exist. New spreadsheet is created and new month sheet is added with column headers.
- Day was skipped. Clock process should check last entered date.