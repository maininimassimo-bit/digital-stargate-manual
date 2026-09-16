variable "project_id" {
  type     = string
  nullable = false

  validation {
    condition     = var.project_id == "digital-stargate-telemetry"
    error_message = "F3-A3 is approved only for the governed Google Cloud project."
  }
}

variable "region" {
  type    = string
  default = "europe-west8"

  validation {
    condition     = var.region == "europe-west8"
    error_message = "F3-A3 is approved only for europe-west8."
  }
}
