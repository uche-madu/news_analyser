terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.70.0"
    }
  }

  backend "gcs" {
    bucket = "general-random-stuff"
    prefix = "terraform/state"
  }
}

# data "google_storage_bucket" "prnews_articles" {
#     name = "scrapy"
# }

# resource "google_cloud_storage" "prnews_articles" {

# }

# resource "google_service_account" "scrapy_sa" {
#   account_id   = "scrapy-sa"
#   display_name = "Scrapy Service Account"
#   description  = "Service account for scrapy projects"
# }

# locals {
#     gcp_services = [
#         "iam.googleapis.com",
#         "storage.googleapis.com",
#         "compute.googleapis.com",
#         "bigquery.googleapis.com",
#         "bigquerystorage.googleapis.com",
#         "serviceusage.googleapis.com"
#     ]
# }

resource "google_project_service" "gcp_services" {
  for_each = toset(var.gcp_services)
  service  = each.key
}

module "service_accounts" {
  source     = "terraform-google-modules/service-accounts/google"
  version    = "4.2.1"
  project_id = var.project
  prefix     = var.prefix
  names      = ["scrapy-sa"]
  project_roles = [
    "${var.project}=>roles/storage.objectCreator",
    "${var.project}=>roles/storage.objectViewer",
    "${var.project}=>roles/bigquery.user"
  ]
  display_name  = "Scrapy Service Account"
  description   = "Service account for scrapy projects"
  generate_keys = true
  depends_on    = [google_project_service.gcp_services]
}
