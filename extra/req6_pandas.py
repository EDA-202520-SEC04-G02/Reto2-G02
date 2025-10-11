import os
import pandas as pd
import numpy as np
import time

# === Paths ===
data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'
path_trips = data_dir + "taxis-large.csv"
path_neigh = data_dir + "nyc-neighborhoods.csv"

# === Parámetros del requerimiento ===
barrio_objetivo = "Midtown"
hora_ini, hora_fin = 9, 12
N = 3

# === Cargar datos ===
print("Cargando datos...")
df = pd.read_csv(path_trips, low_memory=False)
neigh = pd.read_csv(path_neigh, sep=";")

# === Preparar coordenadas de barrios ===
neigh["latitude_f"] = neigh["latitude"].astype(str).str.replace(",", ".").astype(float)
neigh["longitude_f"] = neigh["longitude"].astype(str).str.replace(",", ".").astype(float)
neigh_lat_rad = np.radians(neigh["latitude_f"].values)
neigh_lon_rad = np.radians(neigh["longitude_f"].values)
neigh_names = neigh["neighborhood"].values

# === Vectorized Haversine en bloques ===
def nearest_neighborhoods_vectorized(df, neigh_lat_rad, neigh_lon_rad, neigh_names, chunk_size=5000):
    n = len(df)
    result = np.empty(n, dtype=object)
    lat_arr = pd.to_numeric(df["pickup_latitude"], errors="coerce").values
    lon_arr = pd.to_numeric(df["pickup_longitude"], errors="coerce").values
    R = 3959.0  # millas

    for start in range(0, n, chunk_size):
        end = min(n, start + chunk_size)
        lat_chunk = lat_arr[start:end]
        lon_chunk = lon_arr[start:end]
        valid = (~np.isnan(lat_chunk)) & (~np.isnan(lon_chunk))
        if valid.sum() == 0:
            result[start:end] = None
            continue

        lat_r = np.radians(lat_chunk[valid])
        lon_r = np.radians(lon_chunk[valid])
        dlat = neigh_lat_rad[None, :] - lat_r[:, None]
        dlon = neigh_lon_rad[None, :] - lon_r[:, None]

        a = np.sin(dlat / 2.0) ** 2 + np.cos(lat_r)[:, None] * np.cos(neigh_lat_rad)[None, :] * np.sin(dlon / 2.0) ** 2
        c = 2.0 * np.arcsin(np.sqrt(np.minimum(1.0, a)))
        dists = R * c
        idx_min = np.argmin(dists, axis=1)
        result_block = neigh_names[idx_min]

        tmp = np.empty(end - start, dtype=object)
        tmp[:] = None
        tmp[valid] = result_block
        result[start:end] = tmp

    return result

# === Calcular barrios cercanos y filtrar ===
print("Asignando barrios por chunks (vectorizado)...")
t0 = time.time()
df["nearest_neigh"] = nearest_neighborhoods_vectorized(df, neigh_lat_rad, neigh_lon_rad, neigh_names)
t1 = time.time()
print(f"Tiempo en asignar barrios: {(t1 - t0):.2f} s")

# === Filtrar por barrio y rango horario ===
df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"], errors="coerce")
df["hour"] = df["pickup_datetime"].dt.hour

df_filtrado = df[
    (df["nearest_neigh"] == barrio_objetivo) &
    (df["hour"] >= hora_ini) &
    (df["hour"] <= hora_fin)
].sort_values(by="pickup_datetime", ascending=True)

# === Mostrar resultados ===
total = len(df_filtrado)
primeros = df_filtrado.head(N)
ultimos = df_filtrado.tail(N)

print(f"\nTotal de trayectos en {barrio_objetivo} entre {hora_ini}:00 y {hora_fin}:00 → {total}\n")

cols = [
    "pickup_datetime", "pickup_latitude", "pickup_longitude",
    "dropoff_datetime", "dropoff_latitude", "dropoff_longitude",
    "trip_distance", "total_amount"
]

print("Primeros N trayectos:")
print(primeros[cols])

print("\nÚltimos N trayectos:")
print(ultimos[cols])
