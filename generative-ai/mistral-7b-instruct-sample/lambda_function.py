import json
import os
import boto3

# grab environment variables
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']

def lambda_handler(event, context):
    print(event)
    payload = event["body"]
    client = boto3.client("runtime.sagemaker")
    response = client.invoke_endpoint(
        EndpointName=ENDPOINT_NAME, ContentType="application/json", Body=payload, 
        InferenceComponentName="huggingface-llm-mistral-7b-instruct-20240228-140549"
    )
    response = response["Body"].read().decode("utf8")
    response = json.loads(response)
    api_response = {}
    api_response['body'] = json.dumps(response)
    api_response['statusCode'] = 200
    api_response.update({"headers": {"Content-Type": "application/json"}})
    print(api_response)
    return api_response

