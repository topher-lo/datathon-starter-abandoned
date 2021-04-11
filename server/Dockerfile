FROM python:3.8

ENV MICRO_SERVICE=/home/app/webapp
# set work directory
RUN mkdir -p $MICRO_SERVICE
# where your code lives
WORKDIR $MICRO_SERVICE

# install pip
RUN pip install --upgrade pip
# install prefect
RUN pip install prefect
# change prefect backend
RUN prefect backend server
# copy requirements.txt
COPY requirements.txt $MICRO_SERVICE/requirements.txt
# install dependencies
RUN pip install -r requirements.txt
# copy project
COPY . $MICRO_SERVICE