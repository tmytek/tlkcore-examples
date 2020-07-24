import clr
import sys
import os

print("start")
# API version 3.0.4
clr.AddReference('BBoxAPI')
from BBoxAPI import *
bbox_sn = "000000000-00"
instance = BBoxOneAPI()
idx = 0
trmode = 0 
angx = 5
angy = 10

dev_info = instance.ScanningDevice()

bbox_sn = dev_info[0][0:12] # suppose there is only one BBoxOne

info = instance.Init(bbox_sn, 0, idx)
        
instance.SwitchTxRxMode(trmode,bbox_sn)# TX mode
dr = instance.getDR(bbox_sn)

s = instance.setBeamXY(dr[trmode,0], angx, angy, bbox_sn)
 