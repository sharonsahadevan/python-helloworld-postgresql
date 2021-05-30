# python-helloworld-postgresql

sample python app that shows you how to connect to a PostgreSQL database deployed in Kubernetes. 

## Running the app on Kubernetes

1. Create the kubernetes cluster in any cloud you choose. (ie:EKS)

2. Setup Kubectl in you local host

    The IBM Cloud CLI tool tool is what you'll use to communicate with IBM Cloud from your terminal or command line.

3. Deploy postgresql using Helm charts


4. Create kubernetes secrets to store databse credential which can be used by the sample app.


5. clone the python-helloworld-postgresql
   
```
    git clone -b python git@github.com:IBM-Cloud/clouddatabases-helloworld-kubernetes-examples.git
```

6. `cd` into this newly created directory, and `cd` into the `postgresql` folder. The code for connecting to the service, and reading from and updating the database can be found in `server.py`. There's also a `public` directory, which contains the html, style sheets and JavaScript for the web app. But, to get the application working, we'll first need to push the Docker image to docker hub.

```
    sudo docker login --username=yourhubusername --password=yourpassword
    sudo docker build -t $DOCKER_ACC/$DOCKER_REPO:$IMG_TAG .
    sudo sudo docker push $DOCKER_ACC/$DOCKER_REPO:$IMG_TAG
```

7. Update the Kubernetes deployment configuration file `pypg-deployment.yaml`.

    Under the following, change the `image` name with the repository name that you got from the previous step:

    Now, under `secretKeyRef`, change the name of `<postgres-secret-name>` to match the name of the secret that was created before for PostgreSQL to your Kubernetes cluster.

```yaml
    secretKeyRef:
    name: <postgres-secret-name> # Edit me
```

    As for the `service` configuration at the bottom of the file, [`nodePort`][nodePort_information] indicates the port that the application can be accessed from. You have a range from 30000 - 32767 that you can use, but we've chosen 30081. As for the TCP port, it's set to 8080, which is the port that the Python application runs on in the container.

8. Deploy the application to kubernetes cluster

```
    kubectl apply -f pypg-deployment.yaml
```

9. Get the IP for the application.

```
    kubectl get svc
```

    Now you can access the application from the Public IP on port 30081.

    The clouddatabases-postgresql-helloworld app displays the contents of an _examples_ database. To demonstrate that the app is connected to your service, add some words to the database. The words are displayed as you add them, with the most recently added words displayed first.

## Code Structure

| File | Description |
| ---- | ----------- |
|[**server.py**](server.py)|Establishes a connection to the PostgreSQL database using credentials from BINDING (the name we created in the Kubernetes deployment file to expose the PostgreSQL credentials) and handles create and read operations on the database. |
|[**main.js**](public/javascripts/main.js)|Handles user input for a PUT command and parses the results of a GET command to output the contents of the PostgreSQL database.|

The app uses a PUT and a GET operation:

- PUT
  - takes user input from [main.js](public/javascript/main.js)
  - uses the `client.query` method to add the user input to the words table

- GET
  - uses `client.query` method to retrieve the contents of the _words_ table
  - returns the response of the database command to [main.js](public/javascript/main.js)
