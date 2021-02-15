: '
    This script should run on the first deployment. Thereby, allowing creation of pre-required resources to be created.

    Tags (Case Sensitive):
    -s      SAM/CloudFormation Stack Name
    -b      S3 Bucket Name
    
    Example of Command:
    bash deploy.sh -s jeff-aws-aiml-stack -b jeff-aws-aiml-bucket

'

#!/bin/bash
set -eo pipefail

while getopts s:b: option
    do
    case ${option}
        in
        s) STACK_NAME=${OPTARG};;
        b) BUCKET_NAME=${OPTARG};;
    esac
done

[ -z ${STACK_NAME}  ] && echo "Error: STACK_NAME (-s) argument is missing." && exit 1;
[ -z ${BUCKET_NAME} ] && echo "Error: BUCKET_NAME (-b) argument is missing." && exit 1;

# check and create s3 bucket if not exists
if aws s3api head-bucket --bucket $BUCKET_NAME 2>/dev/null; 
then
    echo $BUCKET_NAME
else
    aws s3 mb s3://$BUCKET_NAME
fi

# build dependencies (if any)
sam build

# put openapi file into s3 bucket
aws s3api put-object --bucket $BUCKET_NAME --key $STACK_NAME/openapi-spec.yaml --body ./openapi-spec.yaml

# package sam template (to be compatible with cloudformation template) 
# then upload required files (e.g. dependencies) to specified bucket
sam package --output-template-file packaged.yaml --s3-bucket $BUCKET_NAME --s3-prefix ${STACK_NAME}

# deploy packaged.yaml file and upload to specified bucket
sam deploy --template-file packaged.yaml --s3-bucket $BUCKET_NAME --s3-prefix ${STACK_NAME} --stack-name $STACK_NAME --capabilities CAPABILITY_IAM --parameter-overrides S3BucketName=${BUCKET_NAME}
