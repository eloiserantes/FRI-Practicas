from robobopy.Robobo import Robobo
from robobopy.utils.Color import Color
from robobopy.utils.IR import IR

robobo = Robobo('localhost')  
robobo.connect()

robobo.moveTiltTo(100, 25)
robobo.setActiveBlobs(True, False, False, False)  # rojo, verde, azul, custom
robobo.moveWheels(10, -10)  

def colordetectcallback():
    color_blob = robobo.readColorBlob(Color.RED)  
    ir_distance = robobo.readIRSensor(IR.FrontC)  
    print(f"Distancia al objeto: {ir_distance} mm")
    
    if 45 <= color_blob.posx <= 55:  # centrado, avanzar
        print("Objeto de frente")
        robobo.moveWheels(10, 10)
    elif color_blob.posx < 45:  
        print("Objeto a la izquierda")
        robobo.moveWheels(-3, 3)  
    elif color_blob.posx > 55:
        print("Objeto a la derecha")
        robobo.moveWheels(3, -3)  
    
    if ir_distance > 100:  # distancia segura para detenerse
        print("Cilindro alcanzado, deteniendo motores.")
        robobo.stopMotors()
        robobo.disconnect()

    robobo.wait(0.01)  

robobo.whenANewColorBlobIsDetected(colordetectcallback)

while True:
    robobo.wait(0.1)


