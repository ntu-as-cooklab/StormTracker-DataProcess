import logging
import os
from time import gmtime, strftime, localtime
import math
from math import pi, sqrt, cos, sin, tan, asin, acos, atan
import dateutil.parser
import datetime
from datetime import timedelta


channel = [dict() for _ in range(100)]


def view_params(lat1D, lon1D, alt1, lat2D, lon2D, alt2):
    # Input: lat of observer, lon of observer, altitude(m) of observer
    #        lat of object,   lon of object,   altitude(m) of object

    ## Haversine formula
    ## Vincenty's formulae
    ## Great-circle navigation
    ## World Geodetic System

    R = 6378100 # Radius of Earth (km)

    # Convert degrees to radians
    lat1 = lat1D * pi/180
    lat2 = lat2D * pi/180
    lon1 = lon1D * pi/180
    lon2 = lon2D * pi/180

    # Difference in latitude/longitude
    dLon = lon2 - lon1
    dLat = lat2 - lat1

    # Distance: haversine formula
    h = sin(dLat/2)*sin(dLat/2) + cos(lat1)*cos(lat2)*sin(dLon/2)* sin(dLon/2)
    if h > 1 : h = 1
    d = 2 * R * asin(sqrt(h))
    
    # Azimuth
    a1 = atan(sin(dLon) / (cos(lat1)*tan(lat2) - sin(lat1)*cos(dLon)))
    if dLat < 0: a1 += pi
    if a1 < 0 : a1 += 2*pi

    # Elevation angle
    lmd = atan( (alt2-alt1)/d )

    # Convert radians to degrees
    a1D = a1 * (180/pi)
    lmdD = lmd * (180/pi)

    return d/1000.0, a1D, lmdD # Distance(km), Azimuth(deg), Elevation angle(deg)


last_ID = -1

def readdata(data):
    global last_ID
    global station_lat
    global station_lon
    global station_height

    csv = data.split(',')
    try:
        t = dateutil.parser.parse(csv[0])+timedelta(hours=8)
        pass
    except Exception as e:
        print (csv[0])
        return ""
    if len(csv)<11:
      return ""
      pass
    if last_ID == int(csv[2]):
      return ""
      pass
    last_ID = int(csv[2])
    node_lat = float(csv[8])/100000
    if node_lat ==0:
      return ""
      pass
    node_lon = float(csv[7])/100000
    node_height = float(csv[9])/100
    sat_count = int(csv[10])
    if sat_count<3: 
      return ""
      pass
    d = 0
    phi = 0
    lamba = 0
    if station_lat != node_lat and station_lon != node_lon:
      try:
        d,phi,lamba = view_params(station_lat,station_lon,station_height,node_lat,node_lon,node_height)
        pass
      except Exception as e:
        print (e)
      pass
      

    temp = float(csv[3])/100
    humidity = float(csv[4])/10
    pressure = float(csv[5])/100
    voltage = float(csv[6])/1023*1.1*2
    rssi = float(csv[11])
    if rssi > 0:
      rssi = -rssi
      pass
    speed = float(csv[14])/100
    SNR = int(csv[15])
    Direction = float(csv[16])/100
    data_str = t.strftime("%Y/%m/%d %H:%M:%S.%f")+","+csv[13]+","+csv[2]+","+str(temp)+","+str(humidity)+","+str(pressure)+","+str(voltage)+","+str(rssi)+","+str(node_lat)+","+str(node_lon)+","+str(node_height)+","+str(d)+","+str(sat_count)+","+str(SNR)+","+str(speed)+","+str(Direction)+","+str(lamba)+"\n"
    return data_str
    pass



for filename in os.listdir("."):
  if filename.startswith("LoRa_"):
    data_log = open(filename,'r')
    data = data_log.readlines()
    for line in data:
      try:
        ID = int(line.split(",")[17])
        packageNo = int(line.split(",")[2])
        pass
      except Exception as e:
        continue
      try:
        channel[ID][packageNo] =  line
        pass
      except Exception as e:
        print (e)
        print (line)


data_date = ""
last_date = ""
station_lon = 0
station_lat = 0
station_height = 0


for x in range(0,100):
  channeldata = sorted(channel[x])
  if len(channeldata) < 100:
    continue
    pass
  try:
    last_date = dateutil.parser.parse(channel[x][channeldata[0]].split(",")[0])+timedelta(hours=8)
    station_lon = float(channel[x][channeldata[50]].split(",")[7])/100000
    station_lat = float(channel[x][channeldata[50]].split(",")[8])/100000
    station_height = float(channel[x][channeldata[50]].split(",")[9])/100
    print("Station Position for Node "+str(x)+"==> "+str(station_lat)+","+str(station_lon)+","+str(station_height))
    pass
  except Exception as e:
    print (e)
    print (channel[x][channeldata[0]])
    station_lon = 0
    station_lat = 0
    station_height = 0
  
  f = open("no_"+str(x)+"_"+last_date.strftime("%Y%m%d_%H%M")+".csv",'w')
  f.write("Time,channel,PacketID,Temperature(degree C),Humidity(%),Pressure(hPa),Voltage(V),RSSI,Lat,Lon,Height(m),Distance(km),Sat,SNR,Speed(km/hr),Direction(degree),angle(degree)\n")  
  print ("Storm Tracker NO: " + str(x) +" Data Length:"+ str(len(channeldata)))
  for line in channeldata:
      data = readdata(channel[x][line])
      if data == "":
        continue
        pass
      f.write(data)
  pass

print("轉檔完畢")
while 1:
    pass
