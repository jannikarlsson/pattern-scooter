# note that this Docker image's containers depend on there being
# a pattern-backend Docker container named 'backend' running on the same
# network as this one. hence, it doesn't make sense to create containers
# based on this image in isolation (it's only meant to be used in the
# supermodule 'pattern-orchestra')
FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP=flask_app.py
ENV REQUEST_ROOT_URL=http://backend:8000/api

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
