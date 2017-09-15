import importlib
from datetime import datetime
import os

import matplotlib.pyplot as plt
import numpy as np
from numpy import array as npa

from VrepPythonApi import vrep
from VrepPythonApi import vrep_ext
from armDemo import ArmDemo, waitSecs
from acerlib import logging_ext

# ================================ parameters ================================ #
nRun = 2
nReachPerRun = 20
nObj = 70
pathname = 'armDemo_data'

# ============================== initialisation ============================== #
try:
    os.mkdir(pathname)
except:
    print('Folder exists')

logger = logging_ext.DataLogger(os.path.join(pathname, 'data.txt'),
                                '{}\t{}\t{}\t{}\t{}',
                                ['isGetObject', 'targetX', 'targetY', 'targetZ', 'imgFile'])

# ============================================================================ #
#                               Connect to V-rep                               #
# ============================================================================ #
arm = ArmDemo('192.168.1.170')

# ============================================================================ #
#                               Simulation start                               #
# ============================================================================ #
iSample = 0
for iRun in range(nRun):
    # restart simulation
    arm.restartSim()

    # create objects
    arm.createRandomObj(nObj)

    # ---------------------------------------------------------------------------- #
    #                                  Pick object                                 #
    # ---------------------------------------------------------------------------- #
    for iReach in range(nReachPerRun):
        print('iSample = {}'.format(iSample))
        isReach = True
        arm.resetArmPosition()
        img = arm.getImageFromCam()

        # generate target location
        pick_x = np.random.uniform(0.2, 0.8, 1)[0]
        pick_y = np.random.uniform(0.07, 0.45, 1)[0]
        # pick_x = np.random.uniform(-0.1, 1.1, 1)[0]
        # pick_y = np.random.uniform(-0.1, 1.1, 1)[0]
        targetPosition = [pick_x, pick_y, 0.054]

        # move above
        arm.moveTo([pick_x, pick_y, 0.17])
        arm.waitToDistination()

        # move down
        arm.moveTo([pick_x, pick_y, .054])
        arm.waitToDistination()

        # grab
        arm.enableSuctionCup(1)
        waitSecs(0.5)
        isGet = arm.isGrip()
        print('GetObj = {}'.format(isGet))

        # move above again
        arm.moveTo([pick_x, pick_y, arm.position_init[2]])
        arm.waitToDistination()

        # reset
        arm.resetArmPosition()
        isReach &= arm.waitToDistination()

        # release
        arm.enableSuctionCup(0)
        waitSecs(0.5)

        if isReach:
            filename = 'armDemo_{:d}.png'.format(iSample)
            plt.imsave(os.path.join(pathname, filename), img)
            logger.write(isGet, targetPosition[0], targetPosition[1], targetPosition[2], filename)
            iSample += 1
        else:
            arm.restartSim()
            arm.createRandomObj(nObj)
