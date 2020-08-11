import clr
import sys
import os

print("start")


# API version 3.0.5
clr.AddReference('BBoxAPI')
from BBoxAPI import *
# print(sys.executable)
os.chdir(".")

instance = BBoxOneAPI()
idx = 0
trmode = 0 
angx = 5
angy = 10

dev_info = instance.ScanningDevice()
bbox_sn = dev_info[0][0:12] # suppose there is only one BBoxOne
bbox_ip = dev_info[0][13:]
print("dev_sn : ", bbox_sn)
print("dev_ip : ", bbox_ip)

info = instance.Init(bbox_sn, 0, idx)
        
instance.SwitchTxRxMode(trmode,bbox_sn)# TX mode
dr = instance.getDR(bbox_sn)
s = instance.setBeamXY(dr[trmode,0], angx, angy, bbox_sn)

print(s)


 