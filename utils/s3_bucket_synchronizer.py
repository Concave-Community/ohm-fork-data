import boto3


def upload_file_to_s3(data_dir: str, file_name: str):
    s3 = boto3.resource('s3')
    for bucket in s3.buckets.all():
        print(bucket.name)
    data = open(data_dir + file_name, 'rb')
    s3.Bucket('my-bucket').put_object(Key=file_name, Body=data)
