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
        # aleatoriamente elige seguir recto o girar a la izquierda
            decision = random.choice([ "izquierda"])
            if decision == "recto":
                print("Decisión: Seguir recto")
                robobo.moveWheels(20, 20)
            else:
                print("Decisión: Girar a la izquierda")
                robobo.moveWheelsByTime(20, 20, 5.3)  
                robobo.moveWheelsByTime(19.5, -18,1)  # Gira a la izquierda
                robobo.moveWheels(20, 20)  # Sigue adelante después de girar
    if qr_data.id == "peatones" and distance > 21.5:
        robobo.moveWheels(0, 0)
        robobo.sayText("No hay peatones, podemos seguir")
        robobo.moveWheels(25, 25)
        robobo.wait(3)

    if qr_data.id == "velocidad10" and distance > 21.5:
        robobo.sayText("Me pongo a velocidad 10")
        robobo.moveWheels(10, 10)
        robobo.wait(3)

    if qr_data.id == "ceda" and distance > 25:
        robobo.stopMotors()
        robobo.disconnect()
    robobo.wait(0.01)
# Configurar el callback para detección de QR
robobo.whenAQRCodeIsDetected(qrDetectedCallback)

# Moverse hacia adelante hasta detectar un QR
robobo.moveWheels(20, 20)

# Mantener el programa en ejecución
while True:
    robobo.wait(0.1)

