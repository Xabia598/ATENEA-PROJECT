from sqlalchemy import create_engine, ForeignKey, Column, String, delete, update, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import random
import ipinfo

access_token = input("Enter IPINFO token: ")
handler = ipinfo.getHandler(access_token)

#=========
#= W.I.P =
#=========

reps = input("How many IPs do you want to scan? - ")

print("PRESS CTRL + C TO STOP")

#ATENEA PROJECT BY XABIA & OMICRON

for i in range(int(reps)):

    iplist = []

    for i in range(4):
        iplist.append(str(random.randint(1, 255)))

    newIP = ".".join(iplist)

    print("New IP: ", newIP)

    details = handler.getDetails(newIP)


    #==========
    #IMPORTANTE
    #==========
    #NUEVOS TIPOS DE DATOS DARAN ERROR EN UNA BASE DE DATOS EXISTENTE!!!

    Base = declarative_base()

    #Se especifican los TIPOS DE DATOS que se van a guardar, "variables" bs
    class Atenea(Base):
        __tablename__ = "atenea"

        ip = Column("IP", String, primary_key=True)
        country = Column("Country", String)
        countrycode = Column("Country Code", String)
        region = Column("Region", String)
        city = Column("City", String)
        latitude = Column("Latitude", String)
        longitude = Column("Longitude", String)

        #Se ponen "APODOS" a las variables
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

print("[SCAN FINISHED]")