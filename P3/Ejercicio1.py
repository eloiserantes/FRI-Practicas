from pynput import keyboard
from robobopy.Robobo import Robobo
import time

robobo = Robobo("localhost") 
robobo.connect()

# Variable para rastrear teclas activas
keys_pressed = set()
ultimo_comando = None  # Guarda el último comando enviado

# Función para manejar las teclas presionadas
def on_press(key):
    global ultimo_comando
    try:
        char = key.char.lower()
        keys_pressed.add(char)  

        if 'w' in keys_pressed:
            comando = (10, 10) 
            mensaje = "Moviéndose hacia adelante"
        elif 's' in keys_pressed:
            comando = (-10, -10)  
            mensaje = "Marcha atrás"
        elif 'a' in keys_pressed:
            comando = (-5, 5)  
            mensaje = "Girando a la izquierda"
        elif 'd' in keys_pressed:
            comando = (5, -5)  
            mensaje = "Girando a la derecha"
        else:
            comando = (0, 0)  
            mensaje = "Detenido"

        # Solo enviar el comando si ha cambiado
        if comando != ultimo_comando:
            print(mensaje)
            robobo.moveWheels(*comando)
            ultimo_comando = comando  # Guardar el último comando enviado

    except AttributeError:
        pass

# Función para detener el robot cuando se suelta la última tecla
def on_release(key):
    global ultimo_comando
    try:
        char = key.char.lower()
        if char in keys_pressed:
            keys_pressed.remove(char)

        if not keys_pressed:  # Si no hay teclas activas, detener Robobo
            if ultimo_comando != (0, 0):
                print("Detenido")
                robobo.moveWheels(0, 0)
                ultimo_comando = (0, 0)

    except AttributeError:
        pass

# Iniciar la escucha del teclado en un hilo
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

# Bucle principal para mantener el programa corriendo
while True:
    robobo.wait(0.1)  # Evita que el bucle consuma demasiados recursos




