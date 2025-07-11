import boto3
import json
import os

def nl_to_sql(natural_language_query, model_id=None, region=None):
    """
    Send a natural language query to Bedrock and return the generated SQL.

    Args:
        natural_language_query (str): The user's NL query.
        model_id (str, optional): Bedrock model id. Defaults to Amazon Titan Express.
        region (str, optional): AWS region. Defaults to AWS_REGION env or 'us-east-1'.

    Returns:
        str: The generated SQL query (or error message).
    """
    if model_id is None:
        # Set to your enabled Bedrock model (Amazon Titan, Claude, etc.)
        model_id = "amazon.titan-embed-text-v2:0"
    if region is None:
        region = os.environ.get("AWS_REGION", "us-east-2")

    bedrock = boto3.client("bedrock-runtime", region_name=region)

    prompt = (
        "Convert the following natural language request into an SQL query:\n"
        f"Request: {natural_language_query}\n"
        "SQL:"
    )

    # For Titan/Claude, the body structure may differ; check documentation for your model.
    body = {
        "inputText": prompt,
        "maxTokenCount": 256,
        "temperature": 0.1,
        "topP": 0.9,
        "stopSequences": ["#", ";"]
    }

    try:
        response = bedrock.invoke_model(
            modelId=model_id,
            body=json.dumps(body)
        )
        result = json.loads(response["body"].read())
        print(f"Bedrock response: {result}")
        # Titan returns: {'results': [{'outputText': '...SQL...'}]}
        sql = result["results"][0].get("outputText", "").strip()
        return sql
    except Exception as e:
        return f"Error invoking Bedrock: {e}"
