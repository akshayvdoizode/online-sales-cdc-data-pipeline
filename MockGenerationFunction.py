import boto3
import random
from decimal import Decimal
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize the DynamoDB resource outside the handler
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('OrdersRawTable')

def generate_order_data():
    """Generate random order data."""
    orderid = str(random.randint(1, 10000))
    product_name = random.choice(['Laptop', 'Phone', 'Tablet', 'Headphones', 'Charger'])
    quantity = random.randint(1, 5)
    price = Decimal(str(round(random.uniform(10.0, 500.0), 2)))
    
    return {
        'orderid': orderid,
        'product_name': product_name,
        'quantity': quantity,
        'price': price
    }

def insert_into_dynamodb(data):
    """Insert data into DynamoDB."""
    try:
        table.put_item(Item=data)
        logger.info(f"Successfully inserted data: {data}")
        return True
    except Exception as e:
        logger.error(f"Error inserting data into DynamoDB: {str(e)}")
        raise

def lambda_handler(event, context):
    """AWS Lambda handler function."""
    try:
        # Generate and insert data
        data = generate_order_data()
        insert_into_dynamodb(data)
        
        return {
            'statusCode': 200,
            'body': f'Successfully generated and inserted order data: {data}'
        }
    except Exception as e:
        logger.error(f"Error in lambda execution: {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Error generating or inserting data: {str(e)}'
        }