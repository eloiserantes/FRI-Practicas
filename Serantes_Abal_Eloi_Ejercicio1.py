# Autores: Jacobo Olmedo Sánchez y Eloi Serantes Abal

from robobopy.Robobo import Robobo
from robobopy.utils.LED import LED
from robobopy.utils.Color import Color
from robobopy.utils.IR import IR

robobo = Robobo('localhost')
robobo.connect()
robobo.moveWheels(5, 5)
farIRValue2 = 20
farIRValue3 = 80
farIRValue4 = 120


robobo.setLedColorTo(LED.All, Color.GREEN)

while (robobo.readIRSensor(IR.FrontC) < farIRValue2)and \
 (robobo.readIRSensor(IR.FrontRR) < farIRValue2)and \
 (robobo.readIRSensor(IR.FrontLL) < farIRValue2):
    robobo.wait(0.01)
robobo.setLedColorTo(LED.All, Color.YELLOW)

while (robobo.readIRSensor(IR.FrontC) < farIRValue3)and \
 (robobo.readIRSensor(IR.FrontRR) < farIRValue3)and \
 (robobo.readIRSensor(IR.FrontLL) < farIRValue3):
    robobo.wait(0.01)
robobo.setLedColorTo(LED.All, Color.RED)

while (robobo.readIRSensor(IR.FrontC) < farIRValue4)and \
 (robobo.readIRSensor(IR.FrontRR) < farIRValue4)and \
 (robobo.readIRSensor(IR.FrontLL) < farIRValue4):
    robobo.wait(0.01)
robobo.stopMotors()




