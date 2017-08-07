import numpy as np
import matplotlib.pyplot as plt
from numpy import array as npa
from datetime import datetime

from VrepPythonApi import vrep
from VrepPythonApi import vrep_ext


def waitSecs(t):
    t0 = datetime.now()
    dt = (datetime.now() - t0).total_seconds()
    while dt < t:
        dt = (datetime.now() - t0).total_seconds()


class ArmDemo(vrep_ext.VrepController):
    def __init__(self, *args, **kwargs):
        super(ArmDemo, self).__init__(*args, **kwargs)
        self.h_orig = vrep.simxGetObjectHandle(self.clientID, 'box_orig', vrep.simx_opmode_blocking)[1]
        self.h_arm = vrep.simxGetObjectHandle(self.clientID, 'redundantRob_target', vrep.simx_opmode_blocking)[1]
        self.h_movingLagDist = vrep.simxGetDistanceHandle(self.clientID, 'movingLagDist', vrep.simx_opmode_blocking)[1]
        self.position_init = self.getArmPosition()

    def startSim(self):
        super(ArmDemo, self).startSim()
        self.position_init = self.getArmPosition()

    def moveTo(self, targetPosition):
        vrep.simxSetObjectPosition(self.clientID, self.h_arm, self.h_orig, targetPosition,
                                   vrep.simx_opmode_blocking)

        # --- old method: using v-rep scene model --- #
        # targetPosition = vrep_ext.toLuaStr_array(targetPosition)
        # self.callAssociatedScriptFunction('redundantRobot', 'moveTo',
        #                                   vrep.simx_opmode_blocking, targetPosition)
        # ---------------------------------------------------------------------------- #

    def enableSuctionCup(self, isOn):
        if isOn:
            self.callAssociatedScriptFunction('redundantRobot', 'enableSuctionCup', vrep.simx_opmode_blocking, 'true')
        else:
            self.callAssociatedScriptFunction('redundantRobot', 'enableSuctionCup', vrep.simx_opmode_blocking, 'false')

    def isGrip(self):
        h_grabDummyParent = vrep.simxGetObjectHandle(self.clientID,
                                                     'uarmVacuumGripper_link2_dyn',
                                                     vrep.simx_opmode_blocking)[1]
        h_grabDummy = vrep.simxGetObjectHandle(self.clientID,
                                               'uarmVacuumGripper_loopDummyA',
                                               vrep.simx_opmode_blocking)[1]
        h_grabDummyParentNow = vrep.simxGetObjectParent(self.clientID, h_grabDummy, vrep.simx_opmode_blocking)[1]
        return not (h_grabDummyParent == h_grabDummyParentNow)

    def objCreation(self, position, ori):
        position = vrep_ext.toLuaStr_array(position)
        ori = vrep_ext.toLuaStr_array(ori)
        self.callAssociatedScriptFunction('box', 'objCreation', vrep.simx_opmode_blocking, position, ori)

    def createRandomObj(self, n):
        X = np.random.uniform(0, 1, n)
        Y = np.random.uniform(0, 0.5, n)
        ori_Z = np.random.uniform(0, 90, n)
        for x, y, ori_z in zip(X, Y, ori_Z):
            self.objCreation([x, y, 0.025], [0, 0, ori_z])

    def getImageFromCam(self, showImg=False):
        h_cam = vrep.simxGetObjectHandle(self.clientID, 'boxCam', vrep.simx_opmode_blocking)
        dimg = vrep.simxGetVisionSensorImage(0, h_cam[1], 0, vrep.simx_opmode_blocking)
        img = -np.reshape(npa(dimg[2]), [dimg[1][0], dimg[1][0], 3])
        # img = np.fliplr(img)
        img = np.flipud(img)
        if showImg:
            plt.imshow(img)
        return img

    def takePicture(self, filename, showImg=False):
        img = self.getImageFromCam(showImg)
        plt.imsave(filename, img)
        if showImg:
            plt.imshow(img)
        return img

    def getArmPosition(self):
        position = vrep.simxGetObjectPosition(self.clientID, self.h_arm, self.h_orig, vrep.simx_opmode_blocking)
        return position[1]

    def resetArmPosition(self):
        vrep.simxSetObjectPosition(self.clientID, self.h_arm, self.h_orig, self.position_init,
                                   vrep.simx_opmode_blocking)

    def getMovingLagDist(self):
        movingLagDist = vrep.simxReadDistance(self.clientID, self.h_movingLagDist, vrep.simx_opmode_blocking)[1]
        return movingLagDist

    def waitToDistination(self, minDist=0.004, timeOut=1):
        isReach = 0
        t0 = datetime.now()
        dt = (datetime.now() - t0).total_seconds()

        while (not isReach) and (dt < timeOut):
            isReach = self.getMovingLagDist() <= minDist
            dt = (datetime.now() - t0).total_seconds()
        return isReach
