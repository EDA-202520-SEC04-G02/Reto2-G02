import sys

# Importaciones necesarias
import App.logic as logic # Portar logic porque, pues muy dificil sin logic no?
from tabulate import tabulate # Para imprimir tablas bonitas
import os
data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'
# -------------------------------------------------

def new_logic():
    """
        Se crea una instancia del controlador
    """
    #TODO DONE: Llamar la función de la lógica donde se crean las estructuras de datos
    control = logic.new_logic()
    return control

def load_data(control): # Note que control es el catalog en view
    """
    Carga los datos
    """
    taxisfile = data_dir + "taxis-large.csv"           # Contruimos las rutas de los archivos aquí
    neighfile = data_dir + "nyc-neighborhoods.csv"     # Así no hay que importarlos en logic, que es más limpio
    #TODO DONE: Realizar la carga de datos
    resultados = logic.load_data(control, taxisfile, neighfile) # Ahora si me voy a logic a cargar los datos, retorno los resultados
    
    print("\n=== Resultados de la carga de datos ===")
    print(f"Tiempo de carga: {resultados['time_ms']:.2f} ms")
    print(f"Total de trayectos cargados: {resultados['total_trips']}")

    # Trayecto mínimo
    min_t = resultados["min_trip"]
    print("\nTrayecto de menor distancia (>0):")
    print(f"Inicio: {min_t['pickup_datetime']} | Distancia: {min_t['trip_distance']} millas | Total: {min_t['total_amount']} USD")

    # Trayecto máximo
    max_t = resultados["max_trip"]
    print("\nTrayecto de mayor distancia:")
    print(f"Inicio: {max_t['pickup_datetime']} | Distancia: {max_t['trip_distance']} millas | Total: {max_t['total_amount']} USD")

    # Preview
    print("\nPrimeros y últimos 5 trayectos:")
    headers = ["pickup_datetime", "dropoff_datetime", "duration_min", "distance_miles", "total_amount"]
    table = [[p[h] for h in headers] for p in resultados["preview"]] # Con ayuda de char hicimos esta lista de listas para poder usar tabulate
    print(tabulate(table, headers=headers, tablefmt="grid"))
    return resultados


def print_menu():
    print("Bienvenido")
    print("0- Cargar información")
    print("1- Ejecutar Requerimiento 1")
    print("2- Ejecutar Requerimiento 2")
    print("3- Ejecutar Requerimiento 3")
    print("4- Ejecutar Requerimiento 4")
    print("5- Ejecutar Requerimiento 5")
    print("6- Ejecutar Requerimiento 6")
    print("7- Salir")

def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO NO HACER: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO DONE: Imprimir el resultado del requerimiento 1
    fecha_ini = input("Ingrese la fecha y hora inicial (YYYY-MM-DD HH:MM:SS): ")
    fecha_fin = input("Ingrese la fecha y hora final (YYYY-MM-DD HH:MM:SS): ")
    N = int(input("Ingrese el tamaño de la muestra N: "))

    resultado = logic.req_1(control, fecha_ini, fecha_fin, N)

    print("\n=== Requerimiento 1 ===")
    print(f"Tiempo de ejecución: {resultado['time_ms']:.2f} ms")
    print(f"Total de trayectos en franja: {resultado['total']}")

    headers = ["pickup_datetime", "pickup_location", "dropoff_datetime", "dropoff_location", "trip_distance", "total_amount"]

    def format_trip(trip):
        return [
            trip["pickup_datetime"],
            [float(trip["pickup_latitude"]), float(trip["pickup_longitude"])],
            trip["dropoff_datetime"],
            [float(trip["dropoff_latitude"]), float(trip["dropoff_longitude"])],
            float(trip["trip_distance"]),
            float(trip["total_amount"])
        ]

    primeros = [format_trip(trip) for trip in resultado["primeros"]["elements"]]
    ultimos = [format_trip(trip) for trip in resultado["ultimos"]["elements"]]

    print("\nPrimeros N trayectos:")
    print(tabulate(primeros, headers=headers, tablefmt="grid"))

    print("\nÚltimos N trayectos:")
    print(tabulate(ultimos, headers=headers, tablefmt="grid"))


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO DONE: Imprimir el resultado del requerimiento 5
    
    fecha_hora = input("Ingrese la fecha y hora de terminación (YYYY-MM-DD HH): ")
    N = int(input("Ingrese el tamaño de la muestra N: "))

    resultado = logic.req_5(control, fecha_hora, N)

    print("\n=== Requerimiento 5 ===")
    print(f"Tiempo de ejecución: {resultado['tiempo_ms']:.2f} ms")
    print(f"Total de trayectos con fecha y hora de terminación {fecha_hora}: {resultado['total']}")

    # No hay resultados
    if resultado["total"] == 0:
        print("\nNo se encontraron trayectos para la fecha y hora especificadas.")
        return

    headers = [
        "pickup_datetime", 
        "pickup_location", 
        "dropoff_datetime", 
        "dropoff_location", 
        "trip_distance", 
        "total_amount"
    ]

    def format_trip(trip):
        return [
            trip["pickup_datetime"],
            [float(trip["pickup_latitude"]), float(trip["pickup_longitude"])],
            trip["dropoff_datetime"],
            [float(trip["dropoff_latitude"]), float(trip["dropoff_longitude"])],
            float(trip["trip_distance"]),
            float(trip["total_amount"])
        ]

    primeros = [format_trip(trip) for trip in resultado["primeros"]["elements"]]
    ultimos = [format_trip(trip) for trip in resultado["ultimos"]["elements"]]

    print("\nPrimeros N trayectos:")
    print(tabulate(primeros, headers=headers, tablefmt="grid"))

    print("\nÚltimos N trayectos:")
    print(tabulate(ultimos, headers=headers, tablefmt="grid"))



def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO DONE: Imprimir el resultado del requerimiento 6
    # Solicitar parámetros al usuario
    barrio = input("Ingrese el nombre del barrio de recogida: ")
    hora_ini = input("Ingrese la hora inicial del rango (HH): ")
    hora_fin = input("Ingrese la hora final del rango (HH): ")
    N = int(input("Ingrese el tamaño de la muestra N: "))

    # Ejecutar el requerimiento
    resultado = logic.req_6(control, barrio, hora_ini, hora_fin, N)

    print("\n=== Requerimiento 6 ===")
    print(f"Tiempo de ejecución: {resultado['tiempo_ms']:.2f} ms")
    print(f"Total de trayectos en {barrio} entre las horas {hora_ini} y {hora_fin}: {resultado['total']}")

    # Definir los encabezados para tabulate
    headers = [
        "pickup_datetime", "pickup_location",
        "dropoff_datetime", "dropoff_location",
        "trip_distance", "total_amount"
    ]

    # Función de formato de cada trayecto
    def format_trip(trip):
        return [
            trip["pickup_datetime"],
            [float(trip["pickup_latitude"]), float(trip["pickup_longitude"])],
            trip["dropoff_datetime"],
            [float(trip["dropoff_latitude"]), float(trip["dropoff_longitude"])],
            float(trip["trip_distance"]),
            float(trip["total_amount"])
        ]

    # Obtener las listas de elementos
    primeros = [format_trip(trip) for trip in resultado["primeros"]["elements"]]
    ultimos = [format_trip(trip) for trip in resultado["ultimos"]["elements"]]

    # Imprimir en formato tabla
    print("\nPrimeros N trayectos:")
    print(tabulate(primeros, headers=headers, tablefmt="grid"))

    print("\nÚltimos N trayectos:")
    print(tabulate(ultimos, headers=headers, tablefmt="grid"))


# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 0:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 1:
            print_req_1(control)

        elif int(inputs) == 2:
            print_req_2(control)

        elif int(inputs) == 3:
            print_req_3(control)

        elif int(inputs) == 4:
            print_req_4(control)

        elif int(inputs) == 5:
            print_req_5(control)

        elif int(inputs) == 6:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
