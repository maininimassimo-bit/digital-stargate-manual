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

resource "google_compute_network" "spike" {
  project                 = var.project_id
  name                    = "dsg-f3-a3-private"
  auto_create_subnetworks = false
  routing_mode            = "REGIONAL"
}

resource "google_compute_subnetwork" "spike" {
  project                  = var.project_id
  name                     = "dsg-f3-a3-private-ew8"
  region                   = var.region
  network                  = google_compute_network.spike.id
  ip_cidr_range            = var.subnet_cidr
  private_ip_google_access = true
}

resource "google_cloud_run_v2_job" "spike" {
  project             = var.project_id
  name                = var.job_name
  location            = var.region
  deletion_protection = true
  labels              = local.labels

  template {
    task_count  = 1
    parallelism = 1

    template {
      service_account = var.runtime_service_account_email
      timeout         = "120s"
      max_retries     = 0

      containers {
        image = var.container_image_digest

        resources {
          limits = {
            cpu    = "2"
            memory = "2Gi"
          }
        }

        env {
          name  = "DSG_EXECUTION_MODE"
          value = "VALIDATION_SPIKE"
        }

        env {
          name  = "DSG_SITE_PROFILE"
          value = "SYNTHETIC_ONLY"
        }

        env {
          name  = "DSG_EXTERNAL_PROVIDER_POLICY"
          value = "DENY"
        }

        env {
          name  = "DSG_DATA_BUCKET"
          value = var.data_bucket_name
        }

        env {
          name  = "DSG_EVIDENCE_BUCKET"
          value = var.evidence_bucket_name
        }

        env {
          name  = "DSG_KERNEL_SHA256"
          value = var.kernel_artifact_sha256
        }

        env {
          name  = "DSG_KERNEL_URI"
          value = var.kernel_artifact_uri
        }

        env {
          name  = "DSG_IERS_SHA256"
          value = var.iers_artifact_sha256
        }

        env {
          name  = "DSG_OWNER_DECISION_REF"
          value = var.owner_decision_ref
        }

        env {
          name  = "DSG_MAX_TARGETS"
          value = "50"
        }

        env {
          name  = "DSG_MAX_INSTANTS_PER_TARGET"
          value = "2016"
        }

        env {
          name  = "DSG_MAX_TARGET_INSTANT_PAIRS"
          value = "10000"
        }

        env {
          name  = "DSG_MAX_SPAN_DAYS"
          value = "7"
        }

        env {
          name  = "DSG_MIN_GRID_STEP_SECONDS"
          value = "60"
        }

        env {
          name  = "DSG_MAX_REQUEST_BYTES"
          value = "262144"
        }
      }

      vpc_access {
        egress = "ALL_TRAFFIC"

        network_interfaces {
          network    = google_compute_network.spike.id
          subnetwork = google_compute_subnetwork.spike.id
        }
      }
    }
  }

  depends_on = [
    google_artifact_registry_repository.spike,
    google_compute_subnetwork.spike,
  ]
}

resource "google_cloud_run_v2_job_iam_member" "deployer_invoker" {
  project  = var.project_id
  location = google_cloud_run_v2_job.spike.location
  name     = google_cloud_run_v2_job.spike.name
  role     = "roles/run.invoker"
  member   = format("serviceAccount:%s", var.deployer_service_account_email)
}
