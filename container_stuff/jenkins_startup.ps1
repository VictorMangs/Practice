# Create jenkins network
# podman network create jenkins
$pull_image = "docker.io/jenkins/jenkins:rhel-ubi9-jdk17"
$jenkins_name = "jenkins-blueocean"

# Build jenkins with blue ocean
# podman build -t $jenkins -f $dockerfile --build-arg IMAGE_TAG=$version

# Create jenkins network
podman network create jenkins

# Run jenkins docker in docker
podman run --name jenkins-docker --rm --detach --privileged --network jenkins --network-alias docker --env DOCKER_TLS_CERTDIR=/certs --volume jenkins-docker-certs:/certs/client --volume jenkins-data:/var/jenkins_home --publish 2376:2376 docker:dind --storage-driver overlay2

# Run jenkins-blueocean
podman run --name $jenkins_name --restart=on-failure --detach --network jenkins --env DOCKER_HOST=tcp://docker:2376 --env DOCKER_CERT_PATH=/certs/client --env DOCKER_TLS_VERIFY=1 --publish 8080:8080 --publish 50000:50000 --volume jenkins-data:/var/jenkins_home --volume jenkins-docker-certs:/certs/client:ro $pull_image

# Get admin password
$password = podman exec $jenkins_name /bin/cat /var/jenkins_home/secrets/initialAdminPassword
echo "Jenkins startup password is: $password"