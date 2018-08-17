# import some librairies
import socket
import pygame
from math import fabs  # to fine the absolute value

# define some constants
HOST = "127.0.0.1"
PORT = 5400

UP_DOWN_AXIS = 1
LEFT_RIGHT_AXIS = 4

def make_move_command(val):
    if val > 0:
        return "T:F;V:%.2f" % fabs(val)
    if val < 0:
        return "T:B;V:%.2f" % fabs(val)
    return "T:S;V:%.2f" % fabs(val)

def make_turn_command(val):
    if val > 0:
        return "T:R;V:%.2f" % fabs(val)
    if val < 0:
        return "T:L;V:%.2f" % fabs(val)
    return "T:S;V:%.2f" % fabs(val)

# init pygame
pygame.init()
pygame.display.set_mode([512, 512])
pygame.joystick.init()

# connect to the processing server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
print("Connection successfull")


# get the number of current connected joystick
number_of_joystick = pygame.joystick.get_count()

if number_of_joystick > 0:
    print("A joystick was detected")
    controller = pygame.joystick.Joystick(0)
    controller.init()  # init the joystick object
    print(controller.get_numaxes(), controller.get_numbuttons())
    keep_loop = True
    while keep_loop:
        sequence_events = pygame.event.get()  # take all current events
        for current_event in sequence_events:  # seq is a sequence of events
            if current_event.type == pygame.QUIT:
                keep_loop = False  # end the loop
            if current_event.type == pygame.JOYAXISMOTION:  # we detect a joystick event
                up_down_value = -1 * round(controller.get_axis(UP_DOWN_AXIS), 2)
                left_right_value = round(controller.get_axis(LEFT_RIGHT_AXIS), 2)
                up_down_value = 0 if up_down_value > -0.1 and up_down_value < 0.1 else up_down_value
                left_right_value = 0 if left_right_value >-0.1 and left_right_value < 0.1 else left_right_value
                up_down_msg = make_move_command(up_down_value)
                left_right_msg = make_turn_command(left_right_value)
                full_msg = up_down_msg + "|" + left_right_msg + "#"
                print(full_msg)
                client.send(full_msg.encode())
else:
    print("There are no joystick")
    print("Pleae check your setup")

client.close()
