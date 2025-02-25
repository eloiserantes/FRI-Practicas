from robobopy.Robobo import Robobo
from robobopy.utils.Color import Color
from robobopy.utils.IR import IR
import time

robobo = Robobo('localhost')  
robobo.connect()

robobo.moveTiltTo(100, 25)
robobo.setActiveBlobs(True, True, True, True)  # Activar detección de rojo, verde y azul
robobo.moveWheels(10, -10)  

# Variable para evitar que Robobo retroceda infinitamente
peligro_detectado = False
ultimo_color_detectado = None
ultimo_tiempo_detectado = time.time()

def colordetectcallback():
    global peligro_detectado, ultimo_color_detectado, ultimo_tiempo_detectado
    color_blobs = robobo.readAllColorBlobs()
    ir_distance = robobo.readIRSensor(IR.FrontC)  
    print(f"Distancia al objeto: {ir_distance} mm")
    
    detected_colors = []
    
    if color_blobs:
        for color_blob in color_blobs:
            detected_color = str(color_blob).upper()  # Convertir a string en mayúsculas
            detected_colors.append(detected_color)
    
    if detected_colors:
        print(f"Colores detectados: {detected_colors}")
        
        # Si se detecta un nuevo color, actualizar el tiempo
        if detected_colors != ultimo_color_detectado:
            ultimo_color_detectado = detected_colors
            ultimo_tiempo_detectado = time.time()
        
        # Si ha pasado al menos 1 segundo viendo el mismo color, tomar acción
        if time.time() - ultimo_tiempo_detectado > 1:
            if "RED" in detected_colors and not peligro_detectado:
                print("Color peligroso detectado. Alejándose una vez.")
                robobo.moveWheels(-10, -10)  # Retrocede
                robobo.wait(1)  # Espera un segundo mientras retrocede
                robobo.stopMotors()  # Se detiene
                peligro_detectado = True
                robobo.disconnect  # Evita que vuelva a retroceder
            else:
                for color in detected_colors:
                    if color != "RED":
                        print(f"Color seguro detectado: {color}")
                        print(f"Anunciando: Color {color}")  # En lugar de usar speak()
    
    robobo.wait(0.1)  # Reducir la frecuencia de callbacks para evitar saturación

robobo.whenANewColorBlobIsDetected(colordetectcallback)

while True:
    robobo.wait(0.1)




