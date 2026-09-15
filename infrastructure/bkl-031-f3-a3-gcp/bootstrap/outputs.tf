output "workload_identity_provider" {
  value       = google_iam_workload_identity_pool_provider.github.name
  description = "Use as GCP_WIF_PROVIDER."
}

output "deployer_service_account_email" {
  value       = google_service_account.deployer.email
  description = "Use as GCP_DEPLOY_SERVICE_ACCOUNT."
}

output "runtime_service_account_email" {
  value       = google_service_account.runtime.email
  description = "Use as GCP_RUNTIME_SERVICE_ACCOUNT."
}

output "state_bucket_name" {
  value = google_storage_bucket.state.name
}

output "data_bucket_name" {
  value = google_storage_bucket.data.name
}

output "evidence_bucket_name" {
  value = google_storage_bucket.evidence.name
}
