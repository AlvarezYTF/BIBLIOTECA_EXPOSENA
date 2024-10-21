import json
from datetime import datetime
import sys
import msvcrt
from utils import load_data, save_data
from user_management import administrar_usuarios
from book_management import biblioteca
from loan_management import presta_libros

def main():
    data = load_data()
    usuarios = data['usuarios']
    
    while True:
        usuario_buscado = input("\033[35mINGRESA TU USUARIO: \033[0m")
        usuario_encontrado = False

        for usuario in usuarios:
            if usuario["nombre_usuario"] == usuario_buscado:
                usuario_encontrado = True

                if usuario_buscado == "Admin":
                    if check_password(usuario):
                        administrador(data)
                    else:
                        print("Contraseña incorrecta, vuelva a intentarlo")
                    break

                if not usuario["activo"]:
                    print("El usuario está desactivado del sistema")
                    print("Vuelva a intentarlo")
                    break

                else:
                    if check_password(usuario):
                        presta_libros(usuario_buscado, data)
                    else:
                        print("Contraseña incorrecta, vuelva a intentarlo")
                break

        if not usuario_encontrado:
            print("Usuario no encontrado")
            print("Vuelva a intentarlo")

def check_password(usuario):
    contrasena_buscado = ""
    print("\033[35mINGRESA TU CONTRASEÑA: \033[0m", end="", flush=True)

    while True:
        char = msvcrt.getch()
        if char == b'\r':
            print()
            break
        elif char == b'\x08':
            if contrasena_buscado:
                contrasena_buscado = contrasena_buscado[:-1]
                sys.stdout.write('\b \b')
                sys.stdout.flush()
        else:
            contrasena_buscado += char.decode()
            sys.stdout.write('*')
            sys.stdout.flush()

    return usuario["contrasena"] == contrasena_buscado

def administrador(data):
    while True:
        print("\033[35mEscoge que sistema quieres utilizar\033[0m")
        print()
        print("1. Administración de libros\n2. Administración de usuarios\n3. Salir")
        print()
        try:
            opcion_sistema = int(input("\033[35mEscoge tu opción: \033[0m"))
            match opcion_sistema:
                case 1:
                    biblioteca(data)
                case 2:
                    administrar_usuarios(data)
                case 3:
                    save_data(data)
                    return
                case _:
                    print("Número no válido")
        except ValueError:
            print("Valor no válido")
            print("Por favor Vuelva a intentarlo")
            print()

if __name__ == "__main__":
    main()
