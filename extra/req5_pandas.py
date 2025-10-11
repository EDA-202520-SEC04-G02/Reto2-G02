import os
import pandas as pd
data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'
# Ruta a tu archivo CSV
# cámbiala si lo tienes en otra carpeta
path = data_dir + "taxis-large.csv"

# Leer los datos
df = pd.read_csv(path, low_memory=False)

# Convertir las columnas a datetime
df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"], errors="coerce")
df["dropoff_datetime"] = pd.to_datetime(df["dropoff_datetime"], errors="coerce")

# Filtro: fecha y hora de terminación
target = "2015-01-04 12"
mask = df["dropoff_datetime"].dt.strftime("%Y-%m-%d %H") == target
filtered = df.loc[mask].copy()

# Orden descendente por hora de terminación
filtered = filtered.sort_values(by="dropoff_datetime", ascending=False)

# Tamaño total y muestras
N = 3
total = len(filtered)
primeros = filtered.head(N)
ultimos = filtered.tail(N)

print(f"Total de trayectos con fecha y hora de terminación {target}: {total}\n")

print("\nPrimeros N trayectos:")
print(primeros[[
    "pickup_datetime",
    "pickup_latitude", "pickup_longitude",
    "dropoff_datetime",
    "dropoff_latitude", "dropoff_longitude",
    "trip_distance", "total_amount"
]])

print("\nÚltimos N trayectos:")
print(ultimos[[
    "pickup_datetime",
    "pickup_latitude", "pickup_longitude",
    "dropoff_datetime",
    "dropoff_latitude", "dropoff_longitude",
    "trip_distance", "total_amount"
]])
