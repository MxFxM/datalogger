import time
import csv

filename = "1h 1000W run hex log.txt"

lines = []

with open(filename) as hexfile:
    for line in hexfile:
        lines.append(line)

hexbytes = []

for line in lines:
    hexbytes = line.split(' ')
    print(len(hexbytes))
    print(hexbytes[0])

hexlines = []

found_ff = False
found_01 = False
hexline = []
for hexbyte in hexbytes:
    hexline.append(hexbyte)
    if not found_ff:
        found_01 = False
        if hexbyte == 'FF':
            found_ff = True
    else: # not found_ff
        if hexbyte == '01':
            hexlines.append(hexline)
            found_ff = False
            found_01 = False
            hexline = []

print(len(hexlines))
print(hexlines[0])

filename = f"log_{int(time.time())}_{filename}.csv"
with open(filename, 'w', newline='') as outputfile:
    writer = csv.writer(outputfile)
    writer.writerow(["InductionMainState", "WaveState", "RequiredPower", "BoosterOn", "CurrentMedian", "HeatsinkTemperature", "InternalTemperature", "CoilTemperature", "ControlBoardRequiredPower"])

    for hexline in hexlines:
        if len(hexline) != 62:
            continue
        InductionMainState = int(hexline[0], 16)
        WaveState = int(hexline[1], 16)
        RequiredPower = int(hexline[2], 16)
        BoosterOn = int(hexline[3], 16)
        CurrentMedian = int(hexline[4], 16)
        HeatsinkTemperature = int(hexline[5], 16)
        InternalTemperature = int(hexline[6], 16)
        CoilTemperature = int(hexline[8], 16)
        ControlBoardRequiredPower = int(hexline[17], 16)
        writer.writerow([InductionMainState, WaveState, RequiredPower, BoosterOn, CurrentMedian, HeatsinkTemperature, InternalTemperature, CoilTemperature, ControlBoardRequiredPower])