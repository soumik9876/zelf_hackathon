# pull a base python image
FROM python:3.10-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR .

# install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --cache-dir .pip-cache -r requirements.txt && \
    rm -rf .pip-cache

# copy run.sh
COPY ./run.sh .
RUN chmod +x run.sh

# copy project
COPY . .