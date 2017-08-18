# fluxctl-rollout

fluxctl-rollout is a prototype of a hypothetical fluxctl rollout subcommand.

It operates directly on Istio-Kubernetes yaml files only and assumes
[gitops](https://www.weave.works/blog/gitops-operations-by-pull-request) for
the rest.  All state required is stored in annotations on Deployment objects
(probably).

It could later be integrated into Flux so that it runs server-side (in the
user's cluster) at the point where Flux is operating on checked-out yaml files
from the source of truth config repo.

https://docs.google.com/document/d/1Mf13PgRWrouc1Ly6IkenDgFkqS7-4jtPf6B5ofrVHXk/edit#heading=h.kg8bv2nefkii

Basic workflow:

```
stage -> (check) -> release
                 \-> abort

```

# Usage:

## Blue-green

```
$ fluxctl-rollout stage bluegreen --update-image=myapp:master-8da5ca3
Rollout id: a1b2c3d4e5
Old tag: myapp:master-7c04b92
New tag: myapp:master-8da5ca3
URL for new tag: http://blah:39191/
Use 'fluxctl-rollout abort a1b2c3d4e5' to cancel, or 'fluxctl-rollout release a1b2c3d4e5' to finish the rollout.

$ fluxctl-rollout release a1b2c3d4e5
Completing rollout... done.
100% user traffic now reaching New deployment.
Cleaning up Old deployment... done

$ fluxctl-rollout list
<shows in-flight rollouts>
```

## Canary

```
$ fluxctl-rollout stage canary --update-image=myapp:master-8da5ca3
Rollout id: a1b2c3d4e5
Old tag: myapp:master-7c04b92
New tag: myapp:master-8da5ca3
5% of traffic is now being routed to master-8da5ca3.
Check your monitoring to see if you like the new version.
Use 'fluxctl-rollout a1b2c3d4e5 abort' to cancel, or 'fluxctl-rollout a1b2c3d4e5 complete' to finish the rollout.

$ fluxctl-rollout release a1b2c3d4e5
Completing rollout... done.
100% user traffic now reaching New deployment.
Cleaning up Old deployment... done
```
