from sqlalchemy import create_engine, ForeignKey, Column, String, delete, update, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import random
import requests

#=========
#= W.I.P =
#=========

#ATENEA PROJECT BY XABIA & OMICRON
print("[ONLY 1.000 LOOKUPS]")

for i in range(10):

    iplist = []

    for i in range(4):
        iplist.append(str(random.randint(1, 255)))

    newIP = ".".join(iplist)

    print("New IP: ", newIP)

    #network=input("Enter the IP you want to scan and save:  ")

    req = requests.get(f'https://ipapi.co/{newIP}/json/') #CHANGE TO IPINFO.IO !!!!
    response = req.json()

    #cityData = response.get("city")
    #countryData = response.get("country_name")
    #countryDataCode = response.get("country_code")
    #regionData = response.get("region")
    #regionDataCode = response.get("region_code")
    #zipData = response.get("zip")
    #latitudeData = response.get("latitude")
    #longitudeData = response.get("longitude")

    print(response.get("countryData"))

    # try using req.status_code
    if response.get("countryData") == None:
        print("[INVALID DIRECTION DETECTED] = ", newIP)
        continue

    Base = declarative_base()
    #==========
    #IMPORTANTE
    #==========
    #NUEVOS TIPOS DE DATOS DARAN ERROR EN UNA BASE DE DATOS EXISTENTE!!!


    #Se especifican los TIPOS DE DATOS que se van a guardar, "variables" bs
    class Atenea(Base):
        __tablename__ = "atenea"

        ip = Column("IP", String, primary_key=True)
        country = Column("Country", String)
        countrycode = Column("Country Code", String)
        region = Column("Region", String)
        regioncode = Column("Region Code", String)
        city = Column("City", String)
        zip = Column("Zip", String)
        latitude = Column("Latitude", String)
        longitude = Column("Longitude", String)

        #Se ponen "APODOS" a las variables
        def __init__(self, ip, country, countrycode, region, regioncode, city, zip, latitude, longitude):
            self.ip = ip
            self.country = country
            self.countrycode = countrycode
            self.region = region
            self.regioncode = regioncode
            self.city = city
            self.zip = zip
            self.latitude = latitude
            self.longitude = longitude

        def __repr__(self):
            return f"({self.ip}) {self.country} {self.countrycode} {self.region} {self.regioncode} {self.city} {self.zip} {self.latitude} {self.longitude})"


    engine  = create_engine("sqlite:///atenea.db", echo=True)
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    delete(Atenea).where(Atenea.country == None)
    update(Atenea)

    #GUARDADO DE DATOS
    newdata = Atenea(newIP, 
                    response["countryData"],
                    response["countryDataCode"],
                    response["regionData"],
                    response["regionDataCode"],
                    response["cityData"],
                    response["zipData"],
                    response["latitudeData"],
                    response["longitudeData"]
                )
    session.add(newdata)
    session.commit()
