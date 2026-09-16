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
  description = "Owner-approved private SPK/IERS data bucket."
  type        = string
  nullable    = false

  validation {
    condition     = var.data_bucket_name == "digital-stargate-telemetry-183451329061-f3-data"
    error_message = "F3-OD05 requires the exact owner-approved private data bucket."
  }
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
    condition     = var.kernel_artifact_sha256 == "54d97562a5b094d298b1b8eafa5a2e17e3e010ce85e1a366d07f003ad159323c"
    error_message = "F3-OD05 requires the owner-approved de442s.bsp SHA-256."
  }
}

variable "kernel_artifact_uri" {
  description = "Owner-approved private content-addressed de442s.bsp URI."
  type        = string
  nullable    = false

  validation {
    condition     = var.kernel_artifact_uri == "gs://digital-stargate-telemetry-183451329061-f3-data/bkl-031/f3-a3/artifacts/spk/de442s/sha256/54d97562a5b094d298b1b8eafa5a2e17e3e010ce85e1a366d07f003ad159323c/de442s.bsp"
    error_message = "F3-OD05 requires the exact owner-approved private content-addressed URI."
  }
}

variable "method_profile_sha256" {
  description = "Exact reviewed ARB-213-MI01 method-profile digest."
  type        = string
  nullable    = false

  validation {
    condition     = var.method_profile_sha256 == "e69f60e5ed7f71cd982437f6ca3556b732d6ae9a46718995134aa64a7b7f67ca"
    error_message = "ARB-213-MI01 requires the exact reviewed method-profile SHA-256."
  }
}

variable "method_profile_path" {
  description = "Path of the immutable method profile embedded in the future container image."
  type        = string
  nullable    = false

  validation {
    condition     = var.method_profile_path == "/app/dsg/method-profile/BKL-031-F3-A3-METHOD-PROFILE-001.json"
    error_message = "The future container must expose the reviewed method profile at the exact preflight path."
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
    condition     = var.owner_decision_ref == "BKL-031-F3-A3-F3-OD05-APPROVAL-2026-09-16"
    error_message = "owner_decision_ref must identify the exact approved F3-OD05 decision."
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
