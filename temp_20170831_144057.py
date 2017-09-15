import matplotlib.pyplot as plt
import numpy as np
from numpy import array as npa

from VrepPythonApi import vrep
from VrepPythonApi import vrep_ext
from armDemo import ArmDemo, waitSecs


arm = ArmDemo('192.168.1.170')
arm.getImageFromCam(True)
plt.show()
