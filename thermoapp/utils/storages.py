#from storages.backends.s3boto3 import S3Boto3Storage
#Standard libraries
import os
#aws
import boto3

# class StaticRootS3Boto3Storage(S3Boto3Storage):
#     location = "static"
#     default_acl = "public-read"
#
#
# class MediaRootS3Boto3Storage(S3Boto3Storage):
#     location = "media"
#     file_overwrite = False

#Upload image to AWS bucket
def upload_to_aws(img):
    # AWS credentials
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
    #Load credentials
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY,
                      aws_secret_access_key=AWS_SECRET_KEY)
    #Get bucket
    S3_BUCKET = os.environ.get('S3_BUCKET')
    #Upload
    s3.upload_fileobj(img, S3_BUCKET,'images/'+img.name, ExtraArgs={ "ContentType": "image/jpeg",
                                                                     'ACL':'public-read'})
