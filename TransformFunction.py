import base64
import json
from datetime import datetime
from typing import Dict, List, Any

def lambda_handler(event: Dict[str, List[Dict[str, Any]]], context: Any) -> Dict[str, List[Dict[str, Any]]]:
    """
    Transform DynamoDB Stream records into a simplified format.
    
    Args:
        event: AWS Lambda event containing records to process
        context: AWS Lambda context object
    
    Returns:
        Dictionary containing processed records
    """
    output_records = []

    for record in event['records']:
        try:
            transformed_record = process_record(record)
            output_records.append(transformed_record)
        except Exception as e:
            # Log the error for debugging
            print(f"Error processing record {record['recordId']}: {str(e)}")
            output_records.append({
                'recordId': record['recordId'],
                'result': 'ProcessingFailed',
                'data': record['data']
            })

    return {'records': output_records}

def process_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process individual record and transform it to the desired format.
    
    Args:
        record: Single record from the input event
    
    Returns:
        Transformed record in the required format
    """
    # Decode and parse the input data
    payload = json.loads(base64.b64decode(record['data']))
    dynamodb_data = payload['dynamodb']
    new_image = dynamodb_data['NewImage']
    
    # Create transformed data structure
    transformed_data = {
        'orderid': new_image['orderid']['S'],
        'product_name': new_image['product_name']['S'],
        'quantity': int(new_image['quantity']['N']),
        'price': float(new_image['price']['N']),
        'cdc_event_type': payload['eventName'],
        'creation_datetime': datetime.utcfromtimestamp(
            dynamodb_data['ApproximateCreationDateTime']
        ).isoformat() + 'Z'
    }

    # Encode the transformed data
    transformed_data_str = json.dumps(transformed_data) + '\n'
    transformed_data_encoded = base64.b64encode(
        transformed_data_str.encode('utf-8')
    ).decode('utf-8')

    return {
        'recordId': record['recordId'],
        'result': 'Ok',
        'data': transformed_data_encoded
    }