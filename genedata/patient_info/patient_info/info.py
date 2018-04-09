import csv, json, decimal
import boto3
from botocore.exceptions import ClientError


class ConnectionError(Exception):
    pass


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def connect():
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2',
                              endpoint_url="http://localhost:6464",
                              aws_access_key_id='anything',
                              aws_secret_access_key='anything')

    try:
        table = dynamodb.create_table(
            TableName='Patients',
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'  #Partition key
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
    except Exception as e:
        if e[0] == 'Connection aborted':
            raise ConnectionError('Connection refused')
        table = dynamodb.Table('Genes')
        table = dynamodb.Table('Patients')

    return table

def populate():
    table = connect()
    with open('../../../data/patients.csv') as datafile:
        reader = csv.reader(datafile, delimiter=',')
        fields = reader.next()
        for row in reader:
            item = {
                'id': row[0],
                'age': int(row[1]),
                'gender': row[2],
                'education': row[3]
            }
            table.put_item(Item=item)

def query(patient_id):
    table = connect()
    try:
	response = table.get_item(Key={'id': patient_id})
        if 'Item' not in response:
            return 'Error: {} not in table {}'.format(patient_id, table.name)
    except ClientError as e:
	return e.response['Error']['Message']
    else:
	return response['Item']
