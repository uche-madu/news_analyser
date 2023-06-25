variable "project" {
  description = "The ID of the project in which to provision resources."
  type        = string
}

variable "credentials_file" {}

variable "region" {
  default = "us-central1"
}

variable "zone" {
  default = "us-central1-c"
}

variable "prefix" {
  type        = string
  description = "Prefix applied to service account names."
  default     = ""
}

# variable "terraform_state_bucket" {
#   type = string
#   description = "GCS bucket for remote storage of terraform state"
# }

variable "gcp_services" {
  type        = list(any)
  description = "GCP services to enable"
}