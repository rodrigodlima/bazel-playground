import os
import boto3
from botocore.exceptions import ClientError


def get_dynamodb_resource():
    """Create DynamoDB resource using environment variables."""
    return boto3.resource(
        'dynamodb',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )


def create_item(table_name: str, item: dict) -> dict:
    """Create a document/item in a DynamoDB table.

    Args:
        table_name: Name of the DynamoDB table
        item: Dictionary containing the item data (must include partition key)

    Returns:
        Response from DynamoDB
    """
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table(table_name)

    try:
        response = table.put_item(Item=item)
        print(f"Item created successfully in table '{table_name}'")
        return response
    except ClientError as e:
        print(f"Error creating item: {e}")
        raise


def get_item(table_name: str, key: dict) -> dict:
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table(table_name)

    try:
        response = table.get_item(Key=key)
        return response.get('Item')
    except ClientError as e:
        print(f"Error getting item: {e}")
        raise


def main():
    table_name = os.environ.get('DYNAMODB_TABLE_NAME')

    if not table_name:
        print("Error: DYNAMODB_TABLE_NAME environment variable is required")
        return

    # Example: Create a sample item
    sample_item = {
        'id': '12345',
        'name': 'Sample Document',
        'description': 'This is a test document',
        'status': 'active'
    }

    print(f"Creating item in table: {table_name}")
    create_item(table_name, sample_item)

    # Retrieve the item
    print(f"\nRetrieving item with id: {sample_item['id']}")
    item = get_item(table_name, {'id': sample_item['id']})

    if item:
        print(f"Retrieved item: {item}")
    else:
        print("Item not found")


if __name__ == '__main__':
    main()
