variable "DOCKER_REGISTRY" {
  default = "ghcr.io"
}
variable "DOCKER_ORG" {
  default = "darpa-askem"
}
variable "VERSION" {
  default = "local"
}

# ----------------------------------------------------------------------------------------------------------------------

function "tag" {
  params = [image_name, prefix, suffix]
  result = [ "${DOCKER_REGISTRY}/${DOCKER_ORG}/${image_name}:${check_prefix(prefix)}${VERSION}${check_suffix(suffix)}" ]
}

function "check_prefix" {
  params = [tag]
  result = notequal("",tag) ? "${tag}-": ""
}

function "check_suffix" {
  params = [tag]
  result = notequal("",tag) ? "-${tag}": ""
}

# ----------------------------------------------------------------------------------------------------------------------

group "prod" {
  targets = ["data-service"]
}

group "default" {
  targets = ["data-service-base", "data-service-dev-db"]
}

# ----------------------------------------------------------------------------------------------------------------------

target "_platforms" {
  platforms = ["linux/amd64", "linux/arm64"]
}

target "data-service-base" {
	context = "."
	tags = tag("data-service", "", "")
	dockerfile = "Dockerfile"
}

target "data-service-dev-db" {
	context = "."
	tags = tag("data-service-dev-db", "", "")
	dockerfile = "Dockerfile-dev-db"
}

target "data-service" {
  inherits = ["_platforms", "data-service-base"]
}
