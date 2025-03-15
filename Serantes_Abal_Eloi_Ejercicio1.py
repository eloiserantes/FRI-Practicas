from robobopy.Robobo import Robobo
from robobopy.utils.Color import Color
from robobopy.utils.IR import IR

# Configuración inicial
robobo = Robobo('localhost')
robobo.connect()
robobo.moveTiltTo(100, 25)

robobo.moveWheels(10, -10)

# Parámetros de control
kp = 0.2  # Ganancia proporcional para la velocidad
goal_distance = 105  # Distancia objetivo en mm

# Activar la detección de blobs de color
robobo.setActiveBlobs(True, False, False, False)

# Función de callback para la detección de color
def colordetectcallback():
    color_blob = robobo.readColorBlob(Color.RED)  # Leer el blob del color especificado
    ir_distance = robobo.readIRSensor(IR.FrontC)  # Leer la distancia al objeto

    if color_blob is not None:  # Si se detecta el color
        print(f"Distancia al objeto: {ir_distance} mm")

        # Ajustar la velocidad de aproximación en función de la distancia
        if 45 <= color_blob.posx <= 55:  
            print("Objeto de frente")
            error = goal_distance - ir_distance
            speed = error * kp
            robobo.moveWheels(speed, speed)
            print(f"Velocidad: {speed}")
            # robobo.moveWheels(10, 10)  # Mover hacia adelante con velocidad gradual
        elif color_blob.posx < 45:  
            print("Objeto a la derecha")
            robobo.moveWheels(3, -3)  
        elif color_blob.posx > 55:
            print("Objeto a la izquierda")
            robobo.moveWheels(-3, 3) 
    else:
        # Si no se detecta el color, seguir girando
        robobo.moveWheels(10, -10)  # Girar sobre sí mismo

    # Condición de parada
    if ir_distance > goal_distance:
        print("Objeto alcanzado, deteniendo motores.")
        robobo.stopMotors()
        robobo.disconnect()

    robobo.wait(0.01)  # Pequeña pausa para evitar sobrecarga

# Asignar la función de callback a la detección de blobs de color
robobo.whenANewColorBlobIsDetected(colordetectcallback)

while True:
    robobo.wait(0.01)  # Esperar para evitar sobrecarga