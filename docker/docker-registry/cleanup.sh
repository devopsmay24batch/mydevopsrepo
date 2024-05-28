echo "Remove the containers from the system"
docker rm -f $(docker ps -aq)
echo "Remove the images from the system"
docker rmi $(docker images -q)
