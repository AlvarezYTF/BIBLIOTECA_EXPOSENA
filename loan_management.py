# loan_management.py
from datetime import datetime
from tabulate import tabulate
from utils import truncar_texto, save_data
from book_management import leer_libro
def presta_libros(usuario_buscado, data):
    db = data['db']
    prestamos = data['prestamos']
    devoluciones = data['devoluciones']
    fecha_actual = datetime.today().date()

    while True:
        print("1. Hacer préstamo")
        print("2. Hacer devolución")
        print("3. Ver préstamos")
        print("4. Atrás")

        try:
            solicitud_usuario = int(input("\033[35mQué procedimiento deseas hacer: \033[0m"))
            match solicitud_usuario:
                case 1:
                    leer_libro(db, data['categorias'])
                    prestamo_usuario = int(input("\033[35mEscoge el id del libro que pedirá prestado: \033[0m"))
                    prestamo_usuario_cantidad = int(input("\033[35mLa cantidad que pedirá prestado: \033[0m"))
                    prestamo(db, prestamos, prestamo_usuario, fecha_actual, usuario_buscado, prestamo_usuario_cantidad)
                case 2:
                    ver_prestamos_usuario(prestamos, usuario_buscado)
                    id_prestamo = int(input("\033[35mIngresa el ID del préstamo que vas a devolver: \033[0m"))
                    devolucion(db, prestamos, devoluciones, id_prestamo, usuario_buscado, fecha_actual)
                case 3:
                    ver_prestamos_usuario(prestamos, usuario_buscado)
                case 4:
                    save_data(data)
                    return
                case _:
                    print()
                    print("\033[31mOpción no válida\033[0m")
                    print()
        except ValueError:
            print()
            print("\033[31mValor no válido\033[0m")
            print()

def prestamo(db, prestamos, id_usuario, fecha, usuario_buscado, prestamo_usuario_cantidad):
    encontrado = False
    for libro in db:
        if id_usuario == libro["Id"]:
            if libro["Cantidad"] >= prestamo_usuario_cantidad:
                libro["Cantidad"] -= prestamo_usuario_cantidad
                print(f"\033[32mPréstamo exitoso, quedan {libro['Cantidad']} unidades disponibles\033[0m")
                nuevo_prestamo = {
                    "Id": (len(prestamos) + 1),
                    "Nombre": usuario_buscado,
                    "nombre_libro": libro["Nombre"],
                    "cantidad": prestamo_usuario_cantidad,
                    "fecha_prestamo": str(fecha)
                }
                prestamos.append(nuevo_prestamo)
                print(f"\033[32mLibro retirado el {fecha}\033[0m")
            else:
                print("\033[31mNo hay unidades suficientes para el préstamo\033[0m")
            encontrado = True
            break
    
    if not encontrado:
        print("\033[31mError: Libro no encontrado\033[0m")

def ver_prestamos_usuario(prestamos, usuario_buscado):
    datos = []
    encabezados = ["Id", "Nombre Usuario", "Nombre libro", "Cantidad", "Fecha"]

    prestamos_usuario = [p for p in prestamos if p["Nombre"] == usuario_buscado]
    
    if prestamos_usuario:
        for p in prestamos_usuario:
            datos.append([
                p['Id'],
                truncar_texto(p['Nombre']),
                p['nombre_libro'],
                p['cantidad'],
                p['fecha_prestamo']
            ])
        print(tabulate(datos, headers=encabezados, tablefmt="pretty"))
    else:
        print("\033[31mNo hay préstamos para este usuario\033[0m")

def devolucion(db, prestamos, devoluciones, id_prestamo, nombre_buscado, fecha):
    prestamo = next((p for p in prestamos if p["Id"] == id_prestamo and p["Nombre"] == nombre_buscado), None)
    
    if not prestamo:
        print("\033[31mError: No se encontró el préstamo.\033[0m")
        return

    libro = next((l for l in db if l["Nombre"] == prestamo["nombre_libro"]), None)
    
    if not libro:
        print("\033[31mError: No se encontró el libro en la base de datos.\033[0m")
        return

    cantidad_devolucion = int(input("Elige la cantidad de libros que deseas devolver: "))
    
    if cantidad_devolucion <= prestamo["cantidad"]:
        nueva_devolucion = {
            "id": len(devoluciones) + 1,
            "nombre_usuario": prestamo["Nombre"],
            "nombre_libro": libro["Nombre"],
            "cantidad devuelta": cantidad_devolucion,
            "fecha devuelta": str(fecha)
        }
        devoluciones.append(nueva_devolucion)
        
        libro["Cantidad"] += cantidad_devolucion
        prestamo["cantidad"] -= cantidad_devolucion
        
        print(f"\033[32mLibro devuelto el {fecha}\033[0m")
        
        if prestamo["cantidad"] == 0:
            prestamos.remove(prestamo)
    else:
        print("\033[31mError: No puedes devolver más libros de los que tienes prestados.\033[0m")