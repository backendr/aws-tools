# List ECR Image Count
Lists the number of images in each ECR

### Requirements
 + `boto3`
 + IAM permissions for `IAM:DescribeRepositorties`, `IAM:ListImages`


### Usage
```
usage: list_empty_ecr.py [-h] [--profile PROFILE] [--region REGION] [--empty]

optional arguments:
  -h, --help         show this help message and exit
  --profile PROFILE  AWS credentials profile to use
  --region REGION    Region to search. Eg: eu-west-1
  --empty            Display only empty ECR
```

### Output
```
Checking ECR...
eu-west-1/someimage-base: 21
eu-west-1/someimage-dev: 39
eu-west-1/someimage-mysql: 0
```
With `--empty` flag:
```
Checking ECR...
eu-west-1/someimage-mysql: 0
```
