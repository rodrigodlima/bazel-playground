import os
import boto3
from botocore.exceptions import ClientError


def get_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )


def list_bucket_files(bucket_name: str, prefix: str = '') -> list:
    s3_client = get_s3_client()
    files = []

    try:
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    files.append({
                        'key': obj['Key'],
                        'size': obj['Size'],
                        'last_modified': obj['LastModified'].isoformat()
                    })
    except ClientError as e:
        print(f"Error listing bucket files: {e}")
        raise

    return files


def main():
    bucket_name = os.environ.get('S3_BUCKET_NAME')

    if not bucket_name:
        print("Error: S3_BUCKET_NAME environment variable is required")
        return

    print(f"Listing files in bucket: {bucket_name}")

    files = list_bucket_files(bucket_name)

    if not files:
        print("No files found in bucket")
        return

    print(f"\nFound {len(files)} file(s):\n")
    for file in files:
        print(f"  {file['key']} ({file['size']} bytes) - {file['last_modified']}")


if __name__ == '__main__':
    main()
