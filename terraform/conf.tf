# Configuration for the cluster
# Data resources at vkcs provider

data "vkcs_kubernetes_clustertemplate" "ct" {
  version = "1.22.6"
}

data "vkcs_networking_subnet" "k8s-subnetwork" {
  # the subnetwork is already present in the cloud
  name = "subnet_8551"
}

data "vkcs_networking_network" "k8s" {
  # this network was created manually when
  # the resources for the first cluster was allocated
  name = "kubernetes-cluster-3980"
}

data "vkcs_networking_router" "k8s" {
  name = "router_1526"
}

data "vkcs_compute_flavor" "master_flavor" {
  # Hardware configuration for the master node:
  # 2 CPU, 4Gb RAM, 50Gb of disk space
  name = "Standard-2-4-50"
}

data "vkcs_compute_flavor" "node_flavor" {
  # Hardware configuration for the worker node
  # 1 CPU, 2Gb RAM, 20Gb of disk space
  name = "Basic-1-2-20"
}
