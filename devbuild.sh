#!/bin/bash
source api.env && VERSION=dev-0.4.0 docker buildx bake
docker push ghcr.io/darpa-askem/data-service:dev-0.4.0
docker push ghcr.io/darpa-askem/data-service-storage:dev-0.4.0
docker push ghcr.io/darpa-askem/data-service-dev-db:dev-0.4.0
