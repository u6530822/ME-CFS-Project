# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 11:02:59 2019
@author: Nigel Tee
"""
import boto3
from PIL import Image
import pytesseract
from boto3.dynamodb.conditions import Key, Attr
import re
import DBAccessKey

access_key_id_global=DBAccessKey.DBAccessKey.access_key_id_global
secret_access_key_global=DBAccessKey.DBAccessKey.secret_access_key_global
list_of_dict = []


class ImageToText:

    def __init__(self, name):
        self.name = name

    def extract_value(self, val_local):
        # extract whole text to string and number as different lines

        val_local1 = val_local.split()
        if val_local1[1] == '*':
            return val_local1[2]
        else:
            return val_local1[1]

    def print_filename(self):

        for filename in self.name:
            image = Image.open(filename)
            # Configure tesseract to treat each document line as a single line by setting --psm to 6
            text = pytesseract.image_to_string(image, lang="eng", config='--psm 6').splitlines()

            global Ref_no
            global Collected_Date_time

            result_dict = {
                "filename": filename
            }

            # TODO: Improve logic of looping to reduce processing time
            for val in text:

                if 'Collected' in val:
                    # remove alphabets
                    Collected_Date_time = ''.join(i for i in val if i.isdigit())
                    Collected_Date_time = Collected_Date_time.replace("/", '')
                    Collected_Date_time = Collected_Date_time.replace(" ", '')
                    Collected_Date_time = Collected_Date_time.replace(":", '')
                    result_dict['Date_Time'] = Collected_Date_time

                elif 'Reference' in val:
                    Ref_no = ImageToText.extract_value(self, val)
                    result_dict['Reference_No'] = Ref_no

                elif val:
                    field_str_list = ['Sodium', 'Potassium', 'Chloride', 'Bicarbonate', 'Urea', 'Creatinine', 'eGFR', 'T.Protein','Albumin', 'ALP', 'Bilirubin', 'GGT',
                                        'AST', 'ALT', 'HAEMOGLOBIN', 'RBC', 'PCV', 'MCV', 'MCHC', 'RDW', 'wcc', 'Neutrophils', 'Lymphocytes', 'Monocytes',
                                        'Eosinophils', 'Basophils', 'PLATELETS','ESR'] # T.Protein

                    for field_str in field_str_list:
                        if val.startswith(field_str):
                            result_str = ImageToText.extract_value(self, val)
                            result_dict[field_str] = result_str

                    if val.startswith('MCH') and not val.startswith('MCHC'):
                        mch = ImageToText.extract_value(self, val)
                        result_dict['MCH'] = mch

            list_of_dict.append(result_dict)

        return list_of_dict

    # TODO: Move these functions to another file
    def check_entry_exist(self, ref_no):

        database = boto3.resource('dynamodb', region_name='ap-southeast-2', aws_access_key_id=access_key_id_global,
                                  aws_secret_access_key=secret_access_key_global)
        table = database.Table('ME_CFS_DB')

        response = table.query(
            KeyConditionExpression=Key('Reference_No').eq(ref_no)
        )
        if response['Items']:
            return True
        else:
            return False

    def write_to_db(self, ref_no, date_time):
        # Read from DB to see if it exist, if it does do not create a new one.
        database = boto3.resource('dynamodb', region_name='ap-southeast-2', aws_access_key_id=access_key_id_global,
                                  aws_secret_access_key=secret_access_key_global)
        table = database.Table('ME_CFS_DB')

        response = table.put_item(
            Item={
                'Reference_No': ref_no,
                'Date_Time': int(date_time),
            }
        )

    def update_db(self, name, value, ref_no, collected_date_time):
        # check existing or not
        # update the existing record

        dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2', aws_access_key_id=access_key_id_global,
                                  aws_secret_access_key=secret_access_key_global)
        table = dynamodb.Table('ME_CFS_DB')
        Expression_string="set "+name+ "= :r";
        response = table.update_item(
            Key={
                'Reference_No': ref_no,
                'Date_Time': int(collected_date_time),
            },
            UpdateExpression=Expression_string,
            ExpressionAttributeValues={
                ':r': value,
            },
            ReturnValues="UPDATED_NEW"
        )


