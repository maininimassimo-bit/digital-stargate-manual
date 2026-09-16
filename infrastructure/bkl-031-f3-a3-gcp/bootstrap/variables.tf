variable "project_id" {
  description = "Owner-selected Google Cloud project ID."
  type        = string
  nullable    = false

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{4,28}[a-z0-9]$", var.project_id))
    error_message = "project_id must be a valid Google Cloud project ID."
  }
}

variable "region" {
  description = "Approved Cloud Run region."
  type        = string
  default     = "europe-west8"

  validation {
    condition     = var.region == "europe-west8"
    error_message = "F3-A3 is approved only for europe-west8."
  }
}

variable "github_repository" {
  description = "Exact GitHub repository trusted by Workload Identity Federation."
  type        = string
  default     = "maininimassimo-bit/digital-stargate-manual"

  validation {
    condition     = var.github_repository == "maininimassimo-bit/digital-stargate-manual"
    error_message = "The WIF trust must remain scoped to the authoritative repository."
  }
}

variable "workload_identity_pool_id" {
  type    = string
  default = "dsg-f3-a3-github"
}

variable "workload_identity_provider_id" {
  type    = string
  default = "github-main"
}

variable "deployer_service_account_id" {
  type    = string
  default = "dsg-f3-a3-deployer"
}

variable "runtime_service_account_id" {
  type    = string
  default = "dsg-f3-a3-runtime"
}

variable "state_bucket_name" {
  description = "Globally unique private Terraform state bucket."
  type        = string
  nullable    = false
}

variable "data_bucket_name" {
  description = "Owner-approved private SPK/IERS data bucket."
  type        = string
  nullable    = false

  validation {
    condition     = var.data_bucket_name == "digital-stargate-telemetry-183451329061-f3-data"
    error_message = "F3-OD05 requires the exact owner-approved private data bucket."
  }
}

variable "evidence_bucket_name" {
  description = "Globally unique private evidence bucket."
  type        = string
  nullable    = false
}
