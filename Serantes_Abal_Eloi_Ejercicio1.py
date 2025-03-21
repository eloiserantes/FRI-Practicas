from robobopy.Robobo import Robobo
from robobopy.utils.Color import Color
from robobopy.utils.IR import IR

robobo = Robobo('localhost')
robobo.connect()
robobo.moveTiltTo(105, 25)

robobo.moveWheels(10, -10)

kp = 0.2  # Ganancia proporcional para la velocidad
goal_distance = 105  

robobo.setActiveBlobs(True, False, False, False) # Se activa el rojo sólo

def colordetectcallback():
    color_blob = robobo.readColorBlob(Color.RED)  # Leer el blob rojo
    ir_distance = robobo.readIRSensor(IR.FrontC)  # Leer la distancia al objeto

    if color_blob is not None:  
        print(f"Distancia al objeto: {ir_distance}")
        error = goal_distance - ir_distance
        speed = error * kp   # Ajustar la velocidad de aproximación en función de la distancia
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
        robobo.moveWheels(10, -10)  

    # Condición de parada
    if ir_distance > goal_distance:
        print("Objeto alcanzado, deteniendo motores.")
        robobo.stopMotors()
        robobo.disconnect()

    robobo.wait(0.01)  

robobo.whenANewColorBlobIsDetected(colordetectcallback)

while True:
    robobo.wait(0.01)  