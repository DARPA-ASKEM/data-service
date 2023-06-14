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
  targets = ["data-service", "data-service-dev-db", "data-service-storage", "data-service-migrations"]
}

group "default" {
  targets = ["data-service-base", "data-service-dev-db-base", "data-service-storage-base", "data-service-migrations-base"]
}

# ----------------------------------------------------------------------------------------------------------------------

target "_platforms" {
  platforms = ["linux/amd64", "linux/arm64"]
}

target "data-service-base" {
	context = "."
	tags = tag("data-service", "", "")
	dockerfile = "docker/Dockerfile"
}

target "data-service-dev-db-base" {
	context = "."
	tags = tag("data-service-dev-db", "", "")
	dockerfile = "docker/Dockerfile-dev-db"
}

target "data-service-storage-base" {
	context = "."
	tags = tag("data-service-storage", "", "")
	dockerfile = "docker/Dockerfile.minio"
}

target "data-service-graphdb-base" {
  context = "."
  tags = tag("data-service-graphdb", "", "")
  dockerfile = "docker/Dockerfile.neo4j"
}

target "data-service-migrations-base" {
  context = "."
  tags = tag("data-service-migrations", "", "")
  dockerfile = "docker/Dockerfile.migrations"
}

target "data-service" {
  inherits = ["_platforms", "data-service-base"]
}

target "data-service-dev-db" {
  inherits = ["_platforms", "data-service-dev-db-base"]
}

target "data-service-storage" {
  inherits = ["_platforms", "data-service-storage-base"]
}

target "data-service-graphdb" {
  inherits = ["_platforms", "data-service-graphdb-base"]
}

target "data-service-migrations" {
  inherits = ["_platforms", "data-service-migrations-base"]
}
