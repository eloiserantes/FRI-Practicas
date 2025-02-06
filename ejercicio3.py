from robobopy.Robobo import Robobo
from robobopy.utils.LED import LED
from robobopy.utils.Color import Color
from robobopy.utils.IR import IR

robobo = Robobo('localhost')
robobo.connect()
Hablar = True

def tapDetectedCallback():
    global Hablar
    robobo.stopMotors()
    Hablar = False

robobo.moveWheels(10,10)
robobo.whenATapIsDetected(tapDetectedCallback)

while True:
 robobo.wait(3)
 if Hablar:
    robobo.sayText("Si me tocas la cara dejaré de moverme")
