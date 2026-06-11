variable "aws_region" {
  default     = "eu-west-3" # Remplace par ta région AWS (ex: eu-west-3 pour Paris)
  type        = string
}

variable "key_name" {
  default     = "fastapi_aws" # Le nom EXACT de ta paire de clés .pem sur AWS
  type        = string
}