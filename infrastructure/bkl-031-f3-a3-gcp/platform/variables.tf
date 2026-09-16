variable "project_id" {
  type     = string
  nullable = false
}

variable "region" {
  type    = string
  default = "europe-west8"

  validation {
    condition     = var.region == "europe-west8"
    error_message = "F3-A3 is approved only for europe-west8."
  }
}

variable "runtime_service_account_email" {
  type     = string
  nullable = false
}

variable "deployer_service_account_email" {
  type     = string
  nullable = false
}

variable "data_bucket_name" {
  type     = string
  nullable = false
}

variable "evidence_bucket_name" {
  type     = string
  nullable = false
}

variable "container_image_digest" {
  description = "Immutable Artifact Registry image reference."
  type        = string
  nullable    = false

  validation {
    condition     = can(regex("@sha256:[0-9a-f]{64}$", var.container_image_digest))
    error_message = "container_image_digest must end with an immutable sha256 digest."
  }
}

variable "kernel_artifact_sha256" {
  type      = string
  nullable  = false
  sensitive = true

  validation {
    condition     = can(regex("^[0-9a-f]{64}$", var.kernel_artifact_sha256))
    error_message = "F3-OD05 requires an exact lowercase SHA-256."
  }
}

variable "iers_artifact_sha256" {
  type      = string
  nullable  = false
  sensitive = true

  validation {
    condition     = can(regex("^[0-9a-f]{64}$", var.iers_artifact_sha256))
    error_message = "The IERS snapshot requires an exact lowercase SHA-256."
  }
}

variable "owner_decision_ref" {
  description = "Exact repository decision evidence reference."
  type        = string
  nullable    = false

  validation {
    condition     = length(trimspace(var.owner_decision_ref)) >= 12 && !can(regex("(?i)replace|todo|pending", var.owner_decision_ref))
    error_message = "owner_decision_ref must be exact and non-placeholder."
  }
}

variable "job_name" {
  type    = string
  default = "dsg-f3-a3-spike"
}

variable "subnet_cidr" {
  type    = string
  default = "10.88.0.0/28"
}
