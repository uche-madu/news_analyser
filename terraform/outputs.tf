output "email" {
  description = "Service account email"
  value       = module.service_accounts.email
}

output "service_account" {
  description = "Service account resource"
  value       = module.service_accounts.service_account
}

output "iam_email" {
  description = "IAM-format service account email"
  value       = module.service_accounts.iam_email
}

output "key" {
  description = "Service account key"
  value       = module.service_accounts.key
  sensitive   = true
}