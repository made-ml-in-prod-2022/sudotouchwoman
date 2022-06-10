# __Kubernetes__

This section contains `k8s` manifests created to work with the application
from `online_inference` section. The `README` shows the results of my experiments.

__VK Cloud Platform__ was used to host the cluster (it is really nice of them
to provide a trial with free balance for testing!). After signing up for their platform I
created a cluster with 3 worker nodes and a single master node. They provide a `kubeconfig` file
to access the cluster in CLI. Moreover, `VSCode` has an extension for k8s with a nice UI.
I could have used `Lens` to monitor and configure the cluster, but it would have implied much headache
as I primarily work through WSL2.

### __Cluster at VK Cloud Solutions__

![Cluster at VKCP](./screenshots/vk-cloud-platform.jpg)

### __Connecting to the cluster__

![Connecting to cluster](./screenshots/k8s-cluster.jpg)

### __Creating the first Pod__

![First Pod](./screenshots/first-pod.jpg)

As the second step, manifest was modified to sleep for about half a minute before launching the server.
Then, a simple trick was used to cause an error and `pod` was stopped.

### __Pods with ConfigMap__

Kubernetes encourages one to separate the data from application logic. For instance,
`pod` can be configured on startup through envars or mounted config files. The prior may be looked up
from `ConfigMap` entity, a key-value storage for non-sensitive information:

![ConfigMap](./screenshots/config-map.jpg)

### __SSH tunelling and port forwarding__

With k8s extension for `VSCode` it was quite easy to terminal into the running pod and therefore
access its internals (say, logs). For such debugging purposes it is appropriate, however, tunelling
or port forwarding into pods is generally discouraged and considered a bad practice.

![SSH](./screenshots/ssh-tunelling.jpg)
