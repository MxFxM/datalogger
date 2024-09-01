import time
import socket
import csv

starttime = time.time()
filename = f"measurements_{int(starttime)}.csv"
device_ip = '192.168.178.169'
device_port = 5025
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((device_ip, device_port))

with open(filename, 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Time [s]", "Delta Time [s]", "Voltage [V]", "Current [A]", "Power [W]"])

while True:
    timestamp = time.time()


    try:
        s.sendall('MEAS:VOLT?\n'.encode())
        voltage = float(s.recv(1024).decode()[:-3])
        s.sendall('MEAS:CURR?\n'.encode())
        current = float(s.recv(1024).decode()[:-3])
        s.sendall('MEAS:POW?\n'.encode())
        power = float(s.recv(1024).decode()[:-3])


        print([timestamp, timestamp-starttime, voltage, current, power])

        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, timestamp-starttime, voltage, current, power])
    except Exception as _:
        s.close()
        time.sleep(5)
        s.connect((device_ip, device_port))
    
    time.sleep(1)

s.close()