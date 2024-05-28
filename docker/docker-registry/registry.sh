#this script executes series of docker commands to illustrate how docker registry can be hosted on the local system.
#This registry will be private useful to host private images from an organiation to save cost for DockerHub.

echo "Pulling registry image"
docker pull registry:2
echo "Run the registry image with 5000 port"
docker run -d -p 5000:5000 --restart=always --name registry registry:2
echo "Pull another Ubuntu OS image"
docker pull ubuntu
echo "Tagging the ubuntu image for the local registry"
docker tag ubuntu localhost:5000/ubuntu
echo "Push the tagged image to the local registry"
docker push localhost:5000/ubuntu
echo "Verify the images both localhost and remote"
docker images
echo " Remove the image from the local cache "
docker rmi ubuntu
echo "Pull the image now from local registry"
docker pull localhost:5000/ubuntu
echo "Run the Ubuntu image and geton to bash"
docker run -it --rm localhost:5000/ubuntu /bin/bash


