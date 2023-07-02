import boto3
from PIL import Image
import os

s3_client = boto3.client('s3')
thumbnail_bucket = 'thumbnail-bucket123'  # Update with your thumbnail bucket name


def lambda_handler(event, context):
    for record in event['Records']:
        # Get the S3 bucket and object key from the event record
        source_bucket = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']
        
        # Generate thumbnail image
        download_path = '/tmp/original.jpg'  # Temporary path to store the downloaded image
        thumbnail_image = generate_thumbnail(source_bucket, object_key, download_path)
        
        # Upload the thumbnail image to the thumbnail bucket
        upload_thumbnail(thumbnail_image, object_key, download_path)
        
    return {
        'statusCode': 200,
        'body': 'Thumbnail generation and upload complete'
    }

def generate_thumbnail(bucket, key, download_path):
    # Download the image from the source bucket
    s3_client.download_file(bucket, key, download_path)
    
    # Generate thumbnail using Pillow
    with Image.open(download_path) as image:
        image.thumbnail((100, 100))
        thumbnail = image.copy()
    
    # Return the thumbnail image
    return thumbnail

def upload_thumbnail(image, key, download_path):
    # Save the thumbnail image to a temporary file
    thumbnail_path = '/tmp/thumbnail.jpg'  # Temporary path to store the thumbnail image
    image.save(thumbnail_path, 'JPEG')
    
    # Upload the thumbnail image to the thumbnail bucket
    s3_client.upload_file(thumbnail_path, thumbnail_bucket, key)
    
    # Delete the temporary files
    os.remove(download_path)
    os.remove(thumbnail_path)
 