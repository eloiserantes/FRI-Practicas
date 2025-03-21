from robobopy.Robobo import Robobo
from robobopy.utils.Color import Color
from robobopy.utils.IR import IR

robobo = Robobo('localhost')
robobo.connect()
robobo.moveTiltTo(105, 25)
robobo.moveWheels(8, -8)

kp_distance = 0.07  # Ganancia proporcional para la velocidad de aproximación
kp_posx = 0.2       # Ganancia proporcional para la posición en el eje X
ki_posx = 0.001    # Ganancia integral para la posición en el eje X
kd_posx = 0.02      # Ganancia derivativa para la posición en el eje X
goal_distance = 300  # Distancia objetivo 
goal_posx = 50       # Posición objetivo en el eje X (medio)

integral_posx = 0
previous_error_posx = 0

# Activar la detección de blobs rojo
robobo.setActiveBlobs(True, False, False, False)

def colordetectcallback():
    global integral_posx, previous_error_posx  # Usamos variables globales para el control PID de posx

    color_blob = robobo.readColorBlob(Color.RED)  # Leer el blob rojo
    ir_distance = robobo.readIRSensor(IR.FrontC)  # Leer la distancia al objeto

    if color_blob is not None:  
        print(f"Distancia al objeto: {ir_distance}")
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

        # Si la posición en el eje X está entre 45 y 55, mover en línea recta
        if 45 <= color_blob.posx <= 55:
            speed_left = speed_distance
            speed_right = speed_distance
        else:
            # Combinar las correcciones de distancia y posición
            speed_left = speed_distance + correction_posx
            speed_right = speed_distance - correction_posx

        # Limitar las velocidades para evitar valores extremos
        max_speed = 30
        speed_left = max(min(speed_left, max_speed), -5)
        speed_right = max(min(speed_right, max_speed), -5)

        # Mover el robot con las velocidades calculadas
        robobo.moveWheels(speed_left, speed_right)
        print(f"Velocidades: izquierda={speed_left}, derecha={speed_right}")

    else:
        # Si no se detecta el color, seguir girando
        robobo.moveWheels(8, -8)  

    # Condición de parada
    if ir_distance > goal_distance:
        print("Objeto alcanzado, deteniendo motores.")
        robobo.moveWheels(5,-5)
        robobo.wait(3)
        robobo.stopMotors()
        robobo.disconnect()

    robobo.wait(0.001)  

robobo.whenANewColorBlobIsDetected(colordetectcallback)

while True:
    robobo.wait(0.001)  