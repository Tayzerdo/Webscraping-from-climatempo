# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 14:54:41 2021

@author: Asus
"""

#Take the information from Clima tempo website

#Import the libraries
from bs4 import BeautifulSoup as BS
import requests

#Make the request
html = requests.get("https://www.climatempo.com.br/previsao-do-tempo/cidade/321/riodejaneiro-rj/").content
soup = BS(html, 'html.parser')

print('---------')

#
tempMin = soup.find("span", class_="_margin-r-20")
print(tempMin)
print('---------')

tempMax = soup.find(id="max-temp-1")
print(tempMax)
print('---------')

rainy = soup.find_all(class_="_margin-l-5")
print(rainy[2])
print('---------')

wind = soup.find_all(class_="_flex")
# for i in range(0,len(wind)):
#     print('the number is: ', i)
#     print(wind[i])
print(wind[40])
print('---------')

humidity = soup.find_all(class_="_flex")
hum = humidity[41].find(class_="_margin-r-20")
hum = humidity[41].find_all("span")
print(hum[1])
print(hum[3])
print('---------')

sun = soup.find_all(class_="item")
# for i in range(0,len(sun)):
#     print('the number is: ', i)
#     print(sun[i])
sunny = sun[24].find_all("span")
print(sunny[1])

