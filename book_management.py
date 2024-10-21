# book_management.py
from tabulate import tabulate
from utils import truncar_texto, save_data

def biblioteca(data):
    db = data['db']
    categorias = data['categorias']
    print()
    print("\033[34mBIENVENIDO AL SISTEMA DE BIBLIOTECA\033[0m")
    while True:
        print()
        print("1. Crear libro")
        print("2. Catálogo de libros")
        print("3. Editar libro")
        print("4. Eliminar libro")
        print("5. Ver préstamos")
        print("6. Ver devoluciones")
        print("7. Crear categoría")
        print("8. Atrás")
        print()
        try:
            opcion = int(input("\033[35mEscoge una opción: \033[0m"))
            match opcion:
                case 1:
                    crear_libro(db, categorias)
                case 2:
                    leer_libro(db, categorias)
                case 3:
                    leer_libro(db, categorias)
                    id_buscar = int(input("\033[35mIngrese el ID del libro que desea actualizar: \033[0m"))
                    actualizar_libro(db, id_buscar)
                case 4:
                    leer_libro(db, categorias)
                    id_libro = int(input("\033[35mID del libro: \033[35m"))
                    eliminar_libro(db, id_libro)
                case 5:
                    ver_prestamos(data['prestamos'])
                case 6:
                    ver_devoluciones(data['devoluciones'])
                case 7:
                    crear_categoria(categorias)
                case 8:
                    save_data(data)
                    return
        except ValueError:
            print()
            print("\033[31mValor no válido\033[0m")
            print()
            print("Por favor vuelva a intentarlo")

def crear_libro(db, categorias):
    nombre_libro = input("\033[35mIngrese el nombre del libro: \033[0m")
    autor_libro = input("\033[35mIngrese el nombre del autor: \033[0m")
    cantidad_libro = int(input("\033[35mIngrese la cantidad de libros: \033[0m"))
    for i, categoria in enumerate(categorias, 1):
        print(f"{i}: {categoria}")
    categoria_libro = int(input("\033[35mIngrese el número de la categoría: \033[0m"))
    categoria = categorias[categoria_libro - 1]
    
    if db:
        max_id = max(libro["Id"] for libro in db)
        nuevo_id = max_id + 1
    else:
        nuevo_id = 1

    if not nombre_libro:
        print("\033[31mError: El nombre del libro es obligatorio.\033[0m")
        return
    if not autor_libro:
        print("\033[31mError: El autor del libro es obligatorio.\033[0m")
        return
    if not cantidad_libro > 0:
        print("\033[31mError: la cantidad del libro no puede ser negativa.\033[0m")
        return

    libro = {"Id": nuevo_id, "Nombre": nombre_libro, "Autor": autor_libro, "Cantidad": cantidad_libro, "Categoria": categoria}
    db.append(libro)
    print()
    print("\033[42mLibro creado exitosamente.\033[0m")
    print()

def leer_libro(db, categorias):
    print("1. Ver por categorías")
    print("2. Ver todos los libros")
    opcion = int(input("Escoge la opción: "))
    match opcion:
        case 1:
            ver_categorias(db, categorias)
        case 2:
            mostrar_todos_libros(db)
        case _:
            print("Número no válido")
            print()

def ver_categorias(db, categorias):
    print()
    print("\033[34mCATEGORÍAS\033[0m")
    print()
    for i, categoria in enumerate(categorias, 1):
        print(f"{i}. {categoria}")
    categoria_buscar = int(input("Escoge el número de la categoría que deseas ver: ")) - 1
    categoria_buscar = categorias[categoria_buscar]
    datos = []

    print("\033[34mCATÁLOGO DE LIBROS\033[0m")
    encabezados = ["Id", "Nombre Libro", "Autor", "Cantidad", "Categoría"]

    try:
        for libro in db:
            if libro["Categoria"] == categoria_buscar:
                datos.append([
                    libro['Id'],
                    truncar_texto(libro['Nombre']),
                    libro['Autor'],
                    libro["Cantidad"],
                    libro["Categoria"]
                ])
        print(tabulate(datos, headers=encabezados, tablefmt="pretty"))
    except:
        print("Error")

def mostrar_todos_libros(db):
    datos = []
    print("\033[34mCATÁLOGO DE LIBROS\033[0m")
    encabezados = ["Id", "Nombre Libro", "Autor", "Cantidad", "Categoría"]
    for libro in db:
        datos.append([
            libro['Id'],
            truncar_texto(libro['Nombre']),
            libro['Autor'],
            libro["Cantidad"],
            libro["Categoria"]
        ])
    print(tabulate(datos, headers=encabezados, tablefmt="pretty"))

# book_management.py (continuación)

def actualizar_libro(db, id):
    libro_encontrado = next((libro for libro in db if libro["Id"] == id), None)
    if libro_encontrado:
        print()
        print("\033[42mLibro encontrado:\033[0m")
        print()
        print(libro_encontrado)
        print()
        print("\033[35m¿Qué desea cambiar?\033[0m")
        print("1. Editar nombre")
        print("2. Editar autor")
        print("3. Editar cantidad")
        print("4. Atrás")
        
        try:
            opcion_editar = int(input("\033[35mIngrese la opción: \033[0m"))
            match opcion_editar:
                case 1:
                    nuevo_nombre = input("\033[35mIngrese el nuevo nombre del libro: \033[0m")
                    libro_encontrado["Nombre"] = nuevo_nombre
                    print("\033[42mNombre actualizado correctamente.\033[0m")
                case 2:
                    nuevo_autor = input("\033[35mIngrese el nuevo autor del libro: \033[0m")
                    libro_encontrado["Autor"] = nuevo_autor
                    print("\033[42mAutor actualizado correctamente.\033[0m")
                case 3:
                    while True:
                        try:
                            nueva_cantidad = int(input("\033[35mIngrese la nueva cantidad de libros: \033[0m"))
                            if nueva_cantidad > 0:
                                libro_encontrado["Cantidad"] = nueva_cantidad
                                print("\033[42mCantidad actualizada correctamente.\033[0m")
                                break
                            else:
                                print("\033[31mLa cantidad debe ser un número mayor que 0.\033[0m")
                        except ValueError:
                            print("\033[31mDebe ingresar un número válido para la cantidad.\033[0m")
                case 4:
                    print("\033[42mSaliendo de la edición...\033[0m")
                    return
                case _:
                    print("\033[31mOpción no válida\033[0m")
        except ValueError:
            print("\033[31mValor no válido\033[0m")
            print("\033[35mPor favor vuelva a intentarlo\033[0m")
    else:
        print("\033[31mNo se encontró un libro con el ID proporcionado.\033[0m")

def eliminar_libro(db, id_libro):
    libro = next((l for l in db if l["Id"] == id_libro), None)
    if not libro:
        print("\033[41mError: No se encontró el libro con el ID proporcionado.\033[0m")
        return

    motivos_eliminar = [
        "No deseo eliminar el libro",
        "Deterioro físico",
        "Obsolescencia",
        "Poca circulación",
        "Perdido"
    ]

    print("\033[35m¿Por qué desea eliminar el libro?\033[0m")
    print()

    for indice, motivo in enumerate(motivos_eliminar, start=1):
        print(f"{indice}: {motivo}")

    try:
        print()
        opcion_usuario = int(input("\033[35mIngrese el número del motivo: \033[0m"))
        print()

        if opcion_usuario == 1:
            print("\033[33mOperación cancelada, el libro no fue eliminado.\033[0m")
            return
        elif 2 <= opcion_usuario <= len(motivos_eliminar):
            cantidad_libro_eliminar = int(input("Ingrese la cantidad de libros a eliminar: "))
            if cantidad_libro_eliminar <= libro["Cantidad"]:
                libro["Cantidad"] -= cantidad_libro_eliminar
                print(f"\033[42mDel libro: {libro['Nombre']} .\033[0m")
                print(f"\033[42mSe ha eliminado la siguiente cantidad: {cantidad_libro_eliminar} .\033[0m")
                print(f"\033[42mPor: {motivos_eliminar[opcion_usuario - 1]} .\033[0m")
            elif cantidad_libro_eliminar > libro["Cantidad"]:
                print()
                print("\033[41mCantidad solicitada excede el stock disponible para el libro seleccionado.\033[0m")
        else:
            print("\033[41mAcaba de ingresar un número no válido.\033[0m")
            print("\033[35mPor favor, vuelva a intentarlo.\033[0m")
    except ValueError:
        print("\033[41mAcaba de ingresar una opción no válida.\033[0m")
        print("\033[35mPor favor, vuelva a intentarlo.\033[0m")

def crear_categoria(categorias):
    nueva_categoria = input("Ingresa la nueva categoría: ")
    categorias.append(nueva_categoria)
    print(f"\033[32mCategoría '{nueva_categoria}' creada exitosamente.\033[0m")
    print("Categorías actualizadas:", categorias)

def ver_prestamos(prestamos):
    if not prestamos:
        print("\033[33mNo hay préstamos registrados.\033[0m")
        return
    
    print("\033[34mLISTA DE PRÉSTAMOS\033[0m")
    for prestamo in prestamos:
        print()  # Línea separadora
        print(f"Id: {prestamo['Id']}")
        print(f"Usuario: {prestamo['Nombre']}")
        print(f"Libro: {prestamo['nombre_libro']}")
        print(f"Cantidad: {prestamo['cantidad']}")
        print(f"Fecha: {prestamo['fecha_prestamo']}")

def ver_devoluciones(devoluciones):
    if not devoluciones:
        print("\033[33mNo hay devoluciones registradas.\033[0m")
        return
    
    print("\033[34mLISTA DE DEVOLUCIONES\033[0m")
    for devolucion in devoluciones:
        print()  # Línea separadora
        print(f"Id: {devolucion['id']}")
        print(f"Usuario: {devolucion['nombre_usuario']}")
        print(f"Libro: {devolucion['nombre_libro']}")
        print(f"Cantidad: {devolucion['cantidad devuelta']}")
        print(f"Fecha: {devolucion['fecha devuelta']}")