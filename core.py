from sqlalchemy import create_engine, ForeignKey, Column, String, delete, update, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import random
import requests

#=========
#= W.I.P =
#=========

#ATENEA PROJECT BY XABIA & OMICRON
print("[ONLY 1.000 LOOKUPS] LIMITED!")

for i in range(10):
    
    iplist = []
    newIP = "0.0.0.0"
    
    def generateip():
        for i in range(4):
            iplist.append(random.randint(1, 255))
        
    generateip()
    newIP = ".".join(str(i) for i in iplist)
    iplist.clear()
    
    print("New IP: ", newIP)
    print(iplist)

    #network=input("Enter the IP you want to scan and save:  ")

    ip_address = newIP
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()

    ip = ip_address

    cityData = response.get("city")
    countryData = response.get("country_name")
    countryDataCode = response.get("country_code")
    regionData = response.get("region")
    regionDataCode = response.get("region_code")
    zipData = response.get("zip")
    latitudeData = response.get("latitude")
    longitudeData = response.get("longitude")

    print(countryData)

    if countryData == None:
        print("[INVALID DIRECTION DETECTED] = ", newIP)
        continue
    else:
        pass

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
    newdata = Atenea(ip, countryData, countryDataCode, regionData, regionDataCode, cityData, zipData, latitudeData, longitudeData)
    session.add(newdata)
    session.commit()
    
