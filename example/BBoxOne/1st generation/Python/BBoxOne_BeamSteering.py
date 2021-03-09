import clr
import sys
import os

print("start")


# API version 3.0.8
clr.AddReference('BBoxAPI')
from BBoxAPI import *
# print(sys.executable)
os.chdir(".")

instance = BBoxOneAPI()
idx = 0
trmode = 0 
angx = 5
angy = 10

dev_info = instance.ScanningDevice(0)
devone = dev_info[idx].split(",")   # suppose there is only one BBoxOne
sn = devone[0]
ip = devone[1]
if len(devone) > 2:
    dev_type = int(devone[2])
else:
    dev_type = 0
print("SN:%s, IP:%s, Type:%d" %(sn, ip, dev_type))

info = instance.Init(sn, dev_type, idx)
        
instance.SwitchTxRxMode(trmode,sn)# TX mode
dr = instance.getDR(sn)
s = instance.setBeamXY(dr[trmode,0], angx, angy, sn)

print(s)


 