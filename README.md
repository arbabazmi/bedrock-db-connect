# Bedrock DB Connect

A serverless AWS Lambda application that converts natural language queries to SQL using Amazon Bedrock and executes them against a SQLite database.

## Overview

This project demonstrates how to build a natural language to SQL (NL2SQL) system using:
- **Amazon Bedrock** for AI-powered natural language processing
- **AWS Lambda** for serverless execution
- **SQLite** for in-memory database operations
- **Python** for backend logic

## Features

- Convert natural language queries to SQL using Amazon Bedrock
- Execute SQL queries against a pre-populated SQLite database
- RESTful API interface for easy integration
- Comprehensive test coverage
- Error handling and validation

## Project Structure

```
bedrock-db-connect/
├── lambda_function.py          # Main Lambda handler
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── src/                        # Source code modules
│   ├── __init__.py
│   ├── bedrock_nl2sql.py      # Bedrock integration for NL2SQL
│   ├── db_setup.py            # Database setup and sample data
│   ├── handler.py             # Request handling logic
│   └── utils.py               # Utility functions
├── tests/                      # Test files
│   ├── __init__.py
│   └── test_db_setup.py       # Database setup tests
├── test_bedrock_nl2sql.py     # Bedrock integration tests
├── test_db_setup.py           # Database tests (root level)
└── test_handler.py            # Handler tests
```

## Sample Database Schema

The application uses a sample `orders` table with the following structure:

| Column        | Type    | Description           |
|---------------|---------|----------------------|
| id            | INTEGER | Primary key          |
| customer_name | TEXT    | Customer name        |
| amount        | REAL    | Order amount         |
| order_date    | TEXT    | Order date (YYYY-MM-DD) |

### Sample Data

The database is pre-populated with 5 sample orders:
- Alice: $1,200 (2025-06-30) and $500 (2025-07-03)
- Bob: $800 (2025-07-01)
- Charlie: $2,200 (2025-07-02)
- Eve: $1,500 (2025-07-04)

## API Usage

### Request Format

**POST** to your Lambda function URL with JSON body:
```json
{
    "query": "Show me all orders from Alice"
}
```

**GET** with query parameter:
```
?query=Show me all orders from Alice
```

### Response Format

```json
{
    "query": "Show me all orders from Alice",
    "sql": "SELECT * FROM orders WHERE customer_name = 'Alice'",
    "result": [
        {"id": 1, "customer_name": "Alice", "amount": 1200, "order_date": "2025-06-30"},
        {"id": 4, "customer_name": "Alice", "amount": 500, "order_date": "2025-07-03"}
    ]
}
```

## Setup and Deployment

### Prerequisites

- AWS Account with Bedrock access enabled
- Python 3.11+
- AWS CLI configured

### Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd bedrock-db-connect
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export AWS_REGION=us-east-2
```

4. Run tests:
```bash
python -m unittest discover tests
```

### AWS Lambda Deployment

1. Create a deployment package:
```bash
pip install -r requirements.txt -t .
zip -r deployment-package.zip .
```

2. Create Lambda function:
```bash
aws lambda create-function \
    --function-name bedrock-db-connect \
    --runtime python3.11 \
    --role arn:aws:iam::YOUR-ACCOUNT:role/lambda-execution-role \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://deployment-package.zip
```

3. Set up environment variables:
```bash
aws lambda update-function-configuration \
    --function-name bedrock-db-connect \
    --environment Variables='{AWS_REGION=us-east-2}'
```

## Configuration

### Bedrock Model

The default model is `amazon.titan-text-express-v1`. You can change this in `src/bedrock_nl2sql.py`:

```python
model_id = "anthropic.claude-3-sonnet-20240229-v1:0"  # Example alternative
```

### AWS Region

Set the AWS region via environment variable:
```bash
export AWS_REGION=us-west-2
```

## Testing

### Unit Tests

Run all tests:
```bash
python -m unittest discover
```

Run specific test files:
```bash
python -m unittest tests.test_db_setup
python test_bedrock_nl2sql.py
python test_handler.py
```

### Test Coverage

The project includes tests for:
- Database setup and data validation
- Bedrock integration
- Lambda handler functionality
- Error handling scenarios

## Example Queries

Try these natural language queries:

- "Show me all orders"
- "Find orders from Alice"
- "What's the total amount of all orders?"
- "Show orders placed after July 1st, 2025"
- "Which customer has the highest order amount?"

## Error Handling

The application handles various error scenarios:
- Invalid natural language queries
- Bedrock service errors
- SQL execution errors
- Missing or malformed request parameters

## Security Considerations

- Use IAM roles with minimal required permissions
- Validate and sanitize all inputs
- Consider implementing rate limiting
- Use VPC for additional network security if needed

## Dependencies

- `boto3`: AWS SDK for Python
- `sqlite3`: Database operations (built-in)
- `json`: JSON handling (built-in)
- `unittest`: Testing framework (built-in)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Check the test files for usage examples
- Review AWS Bedrock documentation
- Ensure your AWS account has Bedrock access enabled in the configured region
