from robobopy.Robobo import Robobo
from robobopy.utils.Color import Color
from robobopy.utils.IR import IR

robobo = Robobo('localhost')  
robobo.connect()

robobo.moveTiltTo(100, 25)
robobo.setActiveBlobs(True, False, False, False)  # rojo, verde, azul, custom
robobo.moveWheels(10, -10)  

def colordetectcallback():
    color_blobs = robobo.readAllColorBlobs()
    ir_distance = robobo.readIRSensor(IR.FrontC)  
    print(f"Distancia al objeto: {ir_distance} mm")
    
    if color_blobs:
        for color_blob in color_blobs:
            detected_color = str(color_blob).upper()  # Convertir a string y mayúsculas para comparación
            print(f"Color detectado: {detected_color}")
            
            if detected_color == "RED":
                print("Color peligroso detectado. Alejándose.")
                robobo.moveWheels(-10, -10)
                robobo.disconnect()  # Retrocede
            else:
                print(f"Color seguro detectado: {detected_color}")
                print(f"Anunciando: Color {detected_color}")  # En lugar de usar speak()
            
            robobo.wait(0.1)  # Pausa para procesar cada color
    
    robobo.wait(0.1)  # Reducir la frecuencia de callbacks para evitar saturación

robobo.whenANewColorBlobIsDetected(colordetectcallback)

while True:
    robobo.wait(0.1)


