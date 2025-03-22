provider "google" {
  project = "cloudk8sa3"  # Replace with your GCP project ID
  region  = "us-central1"
  zone    = "us-central1-c"  # Specify the zone explicitly
}

resource "google_container_cluster" "primary" {
  name     = "my-cluster"
  location = "us-central1-c"  # Ensure this matches the zone of your Persistent Disk

  # Remove the default node pool and create a custom one
  remove_default_node_pool = true
  initial_node_count       = 1
}

resource "google_container_node_pool" "primary_nodes" {
  name       = "my-node-pool"
  location   = "us-central1-c"  # Ensure this matches the zone of your Persistent Disk
  cluster    = google_container_cluster.primary.name
  node_count = 1

  node_config {
    preemptible  = true  # Use preemptible VMs to save costs
    machine_type = "e2-medium"  # Increased to e2-medium for more resources
    disk_size_gb = 20  # Increased disk size
    image_type   = "cos_containerd"  # Container-Optimized OS with containerd

    # Ensure the node has the necessary permissions
    oauth_scopes = [
      "https://www.googleapis.com/auth/devstorage.read_only",
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
      "https://www.googleapis.com/auth/service.management.readonly",
      "https://www.googleapis.com/auth/servicecontrol",
      "https://www.googleapis.com/auth/trace.append",
      "https://www.googleapis.com/auth/compute",
    ]
  }

  autoscaling {
    min_node_count = 1
    max_node_count = 3
  }
}
