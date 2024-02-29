import boto3
import json

# Configure your AWS credentials
# Option 1: Using environment variables (credentials will be picked up automatically)
# session = boto3.Session()

# Option 2: Using a specific profile from the credentials file
# session = boto3.Session(profile_name='your_profile_name')

# Option 3: Specifying credentials directly (not recommended for security reasons)
session = boto3.Session(aws_access_key_id='see json',
                        aws_secret_access_key='see json',
                        region_name="us-east-1")


# Replace placeholders with your actual values
table_name = "strike_analyses"
output_file = "dynamodb_data.json"

# Connect to DynamoDB
dynamodb = session.resource('dynamodb')
dynamodb_client = session.client('dynamodb')
table = dynamodb.Table(table_name)

# increase provisioned throughput
update_response = dynamodb_client.update_table(TableName=table_name,
                                               ProvisionedThroughput={'ReadCapacityUnits': 15,
                                                                      'WriteCapacityUnits': 10})
print(update_response)

# Scan the table and collect results
items = []
last_evaluated_key = None
while True:
    if last_evaluated_key:
        response = table.scan(ExclusiveStartKey=last_evaluated_key)
    else:
        response = table.scan()
    item_in_response = response['Items']
    print(item_in_response[0])
    items.extend(item_in_response)
    last_evaluated_key = response.get('LastEvaluatedKey')
    if not last_evaluated_key:
        break

# Write data to JSON file
with open(output_file, 'w') as f:
    f.write(json.dumps(items, indent=4))

print(f"Data successfully exported to {output_file}")
