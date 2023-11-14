provider "aws" {
  region     = var.region
  access_key = local.envs["AWS_ACCESS_KEY"]
  secret_key = local.envs["AWS_SECRET_KEY"]
}
