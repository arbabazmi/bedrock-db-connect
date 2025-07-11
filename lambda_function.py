import json
import sys
import os

# Add the current directory to Python path for Lambda execution
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from src.db_setup import setup_database
    from src.bedrock_nl2sql import nl_to_sql
except ImportError:
    # Fallback for Lambda deployment where files might be at root
    from db_setup import setup_database
    from bedrock_nl2sql import nl_to_sql

def lambda_handler(event, context):
    # Extract NL query from POST body or queryStringParameters
    natural_language_query = None
    print(f"Received event: {json.dumps(event)}")

    # Try to get from API Gateway HTTP API event
    if "body" in event and event["body"]:
        try:
            body = json.loads(event["body"])
            print(f"Parsed body: {body}")
            natural_language_query = body.get("query")
            print(f"Extracted query: {natural_language_query}")
        except Exception:
            pass

    # Or from queryStringParameters (for GET)
    if not natural_language_query and "queryStringParameters" in event and event["queryStringParameters"]:
        natural_language_query = event["queryStringParameters"].get("query")

    if not natural_language_query:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "No natural language query provided."})
        }

    # Step 1: NL -> SQL
    sql_query = nl_to_sql(natural_language_query)
    print(f"Generated SQL: {sql_query}")
    if not sql_query or sql_query.lower().startswith("error"):
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to generate SQL.", "details": sql_query})
        }

    # Step 2: Run SQL on DB
    try:
        conn = setup_database()
        cursor = conn.cursor()
        cursor.execute(sql_query)
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        rows = cursor.fetchall()
        result = [dict(zip(columns, row)) for row in rows] if columns else rows
        conn.close()
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Error executing SQL.", "details": str(e), "sql": sql_query})
        }

    # Return JSON
    return {
        "statusCode": 200,
        "body": json.dumps({
            "query": natural_language_query,
            "sql": sql_query,
            "result": result
        })
    }