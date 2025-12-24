import boto3
import json
import os

REGION = os.getenv("AWS_REGION", "us-east-1")
MODEL_ID = os.getenv("BEDROCK_MODEL_ID")

if not MODEL_ID:
    raise ValueError("BEDROCK_MODEL_ID environment variable not set")

bedrock = boto3.client("bedrock-runtime", region_name=REGION)

prompt = """
Context:
- Emergency fund: save 3 months of expenses.
- Budget rule: 50% needs, 30% wants, 20% savings.

Question:
How much should I save monthly if my take-home pay is 40,000 PHP?
"""

response = bedrock.invoke_model(
    modelId=MODEL_ID,
    contentType="application/json",
    accept="application/json",
    body=json.dumps({
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300
    })
)

result = json.loads(response["body"].read())
print(result)
