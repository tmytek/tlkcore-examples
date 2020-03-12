import clr
import sys
import os

# API version 1.2.4
clr.AddReference('BBoxAPI')
from BBoxAPI import *


bboxlite_sn = "B19138100-24" # Please replace it by yourself
instance = BBoxLiteAPI()
instance.Init()  
# trmode default should be 0, tx mode
trmode =  instance.GetTxRxMode(bboxlite_sn) 


# trmode  = 0  # TX
trmode  = 1  # RX
instance.SwitchTxRxMode(bboxlite_sn, trmode) # switch to Rx

db = 5.0
angle = 30.0
instance.BeamSteer(bboxlite_sn, trmode, db, angle)