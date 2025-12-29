import json
import boto3
from botocore.exceptions import ClientError

# Initialize Bedrock Agent Runtime client
bedrock_agent_runtime = boto3.client('bedrock-agent-runtime')

def lambda_handler(event, context):

    # ---- HANDLE CORS PREFLIGHT ----
    method = (
        event.get("httpMethod")
        or event.get("requestContext", {}).get("http", {}).get("method")
    )

    if method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "POST,OPTIONS",
                "Access-Control-Max-Age": "3600"
            },
            "body": ""
        }


    """
    Lambda function to query Amazon Bedrock Knowledge Base using Nova Lite model.
    
    Expected event structure:
    {
        "query": "Your question here",
        "sessionId": "optional-session-id"
    }
    """
    
    # Configuration - REPLACE THESE VALUES
    KNOWLEDGE_BASE_ID = "YOUR_KNOWLEDGE_BASE_ID"
    MODEL_ARN = "arn:aws:bedrock:YOUR_REGION::foundation-model/YOUR_MODEL_ID"
    
    try:
        # Extract query from event
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event
            
        query = body.get('query', '')
        session_id = body.get('sessionId')  # Optional, can be None
        
        if not query:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                    'Access-Control-Allow-Methods': 'POST,OPTIONS'
                },
                'body': json.dumps({
                    'error': 'Query parameter is required'
                })
            }
        
        # Prepare the request parameters
        request_params = {
            'input': {
                'text': f"""
                You are a helpful assistant.
                Format answers clearly using sections when appropriate.

                Question:
                {query}
                """
            },
            'retrieveAndGenerateConfiguration': {
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': KNOWLEDGE_BASE_ID,
                    'modelArn': MODEL_ARN,
                    'retrievalConfiguration': {
                        'vectorSearchConfiguration': {
                            'numberOfResults': 5
                        }
                    }
                }
            }
        }
        
        # Only include sessionId if provided (for continuing conversations)
        if session_id:
            request_params['sessionId'] = session_id
        
        # Retrieve and generate response from knowledge base
        response = bedrock_agent_runtime.retrieve_and_generate(**request_params)
        
        # Extract the generated response
        output_text = response['output']['text']
        citations = response.get('citations', [])
        session_id = response.get('sessionId', '')
        
        # Format response
        result = {
            'answer': output_text,
            'sessionId': session_id,
            'citations': citations
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'POST,OPTIONS'
            },
            'body': json.dumps(result, indent=2)
        }
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'POST,OPTIONS'
            },
            'body': json.dumps({
                'error': f'AWS Error: {error_code}',
                'message': error_message
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'POST,OPTIONS'
            },
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }