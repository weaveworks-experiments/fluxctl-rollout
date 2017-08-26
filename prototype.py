# A prototype for the data structures & organization of the
# prototype. For discussion, then will spell out as a more complete
# implementation in Golang.
#
# Read main(), then run me to see the output...

from modules import (Deployment, Yamels, CanaryRollout,
        BlueGreenRollout)

def main():
    y = Yamels([Deployment("front-end", replicas=7)])
    # Scenario 1 - stage and release
    r = CanaryRollout(y, "front-end", "v2")
    r.stage()
    r.release()
    # Scenario 2 - stage and abort
    r = BlueGreenRollout(y, "front-end", "v3")
    r.stage()
    r.abort()

"""
action      | deployment:replicas,traffic%,[* = primary]
--------------------------------------------------------
init(v2)    | front-end*:n,100%
stage()     | front-end*:n,100%, front-end--v2:n,0%
release()   | front-end:0,0%, front-end--v2*:n,100%
init(v3)    | front-end:0,0%, front-end--v2*:n,100%
stage()     | front-end:0,0%, front-end--v2*:n,100%, front-end--v3:n,0%
release()   | front-end:0,0%, front-end--v2:0,0%, front-end--v3*:n,100%
"""

if __name__ == "__main__":
    main()
