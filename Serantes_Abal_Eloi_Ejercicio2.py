from robobopy.Robobo import Robobo
from robobopy.utils.Color import Color
from robobopy.utils.IR import IR

# Configuración inicial
robobo = Robobo('localhost')
robobo.connect()
robobo.moveTiltTo(105, 25)

robobo.moveWheels(10, -10)

# Parámetros de control PID
kp = 0.05  # Ganancia proporcional
ki = 0  # Ganancia integral
kd = 0.01  # Ganancia derivativa

# Variables de estado para el PID
integral = 0
last_error = 0
goal_distance = 500  # Distancia objetivo en mm

# Activar la detección de blobs de color
robobo.setActiveBlobs(True, False, False, False)

# Función para limitar la velocidad
def limit_speed(speed, max_speed):
    if speed < 0:
        speed = 0
    elif speed > max_speed:
        speed = max_speed
    return speed

# Función de callback para la detección de color
def colordetectcallback():
    global integral, last_error

    color_blob = robobo.readColorBlob(Color.RED)  # Leer el blob del color especificado
    ir_distance = robobo.readIRSensor(IR.FrontC)  # Leer la distancia al objeto

    if color_blob is not None:  # Si se detecta el color
        print(f"Distancia al objeto: {ir_distance} mm")

        # Calcular el error (diferencia entre la distancia objetivo y la distancia actual)
        error = goal_distance - ir_distance

        # Calcular la integral y la derivada del error
        integral += error
        derivative = error - last_error

        # Calcular la corrección del PID
        correction = kp * error + ki * integral + kd * derivative

        # Limitar la corrección para evitar velocidades excesivas
        correction = limit_speed(correction, 50)  # Limitar la corrección a un máximo de 10
        speed = correction
        # Ajustar la velocidad de los motores en función de la corrección
        if 45 <= color_blob.posx <= 55:  
            print("Objeto de frente")
            robobo.moveWheels(speed, speed)
            print(f"Velocidad: {speed}")
        elif color_blob.posx < 45:  
            print("Objeto a la derecha")
            robobo.moveWheels(3, -3)  
        elif color_blob.posx > 55:
            print("Objeto a la izquierda")
            robobo.moveWheels(-3, 3) 
    else:
        # Si no se detecta el color, seguir girando
        robobo.moveWheels(10, -10)  # Girar sobre sí mismo

    # Actualizar el último error
    last_error = error

    # Condición de parada
    if ir_distance > goal_distance:
        print("Objeto alcanzado, cogiendo el objeto.")
        robobo.moveWheelsByTime(3, -3, 5)
        robobo.stopMotors()

        robobo.disconnect()

    robobo.wait(0.001)  # Pequeña pausa para evitar sobrecarga

# Asignar la función de callback a la detección de blobs de color
robobo.whenANewColorBlobIsDetected(colordetectcallback)

while True:
    robobo.wait(0.001)  # Esperar para evitar sobrecarga