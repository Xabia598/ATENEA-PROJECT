# MADE BY XABIA598 AND OMICRON166
import sqlite3

print("CTRL + C TO EXIT")

conn = sqlite3.connect('atenea.db')

c = conn.cursor()

mode = input("Country | City | IP :: ")

if mode == "Country":

    def search():

        target = input("Enter Country Name (In English) :: ")
        cursor = conn.execute(f"SELECT * FROM Atenea WHERE Country = '{target}'")

        for row in cursor:
            print(row)

    while True:
        search()
    
else:
    if mode == "City":
        def search():

            target = input("Enter City Name (In English) :: ")
            cursor = conn.execute(f"SELECT * FROM Atenea WHERE City = '{target}'")

            for row in cursor:
                print(row)

        while True:
            search()
    
    else:
        def search():

            target = input("Enter IP :: ")
            cursor = conn.execute(f"SELECT * FROM Atenea WHERE IP = '{target}'")

            for row in cursor:
                print(row)

        while True:
            search()
