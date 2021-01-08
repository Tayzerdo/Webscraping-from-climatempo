# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 14:54:41 2021

@author: Asus
"""

#Take the information from Clima tempo website

#STEP 0 - Import the libraries and make the request
from bs4 import BeautifulSoup as BS
import requests
import json
import pandas as pd
print('libraries imported')

#Make the request
html = requests.get("https://www.climatempo.com.br/previsao-do-tempo/cidade/321/riodejaneiro-rj/").content
soup = BS(html, 'lxml')


#STEP 1 - Take the general forecast for the day
info = soup.find_all("ul", class_="variables-list")[0]
print('---------')
##Extract the minumum and maximum temperature
tempMin = info.find(class_="_margin-r-20").text
print(f'The minimum temperature is: {tempMin}')
tempMax = info.find(id="max-temp-1").text
print(f'The maximum temperature is: {tempMax}')
print('---------')

##Extract the rainy in millimeters and the probability
rainy = info.find("span",class_="_margin-l-5").text.replace(' ','').split("-")
rainyMil = rainy[0]
rainyProb = rainy[1]
print(f'The rainy is: {rainyMil}')
print(f'The probability to rain is: {rainyProb}')
print('---------')

##Extract the information for the wind direction and the velocity in km/h
wind = info.find_all(class_="item")[2].div.text.replace(' ','').strip().split("-")
windDirec = wind[0]
windVelo = wind[1]
print(f'The wind velocity will be: {windVelo}')
print(f'The wind direction will be: {windDirec}')
print('---------')

humidity = info.find_all(class_="item")[3].div
hum = humidity.find_all("span")
humMin = hum[1].text
humMax = hum[3].text
print(f'The minimum humidity is: {humMin}')
print(f'The maximum humidity is: {humMax}')

print('---------')

sun = info.find_all(class_="item")[4]
sunny = sun.find_all("span")
suntime = sunny[1].text.strip().split()
sunrise = suntime[0]
sunset = suntime[1]
print(f'The sunrise it will be at: {sunrise}')
print(f'The sunset it will be at: {sunset}')
print('---------')

#STEP 2 - Take the hourly forecast
hourly = soup.find("div",class_="card -no-top")
forecast = hourly.find(class_="wrapper-chart")["data-infos"]
forecastDict = json.loads(forecast)
tableInfo = pd.DataFrame(columns=['Date', 'Hour','Humidity','Precipitation','Temperature','WindVelo','WindDirec'])
for i in forecastDict:
    tableInfo = tableInfo.append({'Date':i["date"].split()[0],
                                  'Hour':i["date"].split()[1].split(":")[0],
                                  'WindVelo':i["wind"]["velocity"],
                                  'WindDirec':i["wind"]["direction"],
                                  'Temperature':i["temperature"]["temperature"],
                                  'Precipitation':i["rain"]["precipitation"],
                                  'Humidity':i["humidity"]["relativeHumidity"]},ignore_index=True)
    # print(f'The wind velocity will be: {i["wind"]["velocity"]}')
    # print(f'The wind direction will be: {i["wind"]["direction"]}')
    # print(f'The temperature will be: {i["temperature"]["temperature"]}')
    # print(f'The precipitation will be: {i["rain"]["precipitation"]}')
    # print(f'The relative humidity will be: {i["humidity"]["relativeHumidity"]}')
    print('---')

print(tableInfo)




