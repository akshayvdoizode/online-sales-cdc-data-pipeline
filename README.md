# DynamoDB CDC Pipeline Transformer

A serverless AWS Lambda function that's part of a Change Data Capture (CDC) pipeline, transforming DynamoDB Stream records for downstream data processing.

## Overview

This project is a critical component in a Change Data Capture (CDC) pipeline that:

1. Captures changes from DynamoDB through DynamoDB Streams
2. Transforms the raw change events into a standardized format
3. Prepares the data for downstream processing (e.g., analytics, data lakes, or other data stores)

## CDC Pipeline Architecture

```ascii
┌──────────────┐    ┌─────────────────┐    ┌───────────────┐    ┌─────────────────┐
│   DynamoDB   │───►│ DynamoDB Stream │───►│ AWS Lambda    │───►│ Downstream      │
│   Table      │    │ (Change Events) │    │ Transformer   │    │ Processing      │
└──────────────┘    └─────────────────┘    └───────────────┘    └─────────────────┘
```

## Features

- Real-time CDC processing
- Transforms complex DynamoDB JSON format into a simplified structure
- Handles order data including:
  - Order ID
  - Product name
  - Quantity
  - Price
  - CDC event type (INSERT/MODIFY/DELETE)
  - Creation timestamp
- Includes error handling for robust processing
- Base64 encoding/decoding for data compatibility

## Technical Details

### CDC Event Types

The transformer handles the following CDC event types:

- `INSERT`: New record creation
- `MODIFY`: Record updates
- `DELETE`: Record deletion

### Input Format

The function expects DynamoDB Stream records with the following structure:

```json
{
  "records": [
    {
      "recordId": "...",
      "data": "<base64-encoded-data>",
      ...
    }
  ]
}
```

### Output Format

The function transforms the data into:

```json
{
  "orderid": "string",
  "product_name": "string",
  "quantity": number,
  "price": number,
  "cdc_event_type": "INSERT|MODIFY|DELETE",
  "creation_datetime": "ISO8601 timestamp"
}
```

## Requirements

- Python 3.8+
- AWS Lambda
- DynamoDB Streams enabled on your table

## Setup

1. Enable DynamoDB Streams on your table:

   - Go to your DynamoDB table
   - Select 'Exports and streams'
   - Enable 'DynamoDB Stream details'
   - Choose 'New and old images'

2. Create a new Lambda function:

   - Runtime: Python 3.8+
   - Handler: TransformFunction.lambda_handler

3. Deploy the `TransformFunction.py` code to your Lambda function

4. Configure appropriate IAM permissions

## IAM Permissions

The Lambda function requires the following permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetRecords",
        "dynamodb:GetShardIterator",
        "dynamodb:DescribeStream",
        "dynamodb:ListStreams"
      ],
      "Resource": "your-dynamodb-stream-arn"
    }
  ]
}
```

## Error Handling

The function includes robust error handling:

- Each record is processed independently
- Failed records are marked with `"result": "ProcessingFailed"`
- Successful records are marked with `"result": "Ok"`
- Errors are logged to CloudWatch Logs for debugging

## Monitoring

Monitor your CDC pipeline using:

- CloudWatch Metrics for Lambda
- CloudWatch Logs for detailed processing logs
- DynamoDB Streams metrics
- Lambda execution metrics

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Author

Akshay Doyizode
