FROM python:3.9.9-slim-bullseye

# we might want to use the non binary psycopg2 package later
# see https://www.psycopg.org/docs/install.html#psycopg-vs-psycopg-binary
RUN apt-get update && \
    apt-get -y install libpq-dev gcc && \
    pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir mlflow==1.26.0 psycopg2 boto3 protobuf==3.20.0
    # pip install --no-cache-dir scikit-learn

ARG unprivileged_user=mlflow

RUN useradd ${unprivileged_user} --shell /bin/bash --create-home

USER ${unprivileged_user}

WORKDIR /home/${unprivileged_user}

EXPOSE 5000

CMD ["mlflow","server","-h","0.0.0.0"]
