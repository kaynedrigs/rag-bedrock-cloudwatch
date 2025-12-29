# Building a Cost-Aware RAG Application with Amazon Bedrock

This repository accompanies the blog **"Building a Cost-Aware RAG Application with Amazon Bedrock"**.

It demonstrates a minimal, runnable setup for:
- Building a RAG application with Amazon Bedrock Knowledge Bases
- Invoking Amazon Bedrock foundation models via AWS Lambda
- Monitoring Bedrock workloads with Amazon CloudWatch
- Gaining token-level cost visibility

## Prerequisites

- AWS account with Amazon Bedrock access
- Python 3.10+
- boto3 (`pip install boto3`)
- Configured AWS credentials (`aws configure`)

## Files

### Lambda Function
- `lambda_handler.py` – AWS Lambda function that queries a Bedrock Knowledge Base using the RetrieveAndGenerate API

### IAM Policies
- `bedrock-invoke-policy.json` – IAM policy for invoking Bedrock models and accessing S3/CloudWatch
- `kb-inline-permissions.json` – Inline permissions for Bedrock model invocation and logging
- `retrieve-lambda.json` – IAM policy for the Lambda to retrieve from the Knowledge Base

### Frontend
- `kb-chat-ui.html` – Chat UI for interacting with the Knowledge Base via API Gateway

### Monitoring
- `cloudwatch_latency.py` – Fetches Bedrock invocation latency metrics from CloudWatch

### Sample Data
- `recipes-kb/` – Sample knowledge base content (Filipino halal recipes)

## Configuration

Before deploying, replace the placeholder values in the files:

| Placeholder | Description |
|-------------|-------------|
| `YOUR_REGION` | Your AWS region (e.g., `us-east-1`) |
| `YOUR_ACCOUNT_ID` | Your 12-digit AWS account ID |
| `YOUR_KNOWLEDGE_BASE_ID` | Your Bedrock Knowledge Base ID |
| `YOUR_MODEL_ID` | Bedrock model ID (e.g., `amazon.nova-lite-v1:0`) |
| `YOUR_S3_BUCKET` | S3 bucket name for knowledge base documents |
| `YOUR_API_ID` | API Gateway ID |
| `YOUR_STAGE` | API Gateway stage name |

## How to Run

### CloudWatch Latency Metrics

```bash
export AWS_REGION=us-east-1
export BEDROCK_MODEL_ID=amazon.nova-lite-v1:0

python cloudwatch_latency.py
```

### Chat UI

1. Deploy the Lambda function with the provided IAM policies
2. Create an API Gateway endpoint pointing to the Lambda
3. Update `YOUR_API_ID`, `YOUR_REGION`, and `YOUR_STAGE` in `kb-chat-ui.html`
4. Open `kb-chat-ui.html` in a browser

## License

MIT
