#this script will pull the nagios image from docker hub and then run with the default config

#Pull the image
docker pull jasonrivers/nagios:latest

#run it. adjust the host/node port 8080 if it is already in use by Jenkins.

docker run --name nagios4 -p 0.0.0.0:8081:80 jasonrivers/nagios:latest


#access the nagios console using http://localhost:8080
#username: nagiosadmin
#password: nagiosadmin or try admin


#Enjoy learning Nagios without having to go through complex process
