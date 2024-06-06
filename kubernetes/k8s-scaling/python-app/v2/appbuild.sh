
#docker build
docker build -t python-app-v2 .

#docker tag
docker tag python-app-v2 karthickponcloud/devopscourse:python-app-v2

#docker push
docker push karthickponcloud/devopscourse:python-app-v2
