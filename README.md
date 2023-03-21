# Daily Vitals Tracker

A FastAPI application that serves APIs that update a google sheet with blood pressure-related data.

A family member has been tasked to monitor their blood pressure, pulse, and weight daily. 
Currently, they are taking the readings and updating a Google Sheet on their phone. Now, 
we all know working with an excel sheet on a tiny mobile screen is a tedious task. 
To make this ordeal suck less, I figured why not make an API which handles 
the "updating the Google Sheets" part and the only thing left to do is give this API the data.

Made a simple HTML form that makes it easier to enter data on a mobile screen.
A simple JS snippet to send the HTML form data to the back-end as JSON.

As of now, we need a Google spreadsheet to already exist, an individual sheet having its title in the format of "%b%y" and this sheet to have the necessary column headers. Future versions will be able to do these tasks automatically.

The current version does the following tasks:
1. Get data from the front-end.
2. Calculate avg blood pressure and weight.
3. Update Google Sheet with new data.