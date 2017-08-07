from VrepPythonApi import vrep
from VrepPythonApi import vrep_ext
import os

# ============================================================================ #
#                                  Start VREP                                  #
# ============================================================================ #
path_vrep = '"C:\\Program Files\\V-REP3\V-REP_PRO\\vrep.exe"'
os.startfile(path_vrep)

# ============================================================================ #
#                               Start simulation                               #
# ============================================================================ #
v = vrep_ext.VrepController()
v.startSim()
v.restartSim()

# ============================================================================ #
#                            Call build-in function                            #
# ============================================================================ #
# create objects
h_cube = v.callBuildinFunction('simCreatePureShape', vrep.simx_opmode_blocking,
                               '0', '8', '{0.1, 0.1, 0.1}', '1')[1]

# ============================================================================ #
#                           Call child scrip function                          #
# ============================================================================ #

# ---
# create a dummy and attach a script with the following content
# ---
# function f(title, text)
#     simDisplayDialog(title, text, 0, false)
# end
# ---------------------------------------------------------------------------- #
v.callAssociatedScriptFunction('Dummy', 'f', vrep.simx_opmode_blocking, '"a"', '"b"')


# ============================================================================ #
#                                      End                                     #
# ============================================================================ #
v.stopSim()
