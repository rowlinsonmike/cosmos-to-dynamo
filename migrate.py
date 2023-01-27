from azure.cosmos import CosmosClient
from os import environ
import boto3 
URL = environ.get("AZURE_URI")
KEY = environ.get("AZURE_KEY")
DYNAMO_TABLE = environ.get("DYNAMO_TABLE")
DATABASE = environ.get("DATABASE")
CONTAINER_NAME = environ.get("CONTAINER_NAME")
dynamo_table = boto3.resource('dynamodb').Table(DYNAMO_TABLE)
client = CosmosClient(URL, credential=KEY, consistency_level='Session')
database = client.get_database_client(DATABASE)
container = database.get_container_client(CONTAINER_NAME)
for item in container.query_items(
        query='SELECT * FROM Items',
        enable_cross_partition_query=True):
    dynamo_table.put_item(Item=item)




