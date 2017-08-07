# def callAssociatedScriptFunction(clientID, objName, functionName, operationMode, *args):
argStr = ', '.join(['{1,1,1}'])
objName = 'redundantRobot'
functionName = 'moveTo'
s = "h = simGetScriptHandle('{:s}')\nsimCallScriptFunction('{:s}', h, {:s})".format(objName, functionName,
                                                                                    argStr)
emptyBuff = bytearray()
vrep.simxCallScriptFunction(0,
                            "remoteApiCommandServer", vrep.sim_scripttype_childscript,
                            'executeCode_function',
                            [], [], [s],
                            emptyBuff,
