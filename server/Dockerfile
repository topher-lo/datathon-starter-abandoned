FROM prefecthq/prefect:latest-python3.8

# install some base utilities
RUN apt update && apt install build-essential -y build-essential unixodbc-dev && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install curl -y

# set working directory
WORKDIR /opt/server

# make src, flows and tasks directory
RUN mkdir src && mkdir flows && mkdir tasks

# copy tasks directory and utils file
COPY server/src/tasks src/tasks
COPY server/src/utils.py src/.

# append server directory to PYTHONPATH
ENV PYTHONPATH="/opt/server:${PYTHONPATH}"