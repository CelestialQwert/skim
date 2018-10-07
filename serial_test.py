import serial
from time import sleep
from magskeeball.findserial import find_serial_ports

ports = find_serial_ports()
if len(ports) > 1:
    print('Found mroe than one port...')
port = ports[0]
print("Using port {}".format(port))


serial = serial.Serial(
    port=port,
    baudrate=9600,
    timeout=.1
)


int_pressed = 0
int_held = 0
x = 0

# while True:
#     serial.write(b"B")
#     pressed = serial.read(4)
#     if pressed != None and pressed != b'':
#         int_pressed = int.from_bytes(pressed,byteorder='little')
#     held = serial.read(4)
#     if held != None and held != b'':
#         int_held = int.from_bytes(held,byteorder='little')
#     print(x,'{0:08x}'.format(int_pressed),'{0:08x}'.format(int_held))
#     x += 1
#     sleep(0.2)

while True:
    serial.write(b"B")
    pressed = serial.read(4)
    if pressed != None and pressed != b'':
        int_pressed = int.from_bytes(pressed,byteorder='little')
    print(x,'{0:08x}'.format(int_pressed))
    x += 1
    sleep(0.1)