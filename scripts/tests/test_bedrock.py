"""Test AWS Bedrock access."""
import os
import json
import boto3
from dotenv import load_dotenv

load_dotenv()

def test_bedrock():
    """Test Bedrock Claude access."""
    session = boto3.Session(
        profile_name=os.getenv("AWS_PROFILE", "prod-tools"),
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    )

    bedrock = session.client("bedrock-runtime")

    # Test simple message
    model_id = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"

    request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 100,
        "temperature": 0,
        "messages": [
            {
                "role": "user",
                "content": "Say hello in exactly 5 words."
            }
        ]
    }

    response = bedrock.invoke_model(
        modelId=model_id,
        body=json.dumps(request)
    )

    result = json.loads(response["body"].read())
    print(f"✓ Bedrock test successful!")
    print(f"  Model: {model_id}")
    print(f"  Response: {result['content'][0]['text']}")
    print(f"  Tokens: {result['usage']['input_tokens']} in / {result['usage']['output_tokens']} out")


if __name__ == "__main__":
    test_bedrock()
