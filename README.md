# python-helloworld-postgresql

sample python app that shows you how to connect to a PostgreSQL database deployed in Kubernetes. 

## Running the app on Kubernetes

1. Create the kubernetes cluster in any cloud you choose. (ie:EKS)

2. Setup Kubectl in you local host

    ```
    https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/
    ```

3. Deploy postgresql using Helm charts
   
    ref: https://github.com/bitnami/charts/tree/master/bitnami/postgresql/#installing-the-chart
    ```
    helm install pg-test-release --set postgresqlPassword=secretpassword,postgresqlDatabase=testdb bitnami/postgresql
    ```

4. Create kubernetes secrets to store databse credential which can be used by the sample app.
   ```
   kubectl create -f pg-secret.yaml
   ```

5. clone the python-helloworld-postgresql
   
```
    git clone git@github.com:sharonsahadevan/python-helloworld-postgresql.git
```

6. `cd` into this newly created directory, and `cd` into the `postgresql` folder. The code for connecting to the service, and reading from and updating the database can be found in `server.py`. There's also a `public` directory, which contains the html, style sheets and JavaScript for the web app. But, to get the application working, we'll first need to push the Docker image to docker hub.

```
    sudo docker login --username=yourhubusername --password=yourpassword
    sudo docker build -t $DOCKER_ACC/$DOCKER_REPO:$IMG_TAG .
    sudo sudo docker push $DOCKER_ACC/$DOCKER_REPO:$IMG_TAG
```

7. Update the Kubernetes deployment configuration file `pypg-deployment.yaml`.

    Under the following, change the `image` name with the repository name that you got from the previous step:

    Now, under `secretRef`, change the name of `<postgres-secret-name>` to match the name of the secret that was created before for PostgreSQL to your Kubernetes cluster.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: pg-test-secret
type: Opaque
data:
  DB_USERNAME: cG9zdGdyZXM=
  DB_PASSWORD: c2VjcmV0cGFzc3dvcmQ=
  DB_HOST: cGctdGVzdC1yZWxlYXNlLXBvc3RncmVzcWwuZGVmYXVsdC5zdmMuY2x1c3Rlci5sb2NhbA==
  DB_NAME: dGVzdGRi # Edit me
```

    As for the `service` LoadBalancer type is used. Nodeport service also can be used. But I chose to use LoadBalancer.

8. Deploy the application to kubernetes cluster

```
    kubectl apply -f pypg-deployment.yaml
```

9. Get the IP for the application.

```
    kubectl get svc
```

    From the output LoadBalancer External IP can be obtained.

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


## Credits

https://github.com/IBM-Cloud
