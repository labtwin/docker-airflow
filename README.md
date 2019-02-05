# docker-airflow

This repository contains a dockerized airflow application for testing airflow.

## Informations

* Based on Python (3.6-slim) official Image [python:3.6-slim](https://hub.docker.com/_/python/) and uses the official [Postgres](https://hub.docker.com/_/postgres/) as backend and [Redis](https://hub.docker.com/_/redis/) as queue
* Based on
https://github.com/puckel/docker-airflow

## Installation and Environment

1. Install [docker desktop for Mac](https://docs.docker.com/docker-for-mac/install/)
2. Clone the repository.
3. Create a .env in the repository containing the following variables.
```
REDSHIFT_USER=XXX
REDSHIFT_PASSWORD=XXX
REDSHIFT_HOST=XXX
REDSHIFT_PORT=5439
REDSHIFT_DB=labpanda
FERNET_KEY=XXX
```

## Build

Build docker image from Dockerfile

    docker build -t "airflow-test" .

## Usage

### Run container
Run docker-airflow passing the variables of the .env file to the container at runtime:

    docker run -p 8080:8080 --env-file .env airflow-test webserver

### Open web interface
Open web interface of airflow on localhost:8080

### Run specific task
Get the docker container id

    docker container ls

Run a the task insert_chunk_count of the redshift dag using (replace the DOCKER_ID) (You might have to get set write permissions on the table airflow_test.count_users in Redshift).

    docker exec DOCKER_ID bash -c "airflow run redshift insert_chunk_count 2019-01-13"

### Update dag or task

Change the task or dag in the dag-file in /dags/first_dag.py (or any other dag file that you create in that folder). Then

1. Rebuild container using the command above
2. Run the container using the command above
3. Execute the task using the command above
