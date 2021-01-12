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
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
# print("libraries imported")

#Make the request
html = requests.get("https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/321/riodejaneiro-rj").content
now = BS(html, "lxml")

html = requests.get("https://www.climatempo.com.br/previsao-do-tempo/cidade/321/riodejaneiro-rj/").content
today = BS(html, "lxml")

print("---------------------------")
#STEP 1 - Take the information for now
timenow = datetime.now()
print("The time for now is: ",timenow.hour, ':', timenow.minute)
instant = list(now.find("div", class_="card _justify-center").text.split("\n"))
instant= list(filter(None,instant))
# print(instant)
print(f'The temperature is {instant[1]} with the thermal sensation {instant[3][-3:]}')
print(f'The wind has the direction and velocity equals to {instant[5]}')
print(f'The humidity is {instant[7]}')
print(f'The pressure is {instant[9]}')


print("---------------------------")
#STEP 2 - Take the general forecast for the day
info = today.find_all("ul", class_="variables-list")[0]
# print(info)
# print("---------")

##Check the date
timestamp = today.find("h1",class_="-bold -font-18 -dark-blue _margin-r-10 _margin-b-sm-5").text
print(timestamp)
print("---------")

##Extract the minumum and maximum temperature
tempMin = info.find(class_="_margin-r-20").text
print(f'The minimum temperature is: {tempMin}')
tempMax = info.find(id="max-temp-1").text
print(f'The maximum temperature is: {tempMax}')
print("---------")

##Extract the rainy in millimeters and the probability
rainy = info.find("span",class_="_margin-l-5").text.replace(" ","").split("-")
rainyMil = rainy[0]
rainyProb = rainy[1]
print(f'The rainy is: {rainyMil}')
print(f'The probability to rain is: {rainyProb}')
print("---------")

##Extract the information for the wind direction and the velocity in km/h
wind = info.find_all(class_="item")[2].div.text.replace(" ","").strip().split("-")
windDirec = wind[0]
windVelo = wind[1]
print(f'The wind velocity will be: {windVelo}')
print(f'The wind direction will be: {windDirec}')
print("---------")

humidity = info.find_all(class_="item")[3].div
hum = humidity.find_all("span")
humMin = hum[1].text
humMax = hum[3].text
print(f'The minimum humidity is: {humMin}')
print(f'The maximum humidity is: {humMax}')
print("---------")

sun = info.find_all(class_="item")[4]
sunny = sun.find_all("span")
suntime = sunny[1].text.strip().split()
sunrise = suntime[0]
sunset = suntime[1]
print(f'The sunrise it will be at: {sunrise}')
print(f'The sunset it will be at: {sunset}')

print("---------------------------")
#STEP 3 - Take the hourly forecast
hourly = today.find("div",class_="card -no-top")
forecast = hourly.find(class_="wrapper-chart")["data-infos"]
forecastDict = json.loads(forecast)
tableInfo = pd.DataFrame(columns=["Date", "Hour","Humidity","Precipitation","Temperature","Wind","WindDirec"])
for i in forecastDict:
    tableInfo = tableInfo.append({"Date":i["date"].split()[0],
                                  "Hour":i["date"].split()[1].split(":")[0],
                                  "Wind":i["wind"]["velocity"],
                                  "WindDirec":i["wind"]["direction"],
                                  "Temperature":i["temperature"]["temperature"],
                                  "Precipitation":i["rain"]["precipitation"],
                                  "Humidity":i["humidity"]["relativeHumidity"]},ignore_index=True)
    # print(f'The wind velocity will be: {i["wind"]["velocity"]}')
    # print(f'The wind direction will be: {i["wind"]["direction"]}')
    # print(f'The temperature will be: {i["temperature"]["temperature"]}')
    # print(f'The precipitation will be: {i["rain"]["precipitation"]}')
    # print(f'The relative humidity will be: {i["humidity"]["relativeHumidity"]}')
    # print("---")


tableInfo[["humMin","humMax","rainyMil","tempMin","tempMax","windVelo"]]=[humMin[:2],humMax[:2],rainyMil[:-2],tempMin[:-1],tempMax[:-1],windVelo[:-4]]

##Change the data type
tableInfo[["Hour","Humidity","Precipitation","Temperature","Wind","humMin","humMax","rainyMil","tempMin","tempMax",
            "windVelo"]] = tableInfo[["Hour",
        "Humidity","Precipitation","Temperature","Wind","humMin","humMax","rainyMil","tempMin","tempMax","windVelo"]].apply(pd.to_numeric)
tableInfo["PrecipitationAccumulative"] = tableInfo["Precipitation"].cumsum()

# print(tableInfo.dtypes)
# print(tableInfo.head(0))

##Save the table in excel file
tableInfo.to_excel("Table info.xlsx")

# ##Plot the graphs
# plt.plot(tableInfo["Hour"], tableInfo["Humidity"], label="forecast", color="black")
# plt.plot(tableInfo["Hour"], tableInfo["humMin"], label="humMin", color="Lightblue", linestyle="dashed")
# plt.plot(tableInfo["Hour"], tableInfo["humMax"], label="humMax", color="Lightgreen", linestyle="dashed")
# plt.title("Forecast Humidity")
# plt.xlabel("Hour")
# plt.ylabel("Humidity (%)")
# plt.xlim(xmin=0,xmax=23)
# plt.legend()
# plt.show()

# plt.plot(tableInfo["Hour"], tableInfo["Temperature"], label="Temperature", color="black")
# plt.plot(tableInfo["Hour"], tableInfo["tempMin"], label="tempMin", color="Lightblue", linestyle="dashed")
# plt.plot(tableInfo["Hour"], tableInfo["tempMax"], label="tempMax", color="Lightgreen", linestyle="dashed")
# plt.title("Forecast Temperature")
# plt.xlabel("Hour")
# plt.ylabel("Temperature (°)")
# plt.xlim(xmin=0,xmax=23)
# plt.legend(loc=1)
# plt.show()

# plt.bar(tableInfo["Hour"], tableInfo["Precipitation"])
# #plt.bar(tableInfo["Hour"], tableInfo["PrecipitationAccumulative"])
# plt.xlim(xmin=0,xmax=23)
# plt.show()
