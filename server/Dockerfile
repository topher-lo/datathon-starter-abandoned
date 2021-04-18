FROM prefecthq/prefect:latest-python3.8

# install some base utilities
RUN apt update && apt install build-essential -y build-essential unixodbc-dev && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install curl -y

# set working directory
WORKDIR /opt/server/src

# install python dependencies
COPY requirements/flows-requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r flows-requirements.txt

# make flows and tasks directory
RUN mkdir flows && mkdir tasks

# copy tasks directory and utils file
COPY server/src/tasks tasks
COPY server/src/utils.py .

# append opt directory to PYTHONPATH
ENV PYTHONPATH="/opt:${PYTHONPATH}"