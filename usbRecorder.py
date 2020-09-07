import serial
from time import gmtime, strftime, localtime
from serial.tools import list_ports
from time import gmtime, strftime, localtime
from math import pi, sqrt, cos, sin, tan, asin, acos, atan
import dateutil.parser
import datetime


def readdata(data):
    global station_lat
    global station_lon
    global station_height

    csv = data.split(',')
    try:
        t = dateutil.parser.parse(csv[0])+datetime.timedelta(hours=8)
        pass
    except Exception as e:
        print (csv[0])
        return ""
    if len(csv)<11:
      return ""
      pass
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

ports = list(list_ports.comports())
print("There are %d COM port(s) found" % len(ports))
print("==============================")
for x in range(0,len(ports)):
    print("[%d] %s" % (x,ports[x][1]))
    pass
print("==============================")

t = datetime.datetime.utcnow()
f = open("LoRa_" + t.strftime("%Y%m%d_%H%M")+".csv",'w')


x = input(">>> Choose COM port(Enter number): ")
Serial = serial.Serial(ports[int(x)][0],57600)
print("Time,channel,PacketID,Temperature(degree C),Humidity(%),Pressure(hPa),Voltage(V),RSSI,Lat,Lon,Height(m),Distance(km),Sat,SNR,Speed(km/hr),Direction(degree),angle(degree)\n")  
while 1:
    try:
        temp = Serial.readline().decode("utf-8") .strip('\n')
    except:
        pass
    print(temp)
    f.write(datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ") + "," + temp)
    f.flush()
    data = readdata(datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ") + "," + temp)
    print(data)

