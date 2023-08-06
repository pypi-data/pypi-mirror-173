import boto3
import os

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
REGION = 'us-west-2'

class DynamoDb():
    def __init__(self, tables):
        boto3_params = {'region_name': REGION, 'aws_access_key_id': AWS_ACCESS_KEY_ID, 'aws_secret_access_key': AWS_SECRET_ACCESS_KEY}
        dynamodb = boto3.resource('dynamodb', **boto3_params)
        self.tables = dict()
        
        for table_type, table_name in tables.items():
            self.tables[table_type] = dynamodb.Table(table_name)

    def scan(self, table_name):
        records = self.tables[table_name].scan()
        return records["Items"]
    
    def query(self, table_name, **params):
        records = self.tables[table_name].query(**params)
        return records["Items"]
    
    def update_item(self, table_name, **params):
        records = self.tables[table_name].update_item(**params)
    
    def put_item(self, table_name, **params):
        records = self.tables[table_name].put_item(**params)

    def delete_item(self, table_name, **params):
        self.tables[table_name].delete_item(**params)


