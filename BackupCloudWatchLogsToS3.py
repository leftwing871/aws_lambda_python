import json
import urllib.parse
import boto3
import json
import collections
from datetime import datetime, date, time, timedelta


s3 = boto3.client('s3')

bucketName = 'product-bk-cloudwatchlogs'
logGroupName = 'product-Spring-log'
# key = '{}.json'.format(logGroupName)


def lambda_handler(event, context):
    
    
    try:
        today = date.today()
        yesterday = date.today() - timedelta(1)
        
        targetday = yesterday
        # 장애처리시 사용
        ##targetday = datetime(2021, 9, 2, 0, 0, 0)
        targetday = datetime.combine(targetday, time())

        from_ = datetime(targetday.year, targetday.month, targetday.day, 0, 0, 0)
        to_ = (datetime(targetday.year, targetday.month, targetday.day, 23, 59, 59) + timedelta(seconds=1))
        

        # from_s = '{}{}{}000000'.format(targetday.year, targetday.month, targetday.day)
        
        # from_timestamp = time.mktime(datetime.strptime(from_s, 'YYYYMMDD%H%M%S'))
        # print("from_timestamp: " + str(from_timestamp))
        
        
        print("targetday: " + targetday.strftime("YYYYMMDD HH:mm:ss (%Y%m%d %H:%M:%S)"))
        print("from_: " + from_.strftime("YYYYMMDD HH:mm:ss (%Y%m%d %H:%M:%S)"))
        print("to_: " + to_.strftime("YYYYMMDD HH:mm:ss (%Y%m%d %H:%M:%S)"))
        
        print("from_ timestamp: " + str(int(from_.timestamp() * 1000)))
        print("to_ timestamp: " + str(int(to_.timestamp() * 1000)))
        
        exported_folder_name = '{0}-{1}'.format(logGroupName, targetday.strftime("%Y-%m-%d"))

        # unix_start = datetime(1970,1,1,0,0,0)
        client = boto3.client('logs')
        
        response = client.create_export_task(
            taskName='export_cw_to_s3_{}'.format(exported_folder_name + date.today().strftime("%Y%m%d%H%M%S")),
            logGroupName=logGroupName,
            ##fromTime=int((from_-unix_start).total_seconds() * 1000),
            ##to=int((to_-unix_start).total_seconds() * 1000),
            fromTime=int(from_.timestamp() * 1000),
            to=int(to_.timestamp() * 1000),
            ##fromTime=int('1630594800000'),
            ##to=int('1630641599000'),
            destination=bucketName,
            destinationPrefix=exported_folder_name
        )
        
        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise Exception('ResponseMetadata HTTPStatusCode is ' + str(response["ResponseMetadata"]["HTTPStatusCode"]) + ' ')
        
        print(response)
        
    except Exception as e:
        print(e)
        raise e
