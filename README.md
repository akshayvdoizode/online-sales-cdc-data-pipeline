# DynamoDB CDC Pipeline Transformer

A serverless AWS Lambda function that's part of a Change Data Capture (CDC) pipeline, transforming DynamoDB Stream records for downstream data processing.

## Overview

This project is a critical component in a Change Data Capture (CDC) pipeline that:

1. Captures changes from DynamoDB through DynamoDB Streams
2. Transforms the raw change events into a standardized format
3. Prepares the data for downstream processing (e.g., analytics, data lakes, or other data stores)

## CDC Pipeline Architecture

![alt text](https://github.com/akshayvdoizode/online-sales-cdc-data-pipeline/blob/main/architecture-diagram.png?raw=true)

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
- Integration with Amazon Athena for SQL-based analysis
- QuickSight dashboards for real-time data visualization

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
- Amazon Athena
- Amazon QuickSight subscription
- S3 bucket for Athena query results

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

5. Configure Athena Integration:

   - Create a database in Athena
   - Create a table using the following DDL:

   ```sql
   CREATE EXTERNAL TABLE IF NOT EXISTS orders (
     orderid string,
     product_name string,
     quantity int,
     price decimal(10,2),
     cdc_event_type string,
     creation_datetime timestamp
   )
   STORED AS PARQUET
   LOCATION 's3://your-bucket/transformed-data/';
   ```

6. Set up QuickSight:
   - Connect QuickSight to Athena as a data source
   - Create a new dataset using the orders table
   - Design dashboards for:
     - Order volume trends
     - Product performance analysis
     - Revenue metrics
     - Change event monitoring

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
    },
    {
      "Effect": "Allow",
      "Action": [
        "athena:StartQueryExecution",
        "athena:GetQueryResults",
        "s3:GetBucketLocation",
        "s3:GetObject",
        "s3:ListBucket",
        "s3:PutObject"
      ],
      "Resource": [
        "arn:aws:athena:*:*:workgroup/*",
        "arn:aws:s3:::your-bucket/*"
      ]
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
- Athena query performance metrics
- QuickSight dashboard usage analytics

## Data Analysis

### Athena Queries

Common analysis queries:

```sql
-- Get daily order totals
SELECT DATE(creation_datetime) as order_date,
       COUNT(*) as order_count,
       SUM(price * quantity) as daily_revenue
FROM orders
WHERE cdc_event_type = 'INSERT'
GROUP BY DATE(creation_datetime)
ORDER BY order_date DESC;

-- Top selling products
SELECT product_name,
       SUM(quantity) as total_quantity,
       SUM(price * quantity) as total_revenue
FROM orders
WHERE cdc_event_type = 'INSERT'
GROUP BY product_name
ORDER BY total_revenue DESC
LIMIT 10;
```

### QuickSight Dashboards

The project includes pre-built QuickSight dashboards for:

- Sales Performance Overview
- Product Analytics
- Order Trends
- CDC Event Monitoring
- Revenue Analytics

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Author

Akshay Doyizode
