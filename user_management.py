# user_management.py
from tabulate import tabulate
from utils import truncar_texto, save_data

def administrar_usuarios(data):
    usuarios = data['usuarios']
    while True:
        print()
        print("\033[34mBIENVENIDO AL SISTEMA DE USUARIOS\033[0m")
        print()
        print("1. Crear usuario")
        print("2. Catálogo de usuarios")
        print("3. Editar usuario")
        print("4. Desactivar usuario")
        print("5. Atrás")
        print()
        print("\033[35mEscoge una opción: \033[0m")
        try:
            opcion = int(input())
            match opcion:
                case 1:
                    crear_usuario(usuarios)
                case 2:
                    leer_usuario(usuarios)
                case 3:
                    leer_usuario(usuarios)
                    id_buscar = int(input("\033[35mIngrese el id del usuario que desea actualizar: \033[0m"))
                    actualizar_usuario(usuarios, id_buscar)
                case 4:
                    desactivar_usuario(usuarios)
                case 5:
                    save_data(data)
                    return
        except ValueError:
            print("Ingresó un valor no válido")
            print("Por favor vuelva a intentarlo")

def crear_usuario(usuarios):
    usuario_nuevo = input("\033[35mIngrese el nombre del usuario: \033[0m")
    contrasena = input("\033[35mIngrese la contraseña del usuario: \033[0m")
    if not usuario_nuevo:
        print("\033[31mError: El nombre de usuario es obligatorio.\033[0m")
        return
    if not contrasena:
        print("\033[31mError: La contraseña es obligatoria.\033[0m")
        return

    usuario = {"Id": (len(usuarios) + 1), "nombre_usuario": usuario_nuevo, "contrasena": contrasena, "activo": True}
    usuarios.append(usuario)
    print()
    print("\033[32mUsuario creado exitosamente.\033[0m")
    print()

def leer_usuario(usuarios):
    datos = []
    print("\033[34mCATÁLOGO DE USUARIOS\033[0m")
    encabezados = ["Id", "Nombre Usuario", "Contraseña", "Activo"]
    for usuario in usuarios:
        datos.append([
            usuario['Id'],
            truncar_texto(usuario['nombre_usuario']),
            usuario['contrasena'],
            "Sí" if usuario['activo'] else "No"
        ])
    print(tabulate(datos, headers=encabezados, tablefmt="pretty"))

def actualizar_usuario(usuarios, id_usuario):
    for usuario in usuarios:
        if usuario["Id"] == id_usuario:
            print("\033[32mUsuario encontrado:\033[0m")
            print(usuario)
            print("\033[35m¿Qué desea cambiar?\033[0m")
            print("1. Editar nombre de usuario")
            print("2. Editar contraseña")

            while True:
                try:
                    opcion_cambio = int(input("\033[35mIngrese la opción: \033[0m"))
                    match opcion_cambio:
                        case 1:
                            nuevo_nombre_usuario = input("\033[35mIngrese el nuevo nombre del usuario: \033[0m")
                            usuario["nombre_usuario"] = nuevo_nombre_usuario
                            print("\033[32mUsuario actualizado exitosamente\033[0m")
                            break
                        case 2:
                            nuevo_contrasena_usuario = input("\033[35mIngrese la nueva contraseña: \033[0m")
                            usuario["contrasena"] = nuevo_contrasena_usuario
                            print("\033[32mUsuario actualizado exitosamente\033[0m")
                            break
                        case _:
                            print("\033[31mIngresó un valor inválido, vuelva a intentarlo\033[0m")
                except ValueError:
                    print("\033[31mError, vuelva a intentarlo\033[0m")
            leer_usuario(usuarios)
            return
    print("\033[31mUsuario no encontrado\033[0m")

def desactivar_usuario(usuarios):
    print()
    print("\033[35mEscribe el ID del usuario que deseas desactivar\033[0m")
    print()
    leer_usuario(usuarios)
    id_usuario = int(input("\033[35mID del usuario: \033[35m"))
    for usuario in usuarios:
        if usuario["Id"] == id_usuario:
            usuario['activo'] = False
            nombre_usuario_desactivado = usuario['nombre_usuario']
            print("")
            print(f"\033[33mEl usuario {nombre_usuario_desactivado} ha sido desactivado exitosamente\033[0m")
            print("")
            leer_usuario(usuarios)
            return
    print("\033[31mUsuario no encontrado\033[0m")