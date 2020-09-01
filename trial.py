import boto3

s3 = boto3.resource('s3')
bucket = s3.Bucket("datastorage-project")

for s3_file in bucket.objects.filter(Prefix="user/17/gitcommand.txt"):
    file_object = s3_file.key
    file_name = str(file_object.split('/')[-1])
    print(file_name)
    fileDown = "/home/ec2-user/"+file_name
    print('Downloading file {} ...'.format(file_object))
    bucket.download_file(file_object, fileDown)