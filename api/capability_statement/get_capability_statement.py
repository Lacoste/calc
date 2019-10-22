from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
import os,boto3
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
from botocore.exceptions import ClientError
from boto3.s3.transfer import S3Transfer
from django.http import HttpResponse,JsonResponse
from rest_framework.response import Response


def check(s3, bucket, key):
    try:
        s3.head_object(Bucket = bucket, Key = key)
    except ClientError as e:
        return int(e.response['Error']['Code']) != 404
    return True


@login_required
@require_http_methods(["GET", "POST"])
def get_capability_statment(request, contractnumber):
    AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
    AWS_REGION = settings.AWS_REGION
    AWS_BUCKET = settings.AWS_STORAGE_BUCKET_NAME

    required_data = contractnumber
    
    s3 = boto3.client('s3', AWS_REGION, aws_access_key_id = AWS_ACCESS_KEY_ID,
                      aws_secret_access_key = AWS_SECRET_ACCESS_KEY)
    try:
        s3bucket = s3.list_objects_v2(Bucket = AWS_BUCKET)
    except ClientError as e:
        response = JsonResponse({'Error': '1', 'ErrorMessage':'Invalid AWS Credentials'})
        return response

    # Only return the contents if we found some keys
    if s3bucket['KeyCount'] > 0:
        all_objects = s3bucket['Contents']
    else:
        response = JsonResponse({'Error': '1', 'ErrorMessage':'No Files Found on bucket'})
        return response


    objectsNeed = []
    date_arr = []
    for obj in  all_objects:
        obj_name =  str(obj["Key"]).split('.')
        if required_data == obj_name[0]:
            objectsNeed.append({obj['LastModified']:obj['Key']})
            date_arr.append(obj['LastModified'])
    
    if len(date_arr) == 0: #If invalid contract number given
        response = JsonResponse({'Error': '1', 'ErrorMessage':'Invalid Contract Number'})
        return response
    else:
        latest_update = max(date_arr)
        index_of_latest_update = date_arr.index(latest_update)
        latest_file = str(objectsNeed[index_of_latest_update].get(
                          date_arr[index_of_latest_update]))

        if check(s3, AWS_BUCKET, latest_file):
            try:
                file = s3.get_object(Bucket = AWS_BUCKET, Key = latest_file)
                ext_array = latest_file.split('.')
                response = FileResponse(file['Body'], content_type = 'application/' + ext_array[1])
                response['Content-Disposition'] = 'attachment; filename="' + latest_file + '"'
                return response
            except FileNotFoundError:
                response = JsonResponse({'Error': '1', 'ErrorMessage':'Error While Downloading'})
                return response

    
    