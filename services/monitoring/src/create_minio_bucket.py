from decouple import config

from minio import Minio

accessID = config('S3_ROOT_USER')
accessSecret = config('S3_ROOT_PASSWORD')

minioUrl = 'http://127.0.0.1:19000'
bucketName = 'mlflow'

if accessID == None:
    print('[!] AWS_ACCESS_KEY_ID environemnt variable is empty! run \'source .env\' to load it from the .env file')
    exit(1)

if accessSecret == None:
    print('[!] AWS_SECRET_ACCESS_KEY environemnt variable is empty! run \'source .env\' to load it from the .env file')
    exit(1)

if minioUrl == None:
    print('[!] MLFLOW_S3_ENDPOINT_URL environemnt variable is empty! run \'source .env\' to load it from the .env file')
    exit(1)

if bucketName == None:
    print('[!] AWS_BUCKET_NAME environemnt variable is empty! run \'source .env\' to load it from the .env file')
    exit(1)

minioUrlHostWithPort = minioUrl.split('//')[1]
print('[*] minio url: ', minioUrlHostWithPort)

s3Client = Minio(
    minioUrlHostWithPort,
    access_key=accessID,
    secret_key=accessSecret,
    secure=False
)

s3Client.make_bucket(bucketName)
