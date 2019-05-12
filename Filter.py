import boto3
import DBAccessKey
from boto3.dynamodb.conditions import Key, Attr
import json
import decimal

access_key_id_global=DBAccessKey.DBAccessKey.access_key_id_global
secret_access_key_global=DBAccessKey.DBAccessKey.secret_access_key_global


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


class Filter_db:

    response = []

    def get_DB(Ref_no, controller):

        print("Ref no is "+Ref_no)

        dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2', aws_access_key_id=access_key_id_global,
                                  aws_secret_access_key=secret_access_key_global)
        table = dynamodb.Table('ME_CFS_DB')

        response = table.query(
            KeyConditionExpression=Key('Reference_No').eq(Ref_no)
        )
        if (response['Items']):
            print("start of filter")
            for i in response['Items']:
                #print(i['Reference_No'], ":", i['Date_Time']) #print selected attributes
                print(json.dumps(i, cls=DecimalEncoder))#print whole database

            print("end of filter")
            controller.show_frame("FilterPage")

        else:
            print(response['Items'])
            print("It is empty")



