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
import GUI_bk
import DBAccessKey

access_key_id_global=DBAccessKey.DBAccessKey.access_key_id_global
secret_access_key_global=DBAccessKey.DBAccessKey.secret_access_key_global
list_of_dict = []
class ImageToText:

    def __init__(self, name):
        self.name = name

    #initiate to zero
    global Ref_no
    global Collected_Date_time

    def extract_value(val_local,name):
        # extrat whole text to string and number as different lines

        val_local1 = val_local.split()
        if val_local1[1] == '*':
           print('Shout',name,' is high =', val_local1[2])

           return val_local1[2]
        else:
        #  print('Shout',name,' =', val_local1[1])

           return val_local1[1]

    def check_entry_exist(Ref_no):

        dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2', aws_access_key_id=access_key_id_global,
                                  aws_secret_access_key=secret_access_key_global)
        table = dynamodb.Table('ME_CFS_DB')

        response = table.query(
            KeyConditionExpression=Key('Reference_No').eq(Ref_no)
        )
        if (response['Items']):
            for i in response['Items']:
                print(i['Reference_No'], ":", i['Date_Time'])
            return True
        else:
            print(response['Items'])
            print("It is empty")
            return False



    def write_to_DB(Ref_no,Date_time):
        #read from DB to see if it exist, if it does do not create a new one. 

        dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2', aws_access_key_id=access_key_id_global,
                                  aws_secret_access_key=secret_access_key_global)
        table = dynamodb.Table('ME_CFS_DB')

        response = table.put_item(
            Item={
                'Reference_No': Ref_no,
                'Date_Time': Date_time,
            }
        )

    def update_DB(name,value):
        # check existing or not
        # update the existing record

        dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2', aws_access_key_id=access_key_id_global,
                                  aws_secret_access_key=secret_access_key_global)
        table = dynamodb.Table('ME_CFS_DB')
        #Ref_no = "C0011"
        #Date_time = 123
        # print("updateddb " + Ref_no + Collected_Date_time)
        Expression_string="set "+name+ "= :r";
        response = table.update_item(
            Key={
                'Reference_No': Ref_no,
                'Date_Time': int(Collected_Date_time),
            },
            UpdateExpression=Expression_string,
            ExpressionAttributeValues={
                ':r': value,
            },
            ReturnValues="UPDATED_NEW"
        )
        # print("UpdateItem succeeded:")

    def print_filename(self):
# After refactor this def should be outside the print_filename function.
        def parse_result(field_str):
            if val.startswith(field_str):
                result_str= ImageToText.extract_value(val,field_str)
                # print(field_str + ' = ' +result_str)
                self.result_dict[field_str] = result_str
                string2=field_str.replace('.','_')
                ImageToText.update_DB(string2,result_str)

        #process it here. when it opens, it shouldnt be a tuple. should be string, loop it
        for filename in self.name:
            print("string output:",filename)
            image = Image.open(filename)
            text = pytesseract.image_to_string(image, lang="eng").splitlines()

            input = ''
            global Ref_no
            global Collected_Date_time
            
            counter = 0
            check = 2
            count1 = 0
            count2 = 0
            misaligned = True
            s = []
            s2 = []
            self.result_dict = {
                "filename" : filename
            }
# TODO: get the file name, I cannot find where is it
            for val in text:

                if val.startswith('Patient'):
                    # check if misaligned or not
                    check = 1

                    #not misaligned
                    if re.findall('[0-9]', val):
                        misaligned = False
                        print("aligned")

                if check != 2 and misaligned:
                    # check for digit, result of misaligned variables
                    if re.findall('[0-9]', val):
                        check = 0

                    # store misaligned variables
                    if check == 1 and val:
                        s = s + [val]
                        count1 = count1 + 1

                    # store misaligned variables' results
                    if check == 0 and val:
                        s2 = s2 + [val]
                        count2 = count2 + 1

                    if count1 == count2:
                        #print("count1 & 2 is" + str(count1) + " " + str(count2))
                        #print(s)
                        #print(s2)

                        #assume ref at position 4

                        Ref_no = s2[4]
                        Collected_Date_time_pre = s2[1]
                        Collected_Date_time_pre = Collected_Date_time_pre.replace("/", '')
                        Collected_Date_time_pre = Collected_Date_time_pre.replace(" ", '')
                        Collected_Date_time_pre = Collected_Date_time_pre.replace(":", '')
                        print("pre is" + Collected_Date_time_pre)
                        Collected_Date_time = Collected_Date_time_pre
                        print("ref no is " + Ref_no)
                        print("date time is " + Collected_Date_time)

                        #exist = ImageToText.check_entry_exist(Ref_no)

                        #if exist:
                        #    print("Entry already exist, do not create a new one")

                        #else:
                        #    print("Entry doesnt exist, create a new one")
                        #    ImageToText.write_to_DB(Ref_no ,int(Collected_Date_time))

                        check = 2# enable harvesting

                if check != 2 and not misaligned:

                    if 'Reported' in val:
                        Collected_Date_time = ''.join(i for i in val if i.isdigit())  #remove alphabets
                        Collected_Date_time = Collected_Date_time.replace("/", '')
                        Collected_Date_time = Collected_Date_time.replace(" ", '')
                        Collected_Date_time = Collected_Date_time.replace(":", '')
                        print("date time is " + Collected_Date_time)

                    if 'Reference' in val:
                        Ref_no = ImageToText.extract_value(val, 'Reference')
                        print("ref no is " + Ref_no)
                        check = 2

                elif check == 2:

                    if val:
                        print(counter, val)
                        counter = counter + 1
                        field_str_list = ['Sodium', 'Potassium', 'Chloride', 'Bicarbonate', 'Urea', 'Creatinine', 'eGFR', 'T.Protein','Albumin', 'ALP', 'Bilirubin', 'GGT',
                                            'AST', 'ALT', 'HAEMOGLOBIN', 'RBC', 'PCV', 'MCV', 'MCHC', 'RDW', 'wcc', 'Neutrophils', 'Lymphocytes', 'Monocytes',
                                            'Eosinophils', 'Basophils', 'PLATELETS','ESR'] # T.Protein
                        # I don't know what happend in T.Protein but there's a bug related with DB.
                        for field_str in field_str_list:
                            parse_result(field_str)

                        if val.startswith('MCH') and not val.startswith('MCHC') :
                            MCH= ImageToText.extract_value(val,'MCH')
                            print('The value of MCH here is ',MCH)
                            ImageToText.update_DB('MCH',MCH)
                            self.result_dict['MCH'] = MCH

            # print("Testing young-->",self.result_dict)
            list_of_dict.append(self.result_dict)
            # print("List of dict 2:", list_of_dict)


            # And I need a list of dictionary of the result.
            #[young] use this way to process t.protein and MCH, since they are not straightforward
'''
                        if val.startswith('T.Protein') :
                            T_Protein= ImageToText.extract_value(val,'T.Protein')
                            print('The value of T.Protein here is ',T_Protein)
                            input = input + '\n' + 'T_Protein: ' + T_Protein
                            ImageToText.update_DB('T_Protein',T_Protein)
                            self.result_dict[field_str] = result_str
                            
'''
            # GUI_bk.PageTwo.insert_results(input)
            # print("Testing section")
            # print(text[0])

            # print('------------------Break----------------')
        # Create an S3 client
        #s3 = boto3.resource('s3', region_name='ap-southeast-2', aws_access_key_id=access_key_id_global,aws_secret_access_key=secret_access_key_global)

        # for bucket in s3.buckets.all():
        #    print(bucket.name)

        # uploading
       # data = open('C:/Users/young/Downloads/Sample.png', 'rb')
      #  s3.Bucket('mecfsbucket').put_object(Key='test2.jpg', Body=data)
        # downloading
        #s3.Bucket('mecfsbucket').download_file('test.jpg', 'C:/Users/young/Downloads/my_local_image.jpg')
