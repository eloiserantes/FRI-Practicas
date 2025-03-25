from robobopy.Robobo import Robobo
from tkinter import simpledialog, Tk
import re

# Conectar con Robobo
robobo = Robobo("localhost")  # Reemplaza con la IP de tu Robobo
robobo.connect()

speed = 10 

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
    global speed, ultimo_mov  # Usamos variables globales

    if user_response is None:
        robobo.stopMotors()
        robobo.disconnect() 
        return

    user_response = user_response.lower().strip()  

    # Verificar si el comando es solo para cambiar velocidad
    match = re.search(r'velocidad (\d+)', user_response)
    if match:
        speed = int(match.group(1))  # Actualizar la velocidad global
        print(f"Velocidad actualizada a {speed}")
        
        # Si hay un último movimiento, repetirlo con la nueva velocidad
        if ultimo_mov:
            control_robot(ultimo_mov)
        return  

    if re.search(r'\bno\b', user_response):
        print("Comando negado, Robobo no ejecutará el movimiento.")
        return

    # Guardar el comando de movimiento actual para futuras repeticiones
    ultimo_mov = user_response

    # Determinar dirección de movimiento
    if "adelante" in user_response and "izquierda" in user_response:
        print("Moviéndose adelante-izquierda a velocidad", speed)
        robobo.moveWheels(speed//2, speed)
        
    elif "adelante" in user_response and "derecha" in user_response:
        print("Moviéndose adelante-derecha a velocidad", speed)
        robobo.moveWheels(speed, speed//2)

    elif ("atrás" in user_response or "atras" in user_response) and "izquierda" in user_response:
        print("Moviéndose atrás-izquierda a velocidad", speed)
        robobo.moveWheels(-speed//2, -speed)

    elif ("atrás" in user_response or "atras" in user_response) and "derecha" in user_response:
        print("Moviéndose atrás-derecha a velocidad", speed)
        robobo.moveWheels(-speed, -speed//2)

    elif "adelante" in user_response:
        print("Moviéndose hacia adelante a velocidad", speed)
        robobo.moveWheels(speed, speed)

    elif "atrás" in user_response or "atras" in user_response:
        print("Marcha atrás a velocidad", speed)
        robobo.moveWheels(-speed, -speed)

    elif "izquierda" in user_response:
        print("Girando a la izquierda a velocidad", speed)
        robobo.moveWheels(-speed//2, speed//2)

    elif "derecha" in user_response:
        print("Girando a la derecha a velocidad", speed)
        robobo.moveWheels(speed//2, -speed//2)

    else:
        print("Robobo detenido")
        robobo.moveWheels(0, 0)



# Bucle principal para recibir comandos
while True:
    command = get_text_command()
    if command and command.lower() in ["salir", "detener"]:
        print("Deteniendo Robobo")
        robobo.stopMotors()
        robobo.disconnect()
    control_robot(command)
