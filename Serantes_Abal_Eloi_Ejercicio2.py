# Autores: Jacobo Olmedo Sánchez y Eloi Serantes Abal

from robobopy.Robobo import Robobo
from robobopy.utils.LED import LED
from robobopy.utils.Color import Color
from robobopy.utils.IR import IR
from robobopy.utils.Sounds import Sounds
from robobopy.utils.Emotions import Emotions

robobo = Robobo('localhost')
robobo.connect()

farIRValue = 85
speed = 10
robobo.moveWheels(speed,speed)

while(robobo.readIRSensor(IR.FrontC) < farIRValue)and \
 (robobo.readIRSensor(IR.FrontRR) < farIRValue)and \
 (robobo.readIRSensor(IR.FrontLL) < farIRValue):
    robobo.wait(0.01)

robobo.stopMotors()
robobo.setEmotionTo(Emotions.SURPRISED)
robobo.playSound(Sounds.DISCOMFORT)
robobo.wait(0.01)
robobo.moveTiltTo(50,15)
robobo.wait(0.01)
robobo. moveWheelsByTime(-speed,-speed,2)
robobo.sayText("Ui, casi choco!")
robobo.moveTiltTo(75,15)
robobo.setEmotionTo(Emotions.NORMAL)
robobo.wait(0.01)