import boto3
s3=boto3.client('s3')
bucketName = "datastorage-project"

def createBucket(custId):
    folderName = "user/"+str(custId)
    s3.put_object(Bucket=bucketName, Key=(folderName+'/'))