from vds1022 import *

dev = VDS1022(debug=0)
dev.set_channel(CH1, range='100v', offset=1/100, probe='x100')
dev.set_channel(CH2, range='200v', offset=1/100, probe='x100')

for frames in dev.fetch_iter(freq=2) :
    print(f"Vrms:{frames.ch1.rms()}\t{frames.ch2.rms()}", end='\r')