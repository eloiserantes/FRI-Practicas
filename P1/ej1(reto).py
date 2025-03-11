# This imports the library
from robobopy.Robobo import Robobo
from robobopy.utils.LED import LED
from robobopy.utils.Color import Color
from robobopy.utils.IR import IR
# This creates an instance of the Robobo class with the indicated IP address
robobo = Robobo('localhost')
robobo.connect()
robobo.moveWheelsByTime(0, 100, 1, wait=True)
robobo.moveWheels(15, 15)
