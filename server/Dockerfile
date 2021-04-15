FROM prefecthq/prefect:latest-python3.8

# install some base utilities
RUN apt update && apt install build-essential -y build-essential unixodbc-dev && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install curl -y

# set working directory
WORKDIR /opt/server/src

# make flows and tasks directory
RUN mkdir flows
RUN mkdir tasks

# copy tasks dir and utils
COPY server/src/tasks tasks
COPY server/src/utils.py .