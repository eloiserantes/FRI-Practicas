from robobopy.Robobo import Robobo
from robobopy.utils.LED import LED
from robobopy.utils.Color import Color
from robobopy.utils.IR import IR

robobo = Robobo('localhost')
robobo.connect()

speed = 10
Hablar = True
Moverse = True

def tapDetectedCallback():
    global Hablar
    global Moverse
    tap = robobo.readTapSensor()
    if tap.zone == "eye":
        robobo.stopMotors()
        Hablar = False
        Moverse = False
    else:
        Moverse = True
        Hablar = True
        robobo.moveWheels(speed,speed)

robobo.moveWheels(speed,speed)
robobo.whenATapIsDetected(tapDetectedCallback)

while True:
 robobo.wait(3)
 if Hablar:
    robobo.sayText("Si me tocas el ojo dejaré de moverme")