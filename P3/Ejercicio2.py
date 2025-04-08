from robobopy.Robobo import Robobo
from tkinter import simpledialog, Tk
import re

# Conectar con Robobo
robobo = Robobo("localhost") 
robobo.connect()

speed = 10  
ultimo_mov = None  # Inicializar último movimiento

# Función para obtener el comando de texto del usuario
def get_text_command():
    root = Tk()
    root.withdraw() 
    user_input = simpledialog.askstring("Command Input", "Ingrese su comando:")
    
    if user_input:
        print("Comando recibido:", user_input)
    else:
        print("No se ingresó ningún comando.")
    
    return user_input

# Función para interpretar y ejecutar comandos
def control_robot(user_response):
    global speed, ultimo_mov

    if user_response is None:
        robobo.stopMotors()
        robobo.disconnect()
        return

    user_response = user_response.lower().strip()

    # Detectar comandos como “adelante a velocidad 20”
    match_velocidad_nueva = re.search(r'a velocidad (\d+)', user_response)
    if match_velocidad_nueva:
        speed = int(match_velocidad_nueva.group(1))
        print(f"Velocidad nueva detectada y actualizada a {speed}")
        user_response = re.sub(r'a velocidad \d+', '', user_response).strip()

    # Comando explícito solo de velocidad (sin movimiento)
    match_cambio_velocidad = re.fullmatch(r'velocidad (\d+)', user_response)
    if match_cambio_velocidad:
        speed = int(match_cambio_velocidad.group(1))
        print(f"Velocidad actualizada a {speed}")
        if ultimo_mov:
            print(f"Repitiendo último comando: {ultimo_mov} con nueva velocidad {speed}")
            control_robot(ultimo_mov)
        return

    # Comando negado
    if user_response.startswith("no "):
        print("Comando negado, Robobo no ejecutará el movimiento.")
        return

    # Guardar el comando
    ultimo_mov = user_response

    # Comandos de movimiento
    if "adelante" in user_response and "izquierda" in user_response:
        print("Moviéndose adelante-izquierda a velocidad", speed)
        robobo.moveWheels(speed, speed//2)

    elif "adelante" in user_response and "derecha" in user_response:
        print("Moviéndose adelante-derecha a velocidad", speed)
        robobo.moveWheels(speed//2, speed)

    elif ("atrás" in user_response or "atras" in user_response) and "izquierda" in user_response:
        print("Moviéndose atrás-izquierda a velocidad", speed)
        robobo.moveWheels(-speed, -speed//2)

    elif ("atrás" in user_response or "atras" in user_response) and "derecha" in user_response:
        print("Moviéndose atrás-derecha a velocidad", speed)
        robobo.moveWheels(-speed//2, -speed)

    elif "adelante" in user_response:
        print("Moviéndose hacia adelante a velocidad", speed)
        robobo.moveWheels(speed, speed)

    elif "atrás" in user_response or "atras" in user_response:
        print("Marcha atrás a velocidad", speed)
        robobo.moveWheels(-speed, -speed)

    elif "izquierda" in user_response:
        print("Girando a la izquierda a velocidad", speed)
        robobo.moveWheels(speed//2, -speed//2)

    elif "derecha" in user_response:
        print("Girando a la derecha a velocidad", speed)
        robobo.moveWheels(-speed//2, speed//2)

    else:
        print("Robobo detenido")
        robobo.stopMotors()

# Bucle principal para recibir comandos
while True:
    command = get_text_command()
    if command and command.lower() in ["salir", "detener"]:
        print("Deteniendo Robobo")
        robobo.stopMotors()
        robobo.disconnect()
        break  # Salir del bucle
    control_robot(command)
