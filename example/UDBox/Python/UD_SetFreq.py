import clr
import sys
import os

print("start")

# API version 3.1.2.2
clr.AddReference('BBoxAPI')
from BBoxAPI import *
# print(sys.executable)
os.chdir(".")

instance = BBoxOneAPI()
idx = 0

dev_info = instance.ScanningDevice(0)
devone = dev_info[idx].split(",")   # Suppose there is only one device
sn = devone[0]
ip = devone[1]
if len(devone) > 2:
    dev_type = int(devone[2])
else:
    dev_type = 0
print("SN:%s, IP:%s, Type:%d" %(sn, ip, dev_type))

info = instance.Init(sn, dev_type, idx)
print("Init: %d" %info)

info = instance.GetState(0, sn)
print("State(Lock): %d" %info)

info = instance.SetState(1, 0, sn)
print("Set State(CH1 OFF): %d" %info[1])

info = instance.SetState(1, 1, sn)
print("Set State(CH1 ON): %d" %info[1])

info = instance.SetUDFreq(26000000, 28000000, 2000000, 100000, sn)
print("Set Freq result: %d" %info)
