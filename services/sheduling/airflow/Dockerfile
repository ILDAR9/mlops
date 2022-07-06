FROM apache/airflow:2.3.0-python3.8

ARG CUR

USER root
# Add Firefox driver
RUN apt-get update                             \
    && apt-get install -y --no-install-recommends \
     ca-certificates curl firefox-esr make        \
    && rm -fr /var/lib/apt/lists/*                \
    && curl -L https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz | tar xz -C /usr/local/bin \
    && apt-get purge -y ca-certificates curl

WORKDIR /opt/airflow

# project file
COPY ./deepracer_submit ./deepracer_submit
COPY $CUR/requirements.txt ./

USER airflow

# Selenium support & PostgreSQL
RUN pip install --upgrade --no-cache-dir pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r deepracer_submit/requirements.txt

# copy aws data
ARG AWS_CREDENTIALS
RUN mkdir ~/.aws && echo "${AWS_CREDENTIALS}" > /home/airflow/.aws/credentials

# controller
COPY Makefile ./

ENV PYTHONPATH=/opt/airflow/src:$PYTHONPATH
ENV AWS_SHARED_CREDENTIALS_FILE=/home/airflow/.aws/credentials
ENV GIT_PYTHON_REFRESH=quite