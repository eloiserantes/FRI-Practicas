# Autores: Jacobo Olmedo Sánchez y Eloi Serantes Abal

from robobopy.Robobo import Robobo
from robobopy.utils.LED import LED
from robobopy.utils.Color import Color
from robobopy.utils.IR import IR

robobo = Robobo('localhost')
robobo.connect()

def tapDetectedCallback():
    robobo.stopMotors()
    robobo.disconnect()

robobo.moveWheels(10,10)
robobo.whenATapIsDetected(tapDetectedCallback)

while True:
 robobo.wait(2)
 robobo.sayText("Si me tocas la cara dejaré de moverme")
