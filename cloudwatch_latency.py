import boto3
import os
from datetime import datetime, timedelta

REGION = os.getenv("AWS_REGION", "us-east-1")
MODEL_ID = os.getenv("BEDROCK_MODEL_ID")

if not MODEL_ID:
    raise ValueError("BEDROCK_MODEL_ID environment variable not set")

cloudwatch = boto3.client("cloudwatch", region_name=REGION)

response = cloudwatch.get_metric_statistics(
    Namespace="AWS/Bedrock",
    MetricName="InvocationLatency",
    Dimensions=[{"Name": "ModelId", "Value": MODEL_ID}],
    StartTime=datetime.utcnow() - timedelta(hours=1),
    EndTime=datetime.utcnow(),
    Period=300,
    Statistics=["Average"]
)

for datapoint in sorted(response["Datapoints"], key=lambda x: x["Timestamp"]):
    print(datapoint["Timestamp"], datapoint["Average"])
