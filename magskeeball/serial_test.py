import serial
from time import sleep


serial = serial.Serial(
    port='COM3',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=.1,
    rtscts=False,
    dsrdtr=False
)


int_pressed = 0
int_held = 0
x = 0

while True:
    serial.write(b"B")
    pressed = serial.read(2)
    if pressed != None and pressed != b'':
        int_pressed = int.from_bytes(pressed,byteorder='little')
    held = serial.read(2)
    if held != None and held != b'':
        int_held = int.from_bytes(held,byteorder='little')
    print(x,int_pressed,int_held)
    x += 1
    sleep(0.2)
