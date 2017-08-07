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

clientID = vrep.simxStart('192.168.1.170', 19997, True, True, 5000, 5)  # Connect to V-REP
if clientID != -1:
    print('Connected to remote API server')
else:
    print('Failed connecting to remote API server')

vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot_wait)



def callFunc(clientID, objName, functionName, operationMode, *args):
    argStr = ', '.join(args)
    s = "h = simGetScriptHandle('{:s}')\nsimCallScriptFunction('{:s}', h, {:s})".format(objName, functionName, argStr)
    emptyBuff = bytearray()
    vrep.simxCallScriptFunction(clientID, "remoteApiCommandServer", vrep.sim_scripttype_childscript,
                                'executeCode_function', [], [], [s], emptyBuff, operationMode)
    return s

callFunc(clientID, 'Sphere', 'f', vrep.simx_opmode_blocking, '"aaa"', '"bbb"')




# ---------------------------------------------------------------------------- #
emptyBuff = bytearray()
h = vrep.handle('Sphere')
vrep.simxCallScriptFunction(clientID, 'Sphere', 1, 'f', [], [], ['a', 'b'], emptyBuff, vrep.simx_opmode_blocking)



callFunc(clientID, 'Sphere', 'f', vrep.simx_opmode_blocking, '"aaa"', '"bbb"')
simDisplayDialog('a', 'b', 1, )

s = "simDisplayDialog('a', 'b', 1, false)"


s = "h = simGetScriptHandle('Sphere')\n" \
    "simCallScriptFunction('f', h, 'a', 'b')"
emptyBuff = bytearray()
vrep.simxCallScriptFunction(clientID, "remoteApiCommandServer", vrep.sim_scripttype_childscript,
                            'executeCode_function', [], [], [s], emptyBuff, vrep.simx_opmode_blocking)


vrep.simxCallScriptFunction(clientID, 'uarm', 1,
                            'moveToPosition_api',
                            [],
                            [],
                            [],
                            emptyBuff,
                            vrep.simx_opmode_oneshot)


# ----------------------------------------------------------------------------
callAssociatedScriptFunction(clientID, 'uarm', 'moveToPosition', vrep.simx_opmode_blocking, '{180*math.pi/180,59*math.pi/180,84*math.pi/180,180*math.pi/180}', 'true')
callAssociatedScriptFunction(clientID, 'uarm', 'initialize', vrep.simx_opmode_blocking, '0', '0', '0', '0')

moveToPosition