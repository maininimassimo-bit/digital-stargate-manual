output "cloud_run_job_name" {
  value = google_cloud_run_v2_job.spike.name
}

output "network_name" {
  value = google_compute_network.spike.name
}
