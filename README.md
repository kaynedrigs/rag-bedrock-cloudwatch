# Building a Cost-Aware RAG Application with Amazon Bedrock

This repository accompanies the blog **“Building a Cost-Aware RAG Application with Amazon Bedrock”**.

It demonstrates a minimal, runnable setup for:
- Invoking Amazon Bedrock foundation models
- Monitoring Bedrock workloads with Amazon CloudWatch
- Gaining token-level cost visibility

## Prerequisites
- AWS account with Amazon Bedrock access
- Python 3.10+
- pip install boto3
- Configured AWS credentials (aws configure)

## Files
- bedrock_invoke.py – Minimal Bedrock runtime invocation example
- cloudwatch_latency.py – Fetches Bedrock latency metrics from CloudWatch
- cloudwatch_dashboard.json – Importable CloudWatch dashboard example

## How to Run
export AWS_REGION=us-east-1
export BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0

python bedrock_invoke.py
python cloudwatch_latency.py

Replace the model ID with one available in your AWS account and region.
