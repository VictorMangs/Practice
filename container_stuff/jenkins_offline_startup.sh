#!/usr/bin/env bash

# Create jenkins network
podman network create jenkins

# Build jenkins with blue ocean
# podman build -t myjenkins-blueocean:2.426.2-1 -f Dockerfile.jenkins

# Run jenkins docker in docker
podman run --name jenkins-docker --rm --detach --privileged --network jenkins --network-alias docker --env DOCKER_TLS_CERTDIR=/certs --volume jenkins-docker-certs:/certs/client --volume jenkins-data:/var/jenkins_home --publish 2376:2376 docker:dind --storage-driver overlay2

# Set jenkins permission in jenkins-docker container
podman exec jenkins-docker /bin/sh -c "chown -R 1000:1000 /var/jenkins_home"

# Run jenkins-blueocean
podman run --name jenkins-blueocean --restart=on-failure --detach --network jenkins --env DOCKER_HOST=tcp://docker:2376 --env DOCKER_CERT_PATH=/certs/client --env DOCKER_TLS_VERIFY=1 --publish 8080:8080 --publish 50000:50000 --volume jenkins-data:/var/jenkins_home --volume jenkins-docker-certs:/certs/client:ro myjenkins-blueocean:2.426.2-1

# Get admin password
podman exec jenkins-blueocean /bin/cat /var/jenkins_home/secrets/initialAdminPassword