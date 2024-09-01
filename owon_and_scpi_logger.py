from vds1022 import *
import time
import socket
import csv

dev = VDS1022(debug=0)
dev.set_channel(CH1, range='100v', offset=1/100, probe='x100')
dev.set_channel(CH2, range='200v', offset=1/100, probe='x100')

starttime = time.time()
filename = f"measurements_{int(starttime)}.csv"
device_ip = '192.168.178.169'
device_port = 5025
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((device_ip, device_port))

with open(filename, 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Time [s]", "Delta Time [s]", "Voltage [V]", "Current [A]", "Power [W]", "Input [V]", "Output [V]"])

while True:
    timestamp = time.time()


    try:
        s.sendall('MEAS:VOLT?\n'.encode())
        time.sleep(0.1)
        voltage = float(s.recv(1024).decode()[:-3])
        s.sendall('MEAS:CURR?\n'.encode())
        time.sleep(0.1)
        current = float(s.recv(1024).decode()[:-3])
        s.sendall('MEAS:POW?\n'.encode())
        time.sleep(0.1)
        power = float(s.recv(1024).decode()[:-3])

        for frames in dev.fetch_iter(freq=2) :
            ch1 = frames.ch1.rms()
            ch2 = frames.ch2.rms()
            break

        print([timestamp, timestamp-starttime, voltage, current, power, ch1, ch2])

        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, timestamp-starttime, voltage, current, power, ch1, ch2])
    except Exception as _:
        s.close()
        s = None
        time.sleep(5)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((device_ip, device_port))
    
    time.sleep(1)

s.close()