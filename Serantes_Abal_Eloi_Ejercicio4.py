# Autores: Jacobo Olmedo Sánchez y Eloi Serantes Abal

from robobopy.Robobo import Robobo
import random

robobo = Robobo('localhost')  
robobo.connect()

robobo.moveTiltTo(100, 25)  

def qrDetectedCallback():
    qr_data = robobo.readQR()
    distance = robobo.readQR().distance
    if qr_data.id:
        print(f"QR detectado: {qr_data.id} a {distance} m")
    
    if qr_data.id == "peligro izquierda" and distance> 30:
        robobo.moveWheelsByTime(19.7, 11.5, 4.3)
        robobo.moveWheels(25, 25)
    if qr_data.id == "cruce-izquierda" and distance> 21:
        # aleatoriamente elige seguir recto o girar a la izquierda (opción comentada)
            #decision = random.choice([ "recto","izquierda"])
            #if decision == "recto":
            #    print("Decisión: Seguir recto")
            #    robobo.moveWheels(20, 20)
            #else:
            #    print("Decisión: Girar a la izquierda")
            robobo.moveWheelsByTime(20, 20, 5.3)  
            robobo.moveWheelsByTime(19.5, -18,1)  
            robobo.moveWheels(20, 20)  
    if qr_data.id == "peatones" and distance > 21.5:
        robobo.moveWheels(0, 0)
        robobo.sayText("No hay peatones, podemos seguir")
        robobo.moveWheels(25, 25)
        robobo.wait(3)

    if qr_data.id == "velocidad 10" and distance > 21.5:
        robobo.sayText("Me pongo a velocidad 10")
        robobo.moveWheels(10, 10)
        robobo.wait(3)

    if qr_data.id == "ceda" and distance > 25:
        robobo.stopMotors()
        robobo.disconnect()
    robobo.wait(0.01)

robobo.whenAQRCodeIsDetected(qrDetectedCallback)

robobo.moveWheels(20, 20)

while True:
    robobo.wait(0.1)

