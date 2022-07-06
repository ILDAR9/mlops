import mlflow
from decouple import config
import os

# mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_tracking_uri("http://ec2-3-110-179-129.ap-south-1.compute.amazonaws.com:5000")

mlflow.set_experiment("test-exp")

with mlflow.start_run():
    for epoch in range(0, 3):
        print("epoch:", epoch)
        mlflow.log_metric(key="acc", value=2*epoch, step=epoch)

    mlflow.log_artifact('README.md')
