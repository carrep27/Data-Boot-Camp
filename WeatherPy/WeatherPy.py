
# coding: utf-8

# ## WeatherPy

# In[45]:


# Dependencies
import openweathermapy.core as owm
import pandas as pd
import numpy as np
import random
from citipy import citipy 
import matplotlib.pyplot as plt
import requests
import time
from config import apikey


# ## Gather Data

# In[46]:


#Get random coordinates using import random. Latitude runs from 0 to 90 so we are asking for range +-90. Longtitude runs from
# 0 to 180 so we are asking for range +-180. 

#create empty lists we will append to
Latitude = []
Longitude = []
for x in range(0,1500):
    Latitude.append(random.uniform(-90,90))
    Longitude.append(random.uniform(-180,180))

#create dataframe for the latitude and longitude data we just collected. 

Cities = pd.DataFrame(columns = ["Latitude","Longitude"])
Cities["Latitude"] = Latitude
Cities["Longitude"] = Longitude


# In[47]:


#Use Citiypy to get City closest to Coordinates

#create empty list we will append City name to
Cities1 =[]

#use iterrow to loop through Latitude and Longitude from DataFrame "Cities" we just created to get nearest city
for index, row in Cities.iterrows():
    City=citipy.nearest_city(row["Latitude"],row["Longitude"])
    Cities1.append(City.city_name)

#add the list of cities to the dataframe which already contains our Latitude and Longitude
Cities["City"]=Cities1


# In[48]:


#remove any duplicate cities so only unique values. This is why we chose 1500 sets of random numbers....so that when 
#dupliates are elminated, we are left with at least 500 unique cities

new_data = Cities.drop_duplicates("City",keep="first")
print("We have " + str(len(new_data)) + " cities.")

# new_data


# In[49]:


#Utilize openweathermap api to get climate conditions at each city

units = "Imperial"
appid = apikey
url = "http://api.openweathermap.org/data/2.5/weather?"
query_url = f"{url}appid={apikey}&units={units}&q=" 


#create empty lists what we will append to with each API pull and set a city counter to 0
counter = 0
Temp = []
C = []
LTTE = []
LNGE = []
HUM = []
CL = []
WS = []


# Loop through the list of cities and perform a request for data on each
# because CityPy can return a City name that openweathermap might not recongize (for whatever reason), we utilize try/except

for index,row in new_data.iterrows():
    counter = counter + 1
    x=row["City"]
    q_url = query_url + str(x)
    response = requests.get(q_url).json()
    try:
        print(f"City #{counter}.") #print the # the city holds in our list (aka where we are in the loop)
        print(f"City name is {x} and its url is {q_url}.") #print the api url
        print("The City ID is " + str(response["id"]) + ".") #print the city id
        Temp.append(response['main']['temp']) #get the Temp (will be in farenheit cause we declared Imperial units)
        LNGE.append(response["coord"]["lon"]) #get Longitude
        LTTE.append(response["coord"]["lat"]) #get Latitue
        C.append(response["name"]) # get City Name
        HUM.append(response["main"]["humidity"]) #get Humidity
        CL.append(response["clouds"]["all"]) #get Cloudiness
        WS.append(response["wind"]["speed"]) #get WindSpeed (will be in mph cause we declared units Imperial)                       
    except: #if openweathermap cannot find a city, the city will be skipped and the message below will be prints
        print("This is not a city recognized in OpenWeatherMap.There will be no data for this city")
        pass
    print("------------------------------------------------------------------------------------")

#after cycling through the data, create a new data frame that contains all the info we just gathered and appended into lists
#first the dataframe and one column is created, and then each subsequent column is added
citydata=pd.DataFrame(columns = ["City"])

citydata["City"] = C
citydata["Longtitude"] = LNGE
citydata["Latitude"]=LTTE
citydata["Temperature"]= Temp
citydata["Humidity"] = HUM
citydata["Cloudiness"] = CL
citydata["Wind Speed"] = WS



# In[50]:


#print head of datafram to verify it looks ok
citydata.head()


# ## Temp Vs Latitude

# In[51]:


#Temp vs Latitude Graph

#set x value as Latitude and y as Temperature. Then repeat with humidity, cloudiness and windspeed.

xvalue = citydata["Latitude"]
yvalue = citydata["Temperature"]

plt.title("Temperature Vs Latitude (%s)" % time.strftime("%x"))
plt.xlabel("Latitude")
plt.ylabel("Temperature in Farenheit")

plt.scatter(xvalue, yvalue, marker="o", color="red", edgecolor="black")
plt.savefig("Temp Vs Latitude.png")
plt.show()


# # Humidity vs Latitude
# 

# In[52]:


#Humidity vs Latitude Graph

xvalue = citydata["Latitude"]
yvalue = citydata["Humidity"]

plt.title("Humidity Vs Latitude (%s)" % time.strftime("%x"))
plt.xlabel("Latitude")
plt.ylabel("Humidity")

plt.scatter(xvalue, yvalue, marker="o", color="blue", edgecolor="black")
plt.savefig("Humidity Vs Latitude.png")
plt.show()


# ## Cloudiness vs Latitude

# In[53]:


#Cloudiness vs Latitude Graph
xvalue = citydata["Latitude"]
yvalue = citydata["Cloudiness"]

plt.title("Cloudiness vs Latitude (%s)" % time.strftime("%x"))
plt.xlabel("Latitude")
plt.ylabel("Cloudiness")

plt.scatter(xvalue, yvalue, marker="o", color="green", edgecolor="black")
plt.savefig("Cloudiness Vs Latitude.png")
plt.show()



# ## Wind Speed vs Latitude

# In[54]:


#Wind Speed vs Latitude Graph
xvalue = citydata["Latitude"]
yvalue = citydata["Wind Speed"]

plt.title("Wind Speed (mph) Vs Latitude (%s)" % time.strftime("%x"))
plt.xlabel("Latitude")
plt.ylabel("Wind Speed")

plt.scatter(xvalue, yvalue, marker="o", color="orange", edgecolor="black")
plt.savefig("Wind Speed in mph Vs Latitude.png")
plt.show()



# ## Analysis

# In[55]:


#There appears to be a strong relationship between Temperature and distance from the equator. The farther one is away from
#the equator (Lat= 0), the colder it gets


#There doesnt seem to be a very strong correlation with Wind Speed or Cloudiness with Latitude
#There appears to be more cities in the Northern Hemisphere than Southern.

