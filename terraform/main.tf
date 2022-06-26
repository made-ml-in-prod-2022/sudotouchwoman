# Resources required for the kubernetes cluster:
# the cluster resource itself (contains master node(s) and such settings as
# networking interfaces and availability zone(s))

resource "vkcs_kubernetes_cluster" "k8s-cluster" {
  name                = "terraform-managed-k8s"
  cluster_template_id = data.vkcs_kubernetes_clustertemplate.ct.id
  master_flavor       = data.vkcs_compute_flavor.master_flavor.id
  master_count        = 1

  network_id          = data.vkcs_networking_network.k8s.id
  subnet_id           = data.vkcs_networking_subnet.k8s-subnetwork.id
  floating_ip_enabled = true
  availability_zone   = "MS1"
}

resource "vkcs_kubernetes_node_group" "default_ng" {
  cluster_id = vkcs_kubernetes_cluster.k8s-cluster.id

  node_count          = 3
  name                = "default-group"
  flavor_id           = data.vkcs_compute_flavor.node_flavor.id
  availability_zones  = ["MS1"]
  autoscaling_enabled = false
  volume_type         = "ssd"
  volume_size         = 20

  labels {
    key   = "env"
    value = "test"
  }

  labels {
    key   = "disktype"
    value = "ssd"
  }
}
