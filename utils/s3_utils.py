import boto3
import os


def download_s3_folder(local_folder, s3_prefix):
    """
    Downloads all files from a specific S3 folder to a local folder.

    Environment Variables (must be set beforehand):
    - AWS_ACCESS_KEY: AWS access key ID.
    - AWS_SECRET_KEY: AWS secret access key.
    - AWS_BUCKET: Name of the S3 bucket.

    Arguments:
    - local_folder (str): The local directory where files will be downloaded.
    - s3_prefix (str): The destination folder path (prefix) in the S3 bucket.

    This function connects to AWS S3, lists all files under a specific prefix path,
    and downloads them to the local folder while preserving the folder structure.
    """
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
    BUCKET_NAME = os.getenv("AWS_BUCKET")

    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
    )

    paginator = s3.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=BUCKET_NAME, Prefix=s3_prefix)

    for page in pages:
        for obj in page.get("Contents", []):
            s3_key = obj["Key"]

            # Skip directories
            if s3_key.endswith("/") or s3_key == s3_prefix:
                continue

            # Determine relative local path and create directories if needed
            relative_path = os.path.relpath(s3_key, s3_prefix)
            local_path = os.path.join(local_folder, relative_path)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            print(f"Downloading s3://{BUCKET_NAME}/{s3_key} → {local_path}")
            s3.download_file(BUCKET_NAME, s3_key, local_path)


def upload_file_to_s3(file_path, s3_prefix):
    """
    Uploads a single file to a specific folder in an S3 bucket.

    Environment Variables (must be set beforehand):
    - AWS_ACCESS_KEY: AWS access key ID.
    - AWS_SECRET_KEY: AWS secret access key.
    - AWS_BUCKET: Name of the S3 bucket.

    Arguments:
    - file_path (str): The full path of the local file to upload.
    - s3_prefix (str): The destination folder path (prefix) in the S3 bucket.

    This function uploads the file to the specified location inside the S3 bucket.
    """
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
    BUCKET_NAME = os.getenv("AWS_BUCKET")

    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
    )

    file_name = os.path.basename(file_path)
    s3_key = f"{s3_prefix}/{file_name}".replace("\\", "/")

    print(f"Uploading {file_path} → s3://{BUCKET_NAME}/{s3_key}")
    s3.upload_file(file_path, BUCKET_NAME, s3_key)
