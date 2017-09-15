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
nObj = 20

# ============================================================================ #
#                               Connect to V-rep                               #
# ============================================================================ #
arm = ArmDemo()
arm.restartSim()

position = [0, 0, 0]
ori = [0, 0, 0]

position = '{0, 0, 0}'
ori = '{0, 0, 0}'

arm.createRandomObj(40)
arm.objCreation([0, 0, 0], [0,0,0])
h_obj = vrep_ext.callAssociatedScriptFunction(0, 'box', 'objCreation', vrep.simx_opmode_blocking, position, ori)

vrep_ext.callAssociatedScriptFunction(0, 'box', 'objCreation', vrep.simx_opmode_blocking, '{0, 0, 0}', '{0,0,0}')
vrep_ext.callAssociatedScriptFunction(0, 'Dummy', 'a', vrep.simx_opmode_blocking)