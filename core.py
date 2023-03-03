from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import random

#=========
#= W.I.P =
#=========

Base = declarative_base()
#==========
#IMPORTANTE
#==========
#NUEVOS TIPOS DE DATOS DARAN ERROR EN UNA BASE DE DATOS EXISTENTE!!!

#Se especifican los TIPOS DE DATOS que se van a guardar, "variables" bs
class Data(Base):
    __tablename__ = "Data"

    ssn = Column("SSN", Integer, primary_key=True)
    firstname = Column("Firstname", String)
    lastname = Column("Lastname", String)
    gender = Column("Gender", CHAR)
    age = Column("Age", Integer)
 
    #Se ponen "APODOS" a las variables
    def __init__(self, ssn, first, last, gender, age):
        self.ssn = ssn
        self.firstname = first
        self.lastname = last
        self.gender = gender
        self.age = age

    def __repr__(self):
        return f"({self.ssn}) {self.firstname} {self.lastname} {self.gender} {self.age}"
    

engine  = create_engine("sqlite:///atenea.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

#PLANTILLA DE DATOS
for x in range(1, 10):
    p1 = Data(random.randint(1, 99999), "DATA", "DATA", "X", random.randint(1, 99999))
    session.add(p1)
    session.commit()

#===FILTRADO DE DATOS===
results = session.query(Data).all()
print("----------------------------------------------")
for r in results:
    print(r)
print("----------------------------------------------")

print("===[GENERACION ACABADA]===")

#RESET TABLE

input("Reiniciar Base De Datos? - [Y/N]")
if input == "Y":
    session.execute(Data.delete())
else:
    if input == "N":
        exit

