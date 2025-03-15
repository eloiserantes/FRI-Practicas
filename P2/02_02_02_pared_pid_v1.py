#
# Copyright (c) 2022 Manufactura de ingenios tecnológicos SL.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from robobopy.Robobo import Robobo
from robobopy.utils.IR import IR


def turn_right(robobo, speed):
    robobo.moveWheels(-speed, speed)
    # Si pasa de 180º --> continua en -180, -179, ...
    robobo.wait(0.001)


def turn_left(robobo, speed):
    robobo.moveWheels(speed, -speed)
    robobo.wait(0.001)


def turn_degrees(robobo, degrees, speed):
    # giro a la derecha
    if degrees > 0:
        turn_right(robobo, speed)
    # giro a la izquierda
    else:
        turn_left(robobo, speed)
    robobo.stopMotors()


def go_to_wall(rob, goal):
    kp = 1
    while (
        (rob.readIRSensor(IR.FrontC) < goal)
        and (rob.readIRSensor(IR.FrontRR) < goal)
        and (rob.readIRSensor(IR.FrontLL) < goal)
    ):
        error = goal - rob.readIRSensor(IR.FrontC)
        correction = error * kp
        speed = correction
        rob.moveWheels(speed, speed)
        rob.wait(0.1)
    rob.stopMotors()


def limit_speed(speed, max_speed):
    if speed < -2:
        if speed > -5:
            speed = -5
        elif speed < -max_speed:
            speed = -max_speed
    elif speed > 2:
        if speed < 5:
            speed = 5
        elif speed > max_speed:
            speed = max_speed
    return speed


if __name__ == "__main__":
    rob = Robobo("localhost")
    rob.connect()
    frontSensor = IR.FrontRR
    backSensor = IR.BackR
    speed = 20
    turn_speed = 5
    front_distance = 80
    wall_distance = 50
    goal = 50
    kp = 1.5
    ki = 0.2
    kd = 1   

    integral = 0
    previous_error = 0

    if rob.readIRSensor(IR.FrontC) < front_distance:
        go_to_wall(rob, front_distance)

    while True:
        if rob.readIRSensor(IR.FrontC) >= front_distance:
            turn_degrees(rob, -90, turn_speed)
            integral = 0
            previous_error = 0
        else:
            error = rob.readIRSensor(frontSensor) - goal
            integral = integral + error
            derivative = error - previous_error
            correction = round(error * kp + integral * ki + derivative * kd)
            previous_error = error
            correction = limit_speed(correction, speed)
            right_speed = limit_speed(speed + correction, speed)
            left_speed = limit_speed(speed - correction, speed)
            rob.moveWheels(right_speed, left_speed)

        rob.wait(0.1)
