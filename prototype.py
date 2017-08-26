# A prototype for the data structures & organization of the
# prototype. For discussion, then will spell out as a more complete
# implementation in Golang.
#
# Read main(), then run me to see the output...

from modules import (Deployment, Yamels, CanaryRollout,
        BlueGreenRollout)

def main():
    y = Yamels([Deployment("front-end", replicas=7, primary=True)])
    # Scenario 1 - stage and release
    r = CanaryRollout(y, "front-end", "v2")
    r.stage()
    r.release()
    # Scenario 2 - stage and abort
    r = BlueGreenRollout(y, "front-end--v2", "v3")
    r.stage()
    r.abort()

"""
action      | deployment:replicas,traffic%,[* = primary]
--------------------------------------------------------
init(v2)    | front-end*:n,100%
canary()    | front-end*:n,95%, front-end--v2:n,5%
Syncing: <Deployment front-end, primary=True, percent=95, replicas=7> <Deployment front-end--v2, primary=False, percent=5, replicas=7>

release()   | front-end:0,0%, front-end--v2*:n,100%
Syncing: <Deployment front-end, primary=False, percent=0, replicas=0> <Deployment front-end--v2, primary=True, percent=100, replicas=7>

init(v3)    | front-end--v2*:n,100%
bluegreen() | front-end--v2*:n,100%, front-end--v3:n,0%
Syncing: <Deployment front-end--v2, primary=True, percent=100, replicas=7> <Deployment front-end--v3, primary=False, percent=0, replicas=7>

abort()     | front-end--v2*:n,100%, front-end--v3:0,0%
Syncing: <Deployment front-end--v2, primary=True, percent=100, replicas=7> <Deployment front-end--v3, primary=False, percent=0, replicas=0>
"""

if __name__ == "__main__":
    main()
