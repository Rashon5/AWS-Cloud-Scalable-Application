import boto3

def create_dynamodb_table(table_name, partition_key, partition_key_type):
    # Initialize a session using Amazon DynamoDB
    session = boto3.Session()
    dynamodb = session.resource('dynamodb')

    # Define the table schema
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': partition_key,
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': partition_key,
                'AttributeType': partition_key_type
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)

    print(f'Table {table_name} has been created successfully.')
    return table

# Example usage:
table_name = 'users'
partition_key = 'email'
partition_key_type = 'S'  # S for String, N for Number, B for Binary

create_dynamodb_table(table_name, partition_key, partition_key_type)