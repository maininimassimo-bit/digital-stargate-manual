locals {
  required_services = toset([
    "artifactregistry.googleapis.com",
    "compute.googleapis.com",
    "iam.googleapis.com",
    "iamcredentials.googleapis.com",
    "run.googleapis.com",
    "serviceusage.googleapis.com",
    "sts.googleapis.com",
    "storage.googleapis.com",
  ])

  deployer_project_roles = toset([
    "roles/artifactregistry.admin",
    "roles/compute.networkAdmin",
    "roles/run.admin",
    "roles/serviceusage.serviceUsageConsumer",
  ])
}

resource "google_project_service" "required" {
  for_each = local.required_services

  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}

resource "google_service_account" "deployer" {
  project      = var.project_id
  account_id   = var.deployer_service_account_id
  display_name = "Digital StarGate F3-A3 Terraform deployer"

  depends_on = [google_project_service.required]
}

resource "google_service_account" "runtime" {
  project      = var.project_id
  account_id   = var.runtime_service_account_id
  display_name = "Digital StarGate F3-A3 Cloud Run runtime"

  depends_on = [google_project_service.required]
}

resource "google_iam_workload_identity_pool" "github" {
  project                   = var.project_id
  workload_identity_pool_id = var.workload_identity_pool_id
  display_name              = "Digital StarGate F3-A3 GitHub"
  description               = "OIDC trust for the authoritative repository main branch only."
  disabled                  = false

  depends_on = [google_project_service.required]
}

resource "google_iam_workload_identity_pool_provider" "github" {
  project                            = var.project_id
  workload_identity_pool_id          = google_iam_workload_identity_pool.github.workload_identity_pool_id
  workload_identity_pool_provider_id = var.workload_identity_provider_id
  display_name                       = "GitHub main branch"
  disabled                           = false

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.repository" = "assertion.repository"
    "attribute.ref"        = "assertion.ref"
  }

  attribute_condition = format(
    "assertion.repository == '%s' && assertion.ref == 'refs/heads/main'",
    var.github_repository,
  )

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

resource "google_service_account_iam_member" "github_impersonation" {
  service_account_id = google_service_account.deployer.name
  role               = "roles/iam.workloadIdentityUser"
  member = format(
    "principalSet://iam.googleapis.com/%s/attribute.repository/%s",
    google_iam_workload_identity_pool.github.name,
    var.github_repository,
  )
}

resource "google_project_iam_member" "deployer" {
  for_each = local.deployer_project_roles

  project = var.project_id
  role    = each.value
  member  = format("serviceAccount:%s", google_service_account.deployer.email)
}

resource "google_service_account_iam_member" "deployer_uses_runtime" {
  service_account_id = google_service_account.runtime.name
  role               = "roles/iam.serviceAccountUser"
  member             = format("serviceAccount:%s", google_service_account.deployer.email)
}

resource "google_storage_bucket" "state" {
  project                     = var.project_id
  name                        = var.state_bucket_name
  location                    = var.region
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  force_destroy               = false

  versioning {
    enabled = true
  }

  depends_on = [google_project_service.required]
}

resource "google_storage_bucket" "data" {
  project                     = var.project_id
  name                        = var.data_bucket_name
  location                    = var.region
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  force_destroy               = false

  versioning {
    enabled = true
  }

  depends_on = [google_project_service.required]
}

resource "google_storage_bucket" "evidence" {
  project                     = var.project_id
  name                        = var.evidence_bucket_name
  location                    = var.region
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  force_destroy               = false

  versioning {
    enabled = true
  }

  depends_on = [google_project_service.required]
}

resource "google_storage_bucket_iam_member" "state_deployer" {
  bucket = google_storage_bucket.state.name
  role   = "roles/storage.objectAdmin"
  member = format("serviceAccount:%s", google_service_account.deployer.email)
}

resource "google_storage_bucket_iam_member" "data_deployer" {
  bucket = google_storage_bucket.data.name
  role   = "roles/storage.objectAdmin"
  member = format("serviceAccount:%s", google_service_account.deployer.email)
}

resource "google_storage_bucket_iam_member" "evidence_deployer" {
  bucket = google_storage_bucket.evidence.name
  role   = "roles/storage.objectAdmin"
  member = format("serviceAccount:%s", google_service_account.deployer.email)
}

resource "google_storage_bucket_iam_member" "data_runtime_reader" {
  bucket = google_storage_bucket.data.name
  role   = "roles/storage.objectViewer"
  member = format("serviceAccount:%s", google_service_account.runtime.email)
}

resource "google_storage_bucket_iam_member" "evidence_runtime_creator" {
  bucket = google_storage_bucket.evidence.name
  role   = "roles/storage.objectCreator"
  member = format("serviceAccount:%s", google_service_account.runtime.email)
}
