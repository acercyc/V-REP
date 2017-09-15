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

# ============================================================================ #
#                               Connect to V-rep                               #
# ============================================================================ #
arm = ArmDemo('192.168.1.170')
arm.stopSim()

arm.restartSim()

x = 0.5 + 0.25
arm.moveTo([x, 0.25, 0.2])
arm.waitToDistination()
waitSecs(1)
arm.moveTo([x, 0.25, 0.055])
arm.waitToDistination()
waitSecs(2)

arm.enableSuctionCup(1)
waitSecs(2)
arm.moveTo([0.5, 0.5, 0.5])
waitSecs(2)

arm.moveTo([0, -1, 0.8])
arm.enableSuctionCup(0)
