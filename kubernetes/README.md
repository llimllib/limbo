Kubernetes and Secrets
======================
Kubernetes has in-built support for handling secrets in a cluster.

How do I update secrets?
========================
  1. (optional) if you are committing this to a git repo, you may want to use blackbox (https://github.com/stackexchange/blackbox) to encrypt those secrets.  Initialize your blackbox inside repo.
  2. edit limbo.env (`blackbox_edit limbo.env` in the case of blackbox)
  3. commit the change, if needed.
  4. execute `recreate_secrets.sh` which should delete and recreate an opaque secret in Kubernetes, named `limbo-secret-env-vars`
  5. delete the currently running Limbo pod to propogate the new secret (restarting a pod won't fetch a new secret)


