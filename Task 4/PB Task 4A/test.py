import numpy as np
import cv2
from zmqRemoteApi import RemoteAPIClient
import zmq
import os
import time

print("aaaaaaaaaaaaaaaaaaaa")
client = RemoteAPIClient()
sim = client.getObject('sim')
print("bbbbbbbbbbbbbbbbbbbb")
models_directory = os.getcwd()
traffic_sig_model = os.path.join(models_directory, "alpha_bot", "bot.ttt" )
arena = sim.getObject('/Arena')
objectHandle=sim.loadModel(traffic_sig_model)
sim.setObjectParent(objectHandle,arena,True)
sim.setObjectPosition(objectHandle,arena,[0.89,0.89,0.002])
                

