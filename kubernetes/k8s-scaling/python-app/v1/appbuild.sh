
#docker build
docker build -t python-app-v1 .

#docker tag
docker tag python-app-v1 karthickponcloud/devopscourse:python-app-v1

#docker push
docker push karthickponcloud/devopscourse:python-app-v1
