# 1.0 - Acer 2017/07/19 12:00

import numpy as np
from numpy import array as npa
import matplotlib.pyplot as plt

# ============================================================================ #
#                                Check V-REP lib                               #
# ============================================================================ #
try:
    import vrep
except:
    print('--------------------------------------------------------------')
    print('"vrep.py" could not be imported. This means very probably that')
    print('either "vrep.py" or the remoteApi library could not be found.')
    print('Make sure both are in the same folder as this file,')
    print('or appropriately adjust the file "vrep.py"')
    print('--------------------------------------------------------------')
    print('')

# ============================================================================ #
#                               Connect to server                              #
# ============================================================================ #
print('Program started')
vrep.simxFinish(-1)  # just in case, close all opened connections
clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)  # Connect to V-REP
if clientID != -1:
    print('Connected to remote API server')
else:
    print('Failed connecting to remote API server')

# ============================================================================ #
#                                  Get handles                                 #
# ============================================================================ #
h_vision = vrep.simxGetObjectHandle(clientID, 'Vision_sensor', vrep.simx_opmode_blocking)
h_joint01 = vrep.simxGetObjectHandle(clientID, 'Joint01', vrep.simx_opmode_blocking)

#

vrep.simxSetJointTargetPosition(clientID, h_joint01[1], 4, vrep.simx_opmode_blocking)
# ============================================================================ #
#                                Start procedure                               #
# ============================================================================ #
plt.figure()
d = []
for i in range(1000):

    # user input
    s = input('angle')
    if s == '':
        s = 0
    angle = np.float64(s)

    # action
    vrep.simxSetJointTargetPosition(clientID, h_joint01[1], np.pi / 180 * angle, vrep.simx_opmode_blocking)

    # perception
    cAngle = 370
    while np.abs((cAngle - angle) % 360) > 0.5:
        _, cAngle = vrep.simxGetJointPosition(clientID, h_joint01[1], vrep.simx_opmode_blocking)
        cAngle = cAngle / np.pi * 180
    d = vrep.simxGetVisionSensorImage(clientID, h_vision[1], 0, vrep.simx_opmode_blocking)

    # show vision
    img = np.reshape(npa(d[2]), [512, 512, 3])
    plt.cla()
    plt.imshow(img)
    plt.gca().invert_yaxis()
    plt.pause(0.01)
