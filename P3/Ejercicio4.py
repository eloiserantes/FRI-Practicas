from robobopy.Robobo import Robobo
import openai
import re

# Conectar con Robobo
robobo = Robobo("localhost")
robobo.connect()

speed = 10  # Velocidad base del robot
ultimo_mov = None  # Último movimiento para referencia

# Configuración de la API de OpenAI
openai.api_key = "your-api-key"

# Función para enviar comandos a ChatGPT
def send_to_chatgpt(command):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Responde con una de las siguientes opciones exactas: 'adelante', 'atrás', 'izquierda', 'derecha', 'adelante izquierda', 'adelante derecha', 'atrás izquierda', 'atrás derecha'."},
            {"role": "user", "content": command}
        ],
        temperature=0  
    )
    return response["choices"][0]["message"]["content"].strip().lower()

# Función para interpretar y ejecutar comandos en Robobo
def control_robot(user_response):
    global speed, ultimo_mov  

    if user_response is None:
        robobo.stopMotors()
        robobo.disconnect()
        return

    user_response = user_response.lower().strip()

    # Verificar si es un cambio de velocidad
    match = re.search(r'velocidad (\d+)', user_response)
    if match:
        speed = int(match.group(1))
        print(f"Velocidad actualizada a {speed}")

        if ultimo_mov:
            control_robot(ultimo_mov)  # Repetir último movimiento con nueva velocidad
        return  

    # Guardar el último movimiento
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

# Bucle principal para recibir comandos desde ChatGPT
while True:
    user_command = input("Describe el movimiento del robot: ")  # Entrada del usuario
    if user_command.lower() in ["salir", "detener"]:
        print("Deteniendo Robobo")
        robobo.stopMotors()
        robobo.disconnect()
        break

    chatgpt_response = send_to_chatgpt(user_command)  # Obtener la decisión de ChatGPT
    control_robot(chatgpt_response)  # Ejecutar el movimiento
