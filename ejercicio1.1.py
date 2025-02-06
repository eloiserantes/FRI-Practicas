from robobopy.Robobo import Robobo
from robobopy.utils.LED import LED
from robobopy.utils.Color import Color
from robobopy.utils.IR import IR

robobo = Robobo('localhost')
robobo.connect()

robobo.moveWheels(20,20)


farIRValue = 50

while True:
    if (robobo.readIRSensor(IR.FrontR) >= farIRValue or
        robobo.readIRSensor(IR.FrontL) >= farIRValue or
        robobo.readIRSensor(IR.BackR) >= farIRValue or
        robobo.readIRSensor(IR.BackL) >= farIRValue):
        robobo.stopMotors()
        robobo.moveWheels(-20, -20)
        robobo.wait(1)
        robobo.moveWheels(20, -20)
        robobo.wait(1)
        robobo.moveWheels(20, 20)
    robobo.wait(0.01)