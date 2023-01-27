
# Azure Cosmos DB to AWS Dynamo DB Migration

If you have a simple Cosmos DB that you'd like to migrate over to Dynamo DB, this project is for you. 

AWS has a [blog post](https://aws.amazon.com/blogs/database/migrate-from-azure-cosmos-db-to-amazon-dynamodb-using-aws-glue/) on migrating a Cosmos DB, but its fairly complex and required Glue Studio. The other option is the following 16 lines of python!

```python
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
```

If you had more complex ETL requirements you could always add the additional logic for each item before the `put_item` call. 

This repo provides support to execute the above.




## Using this project

1. clone the repo
2. create an `.env` file at the root. This file contains all the unique bits.
```
AZURE_URI=
AZURE_KEY=
DATABASE=
CONTAINER_NAME=
DYNAMO_TABLE=
AWS_DEFAULT_REGION=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_SESSION_TOKEN=
```
3. Build the image
``` bash
docker build . -t cosmosmigration
```
4. Run the image in interactive mode
```bash
docker run --env-file=.env -it cosmosmigration
```
5. Activate python environment
```bash
source env/bin/activate
```
5. Log in with Azure CLI
```bash
az login
```
6. Run the migration 
``` bash
python migrate.py
```