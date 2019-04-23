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
access_key_id_global='AKIAJVYE2V2GLH5NQDWA'
secret_access_key_global='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'
class ImageToText:

    def __init__(self, name):
        self.name = name

    #initiate to zero
    global Ref_no
    global Collected_Date_time

    def extract_value(val_local,name):

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

        dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2', aws_access_key_id=access_key_id_global,
                                  aws_secret_access_key=secret_access_key_global)
        table = dynamodb.Table('ME_CFS_DB')
        #Ref_no = "C0011"
        #Date_time = 123
        print("updateddb " + Ref_no + Collected_Date_time)
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
        print("UpdateItem succeeded:")


    def print_filename(self):

        image = Image.open(self.name)
        text = pytesseract.image_to_string(image, lang="eng").splitlines()
        input = ''
        global Ref_no
        global Collected_Date_time

        #print(text)
        counter = 0
        ##mock
        #Ref_no = "C0013"
        #Date_time = 123

        #exist = ImageToText.check_entry_exist(Ref_no)

        #if(exist):
        #    print("Entry already exist, do not create a new one")

        #else:
        #    print("Entry doesnt exist, create a new one")
        #    ImageToText.write_to_DB(Ref_no,Date_time)

        # initiate to check for misaligned variables
        check = 2
        count1 = 0
        count2 = 0
        misaligned = True
        s = []
        s2 = []

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

                    if val.startswith('Sodium'):
                        Sodium= ImageToText.extract_value(val,'Sodium')
                        print('The value of Sodium here is ',Sodium)
                        input= 'Sodium: '+Sodium
                        ImageToText.update_DB('Sodium',Sodium)

                    if val.startswith('Potassium'):
                        Potassium= ImageToText.extract_value(val,'Potassium')
                        print('The value of Potassium here is ',Potassium)
                        input = input+'\n'+'Potassium: ' + Potassium
                        ImageToText.update_DB('Potassium',Potassium)

                    if val.startswith('Chloride'):
                        Chloride= ImageToText.extract_value(val,'Chloride')
                        print('The value of Chloride here is ',Chloride)
                        input = input + '\n' + 'Chloride: ' + Chloride
                        ImageToText.update_DB('Chloride',Chloride)

                    if val.startswith('Bicarbonate'):
                        Bicarbonate= ImageToText.extract_value(val,'Bicarbonate')
                        print('The value of Bicarbonate here is ',Bicarbonate)
                        input = input + '\n' + 'Bicarbonate: ' + Bicarbonate
                        ImageToText.update_DB('Bicarbonate',Bicarbonate)

                    if val.startswith('Urea'):
                        Urea= ImageToText.extract_value(val,'Urea')
                        print('The value of Urea here is ',Urea)
                        input = input + '\n' + 'Urea: ' + Urea
                        ImageToText.update_DB('Urea',Urea)

                    if val.startswith('Creatinine'):
                        Creatinine= ImageToText.extract_value(val,'Creatinine')
                        print('The value of Creatinine here is ',Creatinine)
                        input = input + '\n' + 'Creatinine: ' + Creatinine
                        ImageToText.update_DB('Creatinine',Creatinine)

                    if val.startswith('eGFR'):
                        eGFR= ImageToText.extract_value(val,'eGFR')
                        print('The value of eGFR here is ',eGFR)
                        input = input + '\n' + 'eGFR here is ' + eGFR
                        ImageToText.update_DB('eGFR',eGFR)

                    if val.startswith('T.Protein') :
                        T_Protein= ImageToText.extract_value(val,'T.Protein')
                        print('The value of T.Protein here is ',T_Protein)
                        input = input + '\n' + 'T_Protein: ' + T_Protein
                        ImageToText.update_DB('T_Protein',T_Protein)

                    if val.startswith('Albumin'):
                        Albumin= ImageToText.extract_value(val,'Albumin')
                        print('The value of Albumin here is ',Albumin)
                        input = input + '\n' + 'Albumin: ' + Albumin
                        ImageToText.update_DB('Albumin',Albumin)

                    if val.startswith('ALP'):
                        ALP= ImageToText.extract_value(val,'ALP')
                        print('The value of ALP here is ',ALP)
                        input = input + '\n' + 'ALP: ' + ALP
                        ImageToText.update_DB('ALP',ALP)

                    if val.startswith('Bilirubin'):
                        Bilirubin= ImageToText.extract_value(val,'Bilirubin')
                        print('The value of Bilirubin here is ',Bilirubin)
                        input = input + '\n' + 'Bilirubin: ' + Bilirubin
                        ImageToText.update_DB('Bilirubin',Bilirubin)

                    if val.startswith('GGT'):
                        GGT= ImageToText.extract_value(val,'GGT')
                        print('The value of GGT here is ',GGT)
                        input = input + '\n' + 'GGT: ' + GGT
                        ImageToText.update_DB('GGT',GGT)

                    if val.startswith('AST'):
                        AST= ImageToText.extract_value(val,'AST')
                        print('The value of AST here is ',AST)
                        input = input + '\n' + 'AST: ' + AST
                        ImageToText.update_DB('AST',AST)

                    if val.startswith('ALT'):
                        ALT= ImageToText.extract_value(val,'ALT')
                        print('The value of ALT here is ',ALT)
                        input = input + '\n' + 'ALT: ' + ALT
                        ImageToText.update_DB('ALT',ALT)

                    if val.startswith('HAEMOGLOBIN'):
                        HAEMOGLOBIN= ImageToText.extract_value(val,'HAEMOGLOBIN')
                        print('The value of HAEMOGLOBIN here is ',HAEMOGLOBIN)
                        input = input + '\n' + 'HAEMOGLOBIN: ' + HAEMOGLOBIN
                        ImageToText.update_DB('HAEMOGLOBIN',HAEMOGLOBIN)

                    if val.startswith('RBC'):
                        RBC= ImageToText.extract_value(val,'RBC')
                        print('The value of RBC here is ',RBC)
                        input = input + '\n' + 'RBC: ' + RBC
                        ImageToText.update_DB('RBC',RBC)

                    if val.startswith('PCV'):
                        PCV= ImageToText.extract_value(val,'PCV')
                        print('The value of PCV here is ',PCV)
                        input = input + '\n' + 'PCV: ' + PCV
                        ImageToText.update_DB('PCV',PCV)

                    if val.startswith('MCV'):
                        MCV= ImageToText.extract_value(val,'MCV')
                        print('The value of MCV here is ',MCV)
                        input = input + '\n' + 'MCV: ' + MCV
                        ImageToText.update_DB('MCV',MCV)

                    if val.startswith('MCH') and not val.startswith('MCHC'):
                        MCH= ImageToText.extract_value(val,'MCH')
                        print('The value of MCH here is ',MCH)
                        input = input + '\n' + 'MCH: ' + MCH
                        ImageToText.update_DB('MCH',MCH)

                    if val.startswith('MCHC'):
                        MCHC= ImageToText.extract_value(val,'MCHC')
                        print('The value of MCHC here is ',MCHC)
                        input = input + '\n' + 'MCHC: ' + MCHC
                        ImageToText.update_DB('MCHC',MCHC)

                    if val.startswith('RDW'):
                        RDW= ImageToText.extract_value(val,'RDW')
                        print('The value of RDW here is ',RDW)
                        input = input + '\n' + 'RDW: ' + RDW
                        ImageToText.update_DB('RDW',RDW )

                    if val.startswith('wcc'):
                        wcc= ImageToText.extract_value(val,'wcc')
                        print('The value of wcc here is ',wcc)
                        input = input + '\n' + 'wcc: ' + wcc
                        ImageToText.update_DB('wcc',wcc)

                    if val.startswith('Neutrophils'):
                        Neutrophils= ImageToText.extract_value(val,'Neutrophils')
                        print('The value of Neutrophils here is ',Neutrophils)
                        input = input + '\n' + 'Neutrophils: ' + Neutrophils
                        ImageToText.update_DB('Neutrophils',Neutrophils)

                    if val.startswith('Lymphocytes'):
                        Lymphocytes= ImageToText.extract_value(val,'Lymphocytes')
                        print('The value of Lymphocytes here is ',Lymphocytes)
                        input = input + '\n' + 'Lymphocytes: ' + Lymphocytes
                        ImageToText.update_DB('Lymphocytes',Lymphocytes)

                    if val.startswith('Monocytes'):
                        Monocytes= ImageToText.extract_value(val,'Monocytes')
                        print('The value of Monocytes here is ',Monocytes)
                        input = input + '\n' + 'Monocytes: ' + Monocytes
                        ImageToText.update_DB('Monocytes',Monocytes)

                    if val.startswith('Eosinophils'):
                        Eosinophils= ImageToText.extract_value(val,'Eosinophils')
                        print('The value of Eosinophils here is ',Eosinophils)
                        input = input + '\n' + 'Eosinophils: ' + Eosinophils
                        ImageToText.update_DB('Eosinophils',Eosinophils)

                    if val.startswith('Basophils'):
                        Basophils= ImageToText.extract_value(val,'Basophils')
                        print('The value of Basophils here is ',Basophils)
                        input = input + '\n' + 'Basophils: ' + Basophils
                        ImageToText.update_DB('Basophils',Basophils)

                    if val.startswith('PLATELETS'):
                        PLATELETS= ImageToText.extract_value(val,'PLATELETS')
                        print('The value of PLATELETS here is ',PLATELETS)
                        input = input + '\n' + 'PLATELETS: ' + PLATELETS
                        ImageToText.update_DB('Eosinophils',Eosinophils)

                    if val.startswith('ESR'):
                        ESR= ImageToText.extract_value(val,'ESR')
                        print('The value of ESR here is ',ESR)
                        input = input + '\n' + 'ESR: ' + ESR
                        ImageToText.update_DB('ESR',ESR)

        GUI_bk.PageTwo.insert_results(input)
        print("Testing section")
        print(text[0])

        print('------------------Break----------------')
        # Create an S3 client
        #s3 = boto3.resource('s3', region_name='ap-southeast-2', aws_access_key_id=access_key_id_global,aws_secret_access_key=secret_access_key_global)

        # for bucket in s3.buckets.all():
        #    print(bucket.name)

        # uploading
       # data = open('C:/Users/young/Downloads/Sample.png', 'rb')
      #  s3.Bucket('mecfsbucket').put_object(Key='test2.jpg', Body=data)
        # downloading
        #s3.Bucket('mecfsbucket').download_file('test.jpg', 'C:/Users/young/Downloads/my_local_image.jpg')
