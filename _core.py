from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import random
import ipinfo
import ipaddress
import time
import csv

ipscan = 0
notvalidips = 0

access_token = input("Enter IPINFO token: ")
handler = ipinfo.getHandler(access_token)

#=========
#= W.I.P =
#=========

reps = input("How many IPs do you want to scan? - ")

print("PRESS CTRL + C TO STOP")

def validateip(ip_string):
    try:
        ipaddress.ip_address(ip_string)
        return
    except:
        pass    


for i in range(int(reps)):

    iplist = []

    for i in range(4):
        iplist.append(str(random.randint(1, 255)))

    newIP = ".".join(iplist)

    print("New IP: ", newIP)

    details = handler.getDetails(newIP)

    validateip(newIP)

    Base = declarative_base()


    class Atenea(Base):
        __tablename__ = "atenea"

        ip = Column("IP", String, primary_key=True)
        country = Column("Country", String)
        countrycode = Column("Country Code", String)
        region = Column("Region", String)
        city = Column("City", String)
        latitude = Column("Latitude", String)
        longitude = Column("Longitude", String)

        def __init__(self, ip, country, countrycode, region, city, latitude, longitude):
            self.ip = ip
            self.country = country
            self.countrycode = countrycode
            self.region = region
            self.city = city
            self.latitude = latitude
            self.longitude = longitude

        def __repr__(self):
            return f"({self.ip}) {self.country} {self.countrycode} {self.region} {self.city} {self.latitude} {self.longitude})"


    engine  = create_engine("sqlite:///atenea.db", echo=True)
    Base.metadata.create_all(bind=engine)


    Session = sessionmaker(bind=engine)
    session = Session()
    
    if "bogon" in details.all:
        print("Not valid IP")
        print("What the actual fuck are you doing in my database")

        notvalidips = notvalidips + 1
        continue
    else:
        print("Valid IP")

    #GUARDADO DE DATOS
    newdata = Atenea(newIP, 
                     details.country_name,
                     details.country,
                     details.region,
                     details.city,
                     details.latitude,
                     details.longitude
                )
    
    session.add(newdata)
    session.commit()

    ipscan = ipscan + 1
    
rows = session.query(Atenea).count()

print("[SCAN FINISHED]")
print("==================================================")
print("STATS:")
print("Time Elapsed: ", time.process_time())
print("Total Rows in Database: ", rows)
print("Aprox. Values: ", rows * 7)
print("Valid IPs Scanned: ", ipscan)
print("Not Valid IPs: ", notvalidips)
print("==================================================")

results = session.query(Atenea).all()

def savedata():
    with open('atenea.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['IP', 'Country', 'Country Code', 'Region', 'City', 'Latitude', 'Longitude'])
        for row in results:
            writer.writerow([row.ip, row.country, row.countrycode, row.region, row.city, row.latitude, row.longitude])

    session.close()

    print("Data saved to 'atenea.csv'")

sd = input("Dump DATA in .csv file? (Can be used for _plot.py) Y/N :: ")

if sd == "Y":
    savedata()
else:
    input("Press any key to quit...")