# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 11:02:59 2019

@author: Nigel Tee
"""
import boto3
from PIL import Image
import pytesseract


class ImageToText:
    def __init__(self, name):
        self.name = name

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
                    val1 = val.split();
                    if val1[1] == '*':
                        print('Shout Sodium is high =', val1[2])
                    else:
                        print('Shout Sodium =', val1[1])
                        sodium = val1[1]

                if val.startswith('Potassium'):
                    val1 = val.split();
                    if val1[1] == '*':
                        print('Shout Potassium is high =', val1[2])
                        potassium = val1[2]
                    else:
                        print('Shout Potassium =', val1[1])

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
                'Potassium': potassium,

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