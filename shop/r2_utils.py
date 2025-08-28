import boto3
from django.conf import settings

s3 = boto3.client(
    's3',
    region_name='auto',
    endpoint_url=settings.AWS_S3_ENDPOINT_URL,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
)

def upload_to_r2(file, filename):
    s3.upload_fileobj(
        Fileobj=file,
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=filename,
        ExtraArgs={'ACL': 'public-read'}
    )
    return f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{filename}"