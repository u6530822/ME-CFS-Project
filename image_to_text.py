# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 11:02:59 2019

@author: Nigel Tee
"""
import boto3
from PIL import Image
import pytesseract
import re


class ImageToText:
    def __init__(self, name):
        self.name = name

    def extract_value(val_local,name):

        val_local1 = val_local.split();
        if val_local1[1] == '*':
           print('Shout ',name,' is high =', val_local1[2])
           return val_local1[2];
        else:
           print('Shout', name ,' =', val_local1[1])
           return val_local1[1]


    def print_filename(self):
        image = Image.open(self.name)
        text = pytesseract.image_to_string(image, lang="eng").splitlines();
        #print(text)
        counter = 0

        for val in text:
            if val:
                print(counter, val)
                counter = counter + 1

                if val.startswith('Sodium'):
                    Sodium= ImageToText.extract_value(val,'Sodium')
                    print('The value of Sodium here is ',Sodium)

                if val.startswith('Potassium'):
                    Potassium= ImageToText.extract_value(val,'Potassium')
                    print('The value of Potassium here is ',Potassium)

                if val.startswith('Chloride'):
                    Chloride= ImageToText.extract_value(val,'Chloride')
                    print('The value of Chloride here is ',Chloride)

                if val.startswith('Bicarbonate'):
                    Bicarbonate= ImageToText.extract_value(val,'Bicarbonate')
                    print('The value of Bicarbonate here is ',Bicarbonate)

                if val.startswith('Urea'):
                    Urea= ImageToText.extract_value(val,'Urea')
                    print('The value of Urea here is ',Urea)

                if val.startswith('Creatinine'):
                    Creatinine= ImageToText.extract_value(val,'Creatinine')
                    print('The value of Creatinine here is ',Creatinine)

                if val.startswith('eGFR'):
                    eGFR= ImageToText.extract_value(val,'eGFR')
                    print('The value of eGFR here is ',eGFR)

                if val.startswith('T.Protein') :
                    T_Protein= ImageToText.extract_value(val,'T.Protein')
                    print('The value of T.Protein here is ',T_Protein)

                if val.startswith('Albumin'):
                    Albumin= ImageToText.extract_value(val,'Albumin')
                    print('The value of Albumin here is ',Albumin)

                if val.startswith('ALP'):
                    ALP= ImageToText.extract_value(val,'ALP')
                    print('The value of ALP here is ',ALP)

                if val.startswith('Bilirubin'):
                    Bilirubin= ImageToText.extract_value(val,'Bilirubin')
                    print('The value of Bilirubin here is ',Bilirubin)

                if val.startswith('GGT'):
                    GGT= ImageToText.extract_value(val,'GGT')
                    print('The value of GGT here is ',GGT)

                if val.startswith('AST'):
                    AST= ImageToText.extract_value(val,'AST')
                    print('The value of AST here is ',AST)

                if val.startswith('ALT'):
                    ALT= ImageToText.extract_value(val,'ALT')
                    print('The value of ALT here is ',ALT)
        print("Testing section")
        print(text[0])
        access_key_id = 'A'
        secret_access_key ='D'

        dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2', aws_access_key_id=access_key_id,aws_secret_access_key=secret_access_key)

        table = dynamodb.Table('ME_CFS_DB')

        Ref_no = "C0011"
        Date_time = 123

        response = table.put_item(
            Item={
                'Reference_No': Ref_no,
                'Date_Time': Date_time,
                'Sodium': sodium,


            }
        )

        print('------------------Break----------------')
        # Create an S3 client
        s3 = boto3.resource('s3', region_name='ap-southeast-2', aws_access_key_id=access_key_id,aws_secret_access_key=secret_access_key)

        # for bucket in s3.buckets.all():
        #    print(bucket.name)

        # uploading
        data = open('C:/Users/young/Downloads/Sample.png', 'rb')
        s3.Bucket('mecfsbucket').put_object(Key='test2.jpg', Body=data)
        # downloading
        #s3.Bucket('mecfsbucket').download_file('test.jpg', 'C:/Users/young/Downloads/my_local_image.jpg')