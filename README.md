# RESTfull-app

# Current weather REST Application
this Flask Application enable you to get the weather of cities around the world and fetch  their information such as population,latitude and longitude.
You should type the latitude and longitude.

# Setup
The assumption is you have a Cassandra cluster setup already, with a keyspace called "city" and a table called "city" loaded from the csv file provided "worldcities.csv". Steps to create and load this file is provided in the appendix below.

# Initial setup:
1.External API registration:
https://developers.breezometer.com/

create a file called ‘config.py’ in the root folder and edit the file like follow:
DEBUG=True
2.Create a folder called ‘instance’ 
1. create a file called ‘config.py’ 
2. edit the file like below:
DEBUG=True
MY_API_KEY=”your API key”

# RESTfull app:
This application provides the current weather data of each city via a REST API. http://{Hostname}/currnetweather?latitude=&longitude=
example: http://34.65.181.39/currentweather?latitude=59&longitude=10

# Deploying on GCP:
1. set your project id and zone:
```
gcloud config set project ${PROJECT_ID} // my project id is layegh-195606
```
```
gcloud config set compute/zone  europe-west6-c
```
2. build our docker image:
```
 docker build -t gcr.io/${PROJECT_ID}/weather-app:v1 .
 ```
3. Push our docker image:
```
docker push gcr.io/${PROJECT_ID}/weather-app:v1
```
4. creating a 3node container cluster (cassandra):
```
gcloud container clusters create cassandra --num-nodes=3--machine-type "n1-standard-2"
```
5. deploy our application 
```
kubectl run weather-app --image=gcr.io/${PROJECT_ID}/pokemon-app:v1
--port 8080
```
6. to expose the deployment to get an External IP adress we need to create a service:
```
kubectl expose deployment weather-app --type=LoadBalancer --port 80
--target-port 8080
```
7. see the pods created:
```
kubectl get pods
```
8. get the external IP address that is assigned to our deployment :
```
kubectl get services
```
```
example: my ip address was: http://34.65.181.39/
```

to see the status of our deployment we can check this command:
```
kubectl get deployment cassandra
```
If all is fine, it could be that the firewall ruleset does not allow external
HTTP requests to our load-balancer. Check the firewall ruleset by issuing:
```
gcloud compute firewall-rules list
```
Look for a line that allows INGRESS for "DIRECTION" and for "ALLOW" it
should be tcp:80 and for "DISABLED" should be False.

