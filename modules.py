class Yamels(object):
    def __init__(self, deployments=[], rollouts=[]):
        self.deployments = deployments
        self.rollouts = rollouts
    def load(self):
        pass
    def save(self):
        pass
    def find(self, deploymentName):
        for d in self.deployments:
            if d.name == deploymentName:
                return d
        raise(KeyError(deploymentName))
    def sync(self, *deployments):
        print "Syncing:",
        # Record the deployments in-memory at least
        for d in deployments:
            try:
                self.find(d)
            except KeyError:
                self.deployments.append(d)
            print d,
        print

class Deployment(object):
    def __init__(self, name, replicas=0, primary=False):
        self.name = name
        self.primary = primary
        self.percent = 0
        self.replicas = replicas
    def __str__(self):
        return ("<Deployment %s, primary=%s, percent=%d, replicas=%d>" %
                (self.name, self.primary, self.percent, self.replicas))

def replaceVersion(deploymentName, targetVersion):
    if "--" in deploymentName:
        deploymentName, _ = deploymentName.split("--")
    return deploymentName + "--" + targetVersion

class Rollout(object):
    def __init__(self, yamels, deploymentName, targetVersion):
        self.yamels = yamels
        self.fromDeployment = self.yamels.find(deploymentName)
        self.originalReplicas = self.fromDeployment.replicas
        self.toDeployment = Deployment(
            replaceVersion(deploymentName, targetVersion),
            replicas=self.originalReplicas,
        )
    def stage(self):
        self.fromDeployment.percent = self.initialPercent
        self.toDeployment.percent = 100 - self.initialPercent
        self.yamels.sync(self.fromDeployment, self.toDeployment)
    def release(self):
        self.fromDeployment.primary = False
        self.toDeployment.primary = True
        self.fromDeployment.percent = 0
        self.toDeployment.percent = 100
        self.fromDeployment.replicas = 0
        self.yamels.sync(self.fromDeployment, self.toDeployment)
    def abort(self):
        self.fromDeployment.percent = 100
        self.toDeployment.percent = 0
        self.yamels.sync(self.fromDeployment, self.toDeployment)

class CanaryRollout(Rollout):
    initialPercent = 5
    def __init__(self, *a, **kw):
        return Rollout.__init__(self, *a, **kw)

class BlueGreenRollout(Rollout):
    initialPercent = 0
    def __init__(self, *a, **kw):
        return Rollout.__init__(self, *a, **kw)

# TODO: clean up old deployments, only really possible when flux
# supports deleting things.
