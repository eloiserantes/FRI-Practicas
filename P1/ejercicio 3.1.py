from robobopy.Robobo import Robobo
from robobopy.utils.LED import LED
from robobopy.utils.Color import Color
from robobopy.utils.IR import IR

robobo = Robobo('localhost')
robobo.connect()

speed = 10

def tapDetectedCallback():
    tap = robobo.readTapSensor()
    if tap.zone == "eye":
        robobo.stopMotors()
        robobo.disconnect()
    else:
        robobo.moveWheels(speed,speed)

robobo.moveWheels(speed,speed)
robobo.whenATapIsDetected(tapDetectedCallback)

while True:
 robobo.wait(3)
 robobo.sayText("Si me tocas el ojo dejaré de moverme")