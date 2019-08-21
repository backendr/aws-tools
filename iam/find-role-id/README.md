# Find Role Id
Finds matching role IDs and prints info

### Use case
You work with Role IDs rather than Role names, and want to find the role.

### Requirements
+ `boto3`
+ IAM permissions for `iam:ListRoles`

### Usage
```
usage: find-role-id.py [-h] [--profile PROFILE] [--region REGION] id

positional arguments:
  id                 Role ID to search for

optional arguments:
  -h, --help         show this help message and exit
  --profile PROFILE  AWS credentials profile to use
  --region REGION    Region to search. Eg: eu-west-1

```

### Output
```
Path: /
RoleName: JenkinsRole
RoleId: ABCDEFGHIJKLMNOPQRST
Arn: arn:aws:iam::12345678910:role/JenkinsRole
CreateDate: 2019-03-11 10:04:29+00:00
AssumeRolePolicyDocument: {'Version': '2008-10-17', 'Statement': [{'Effect': 'Allow', 'Principal': {'AWS': 'arn:aws:iam::12345678910:root'}, 'Action': 'sts:AssumeRole'}]}
```