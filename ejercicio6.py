from robobopy.Robobo import Robobo
from robobopy.utils.Color import Color
from robobopy.utils.IR import IR

robobo = Robobo('localhost')  
robobo.connect()

robobo.moveTiltTo(100, 25)
robobo.setActiveBlobs(True, False, False, False)  #detecta verde
robobo.moveWheels(10, -10)  

def colordetectcallback():
    color_blob = robobo.readColorBlob(Color.RED)  
    ir_distance = robobo.readIRSensor(IR.FrontC)  
    print(ir_distance)
    if 45 <= color_blob.posx <= 55:  #centrado, avanzar
        robobo.moveWheels(10, 10)
    elif color_blob.posx < 45:  
        robobo.moveWheels(-3, 3)  
    elif color_blob.posx > 55:
        robobo.moveWheels(3, -3)  
    if ir_distance > 300: 
        print("Agarrando cilindro con el pusher...")
        robobo.moveWheelsByTime(2, -2, 5) #implementar coger objeto
        print("Cilindro alcanzado, deteniendo motores.")
        robobo.stopMotors()
        robobo.disconnect()


    robobo.wait(0.01)  

robobo.whenANewColorBlobIsDetected(colordetectcallback)

while True:
    robobo.wait(0.1)