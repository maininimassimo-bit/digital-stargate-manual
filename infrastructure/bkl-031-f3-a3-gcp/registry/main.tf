locals {
  labels = {
    capability = "bkl-031"
    increment  = "f3-a3"
    purpose    = "validation-spike"
    safety     = "none"
  }
}

resource "google_artifact_registry_repository" "spike" {
  project       = var.project_id
  location      = var.region
  repository_id = "dsg-f3-a3"
  description   = "Digest-pinned F3-A3 validation images."
  format        = "DOCKER"
  labels        = local.labels
}
