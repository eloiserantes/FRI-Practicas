from robobopy.Robobo import Robobo
from robobopy.utils.Color import Color
from robobopy.utils.IR import IR

# Configuración inicial
robobo = Robobo('localhost')
robobo.connect()
robobo.moveTiltTo(105, 25)
robobo.moveWheels(8, -8)
# Parámetros de control
kp_distance = 0.2  # Ganancia proporcional para la velocidad de aproximación
kp_posx = 0.55       # Ganancia proporcional para la posición en el eje X
ki_posx = 0.0005    # Ganancia integral para la posición en el eje X
kd_posx = 0.02      # Ganancia derivativa para la posición en el eje X
goal_distance = 184  # Distancia objetivo en mm
goal_posx = 50       # Posición objetivo en el eje X (centro de la cámara)

# Variables para el control PID de la posición en el eje X
integral_posx = 0
previous_error_posx = 0

# Activar la detección de blobs de color
robobo.setActiveBlobs(True, False, False, False)

# Función de callback para la detección de color
def colordetectcallback():
    global integral_posx, previous_error_posx  # Usamos variables globales para el control PID de posx

    color_blob = robobo.readColorBlob(Color.RED)  # Leer el blob del color especificado
    ir_distance = robobo.readIRSensor(IR.FrontC)  # Leer la distancia al objeto

    if color_blob is not None:  # Si se detecta el color
        print(f"Distancia al objeto: {ir_distance} mm")
        print(f"Posición del objeto (posx): {color_blob.posx}")

        # Control proporcional para la distancia al objeto
        error_distance = goal_distance - ir_distance
        speed_distance = error_distance * kp_distance  # Velocidad de aproximación proporcional

        # Control PID para la posición en el eje X (posx)
        error_posx = goal_posx - color_blob.posx
        integral_posx += error_posx
        derivative_posx = error_posx - previous_error_posx
        correction_posx = error_posx * kp_posx + integral_posx * ki_posx + derivative_posx * kd_posx
        previous_error_posx = error_posx

        # Combinar las correcciones de distancia y posición
        speed_left = speed_distance + correction_posx
        speed_right = speed_distance - correction_posx

        # Limitar las velocidades para evitar valores extremos
        max_speed = 25
        speed_left = max(min(speed_left, max_speed), -5)
        speed_right = max(min(speed_right, max_speed), -5)

        # Mover el robot con las velocidades calculadas
        robobo.moveWheels(speed_left, speed_right)
        print(f"Velocidades: izquierda={speed_left}, derecha={speed_right}")

    else:
        # Si no se detecta el color, seguir girando
        robobo.moveWheels(8, -8)  # Girar sobre sí mismo

    # Condición de parada
    if ir_distance > goal_distance:
        print("Objeto alcanzado, deteniendo motores.")
        robobo.moveWheels(5,-5)
        robobo.wait(1)
        robobo.stopMotors()
        robobo.disconnect()

    robobo.wait(0.001)  # Pequeña pausa para evitar sobrecarga

# Asignar la función de callback a la detección de blobs de color
robobo.whenANewColorBlobIsDetected(colordetectcallback)

while True:
    robobo.wait(0.001)  # Esperar para evitar sobrecarga