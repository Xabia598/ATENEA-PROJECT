import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
import matplotlib.pyplot as plt
from geopandas import GeoDataFrame

df = pd.read_csv("atenea.csv", delimiter=',')

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]

gdf = GeoDataFrame(df, geometry=geometry)

world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
cities = gpd.read_file(gpd.datasets.get_path("naturalearth_cities"))

fig, ax = plt.subplots(figsize=(10, 5))

world.plot(ax=ax, color="lightgray", edgecolor="white")
cities.plot(ax=ax, marker="*", color="red", markersize=16, label="Cities")

gdf.plot(ax=ax, marker=".", color="blue", markersize=8, label="Data Locations")

ax.legend()

plt.title("LOCATION OF OBTAINED DATA")
plt.show()