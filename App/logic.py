import time

# Imports necesarios
import csv # Para cargar los datos
from DataStructures.List import array_list as lt # Importo mi implementación de lista para guardar la información
csv.field_size_limit(2147483647) # Consejo de la guía
from datetime import datetime # Importamos datetime, porque es MUCHO MEJOR para manejar fechas que hacer todo a mano
import math
# -----------------------------------------

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    #TODO DONE: Llama a las funciónes de creación de las estructuras de datos
    catalog = {
        "trips": None,          # Lista de trayectos
        "neighborhoods": None   # Lista de barrios
    }
    
    catalog["trips"] = lt.new_list()
    catalog["neighborhoods"] = lt.new_list()
    
    return catalog


# Funciones para la carga de datos

def load_data(catalog, taxisfile, neighfile):
    """
    Carga los datos del reto
    """
    # TODO DONE: Realizar la carga de datos
    
    # iniciar tiempo
    start = get_time()

    # Cargar trayectos
    with open(taxisfile, encoding="utf-8") as f:
        input_file = csv.DictReader(f)
        for row in input_file:
            lt.add_last(catalog["trips"], row) # Agrego cada fila como un dict a la lista

    # Cargar barrios
    with open(neighfile, encoding="utf-8") as f:
        input_file = csv.DictReader(f, delimiter=";") # Esta carga de datos tiene la peculiaridad que usa ; como separador
        for row in input_file:
            lt.add_last(catalog["neighborhoods"], row) # Agrego cada fila como un dict a la lista

    # Procesar min/max y preview, se hizo con funciones externas
    min_trip, max_trip = find_min_max_trip(catalog["trips"])
    
    # Formatear preview con tabulate
    preview = get_preview_trips(catalog["trips"], 5)

    # parar tiempo
    end = get_time()
    delta = delta_time(start, end)

    return {
        "time_ms": delta,
        "total_trips": lt.size(catalog["trips"]),
        "min_trip": min_trip,
        "max_trip": max_trip,
        "preview": preview
    }

# Funciones de ayuda

def trip_duration_minutes(trip): # Esta función nos ayuda a sacar la diferencia de fechas
    """
    Calcula la duración en minutos de un trayecto
    """
    fmt = "%Y-%m-%d %H:%M:%S" # Formato de las fechas en el csv
    if "pickup_datetime" in trip and "dropoff_datetime" in trip: # If para entrar a las fechas de un trip en específico
        pickup = datetime.strptime(trip["pickup_datetime"], fmt)
        dropoff = datetime.strptime(trip["dropoff_datetime"], fmt)
        return (dropoff - pickup).total_seconds() / 60 # Diferencia en minutos
    else:
        return 0.0 # Por si acaso?


def find_min_max_trip(trips):
    """
    Encuentra el trayecto de menor y mayor distancia (distancia > 0)
    """
    min_trip = None
    max_trip = None
    size = lt.size(trips)
    for i in range(size): # Iteramos sobre cada viaje
        t = lt.get_element(trips, i) # accedemos a la información del viaje
        dist = float(t["trip_distance"]) # sacamos la distancia
        if dist > 0: # Entramos a comparar solo si la distancia es mayor a 0
            if min_trip is None or dist < float(min_trip["trip_distance"]): # Este primer if me da la distancia mínima, y va guardando el que cumpla la desigualdad
                min_trip = t
            if max_trip is None or dist > float(max_trip["trip_distance"]): # Misma idea pero con la otra desigualdad, así se puede hacer O(n)
                max_trip = t
    return min_trip, max_trip # DEvolvemos ambos viajes


def get_preview_trips(trips, n=5): # Función para hacer el preview con tabulate
    """
    Retorna los primeros y últimos n trayectos con los campos requeridos
    """
    preview = []
    size = lt.size(trips)

    # Primeros n
    for i in range(min(n, size)):
        t = lt.get_element(trips, i)
        preview.append(format_trip(t)) # Guardamos los primeros 5

    # Últimos n
    for i in range(max(size - n, 0), size):
        t = lt.get_element(trips, i)
        preview.append(format_trip(t)) # Guardamos los últimos 5

    return preview

def format_trip(t): # Formato según requerimientos
    """
    Formatea un trayecto en dict con solo los campos necesarios
    """
    return {
        "pickup_datetime": t["pickup_datetime"],
        "dropoff_datetime": t["dropoff_datetime"],
        "duration_min": round(trip_duration_minutes(t), 2),
        "distance_miles": float(t["trip_distance"]),
        "total_amount": float(t["total_amount"])
    }
    
def find_nearest_neighborhood(neigh_list, lat, lon):
    """
    Encuentra el barrio más cercano a un punto (lat, lon) usando la lista de centroides de barrios
    """
    size = lt.size(neigh_list)
    nearest_name = None
    min_dist = None  # empezamos sin valor

    for i in range(size):
        neigh = lt.get_element(neigh_list, i)
        nlat = float(neigh["latitude"].replace(",", ".")) # NO MÁS COMAS, ARRIBA LOS PUNTOS!
        nlon = float(neigh["longitude"].replace(",", "."))
        dist = haversine(lat, lon, nlat, nlon) # Uso la función recomendada para sacar la distancia entre los puntos

        if min_dist is None or dist < min_dist:
            min_dist = dist
            nearest_name = neigh["neighborhood"]

    return nearest_name
    
def haversine(lat1, lon1, lat2, lon2): # Esto es literal sacado de wikipedia básicamente
    """
    Calcula la distancia haversine en kilómetros entre dos puntos
    """
    R = 3959  # radio de la Tierra en mi
    # Hay que importar ¡math!
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c # Note que se usa un radio de la tierra  sin decimales, no vamos a tener tanta precisión

# Funciones de consulta sobre el catálogo

def get_data(catalog, id):
    """
    Retorna un dato por su ID.
    """
    #TODO NO HACER: Consulta en las Llamar la función del modelo para obtener un dato
    pass

def req_1(catalog, fecha_ini, fecha_fin, N):    
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO DONE: Modificar el requerimiento 1
    start = get_time()
    fmt = "%Y-%m-%d %H:%M:%S"
    fecha_ini = datetime.strptime(fecha_ini, fmt)
    fecha_fin = datetime.strptime(fecha_fin, fmt)

    # 1. Filtrar
    filtrados = lt.new_list()
    for i in range(lt.size(catalog["trips"])):
        trip = lt.get_element(catalog["trips"], i)
        pickup = datetime.strptime(trip["pickup_datetime"], fmt)
        if fecha_ini <= pickup <= fecha_fin:
            lt.add_last(filtrados, trip)

    # 2. Ordenar por pickup_datetime ascendente
    def sort_criteria(t1, t2):
        d1 = datetime.strptime(t1["pickup_datetime"], fmt)
        d2 = datetime.strptime(t2["pickup_datetime"], fmt)
        return d1 < d2

    filtrados = lt.merge_sort(filtrados, sort_criteria)

    total = lt.size(filtrados)

    # 3. N primeros y últimos (sin formatear)
    primeros = lt.sub_list(filtrados, 0, min(N, total))
    ultimos = lt.sub_list(filtrados, max(0, total - N), min(N, total))

    end = get_time()
    delta = delta_time(start, end)

    return {
        "time_ms": delta,
        "total": total,
        "primeros": primeros,
        "ultimos": ultimos
    }


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
