output "cloud_run_job_name" {
  value = google_cloud_run_v2_job.spike.name
}

output "artifact_registry_repository" {
  value = google_artifact_registry_repository.spike.name
}

output "network_name" {
  value = google_compute_network.spike.name
}
