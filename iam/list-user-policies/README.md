# List User Policies
Prints users who have policies attached directly to them.

Example use cases:
+ Finding users with custom permissions

### Requirements
+ Your `profile` must be able to `iam:ListUsers` and `iam:ListAttachedUserPolicies`
+ `boto3` must be installed

### Usage
```
usage: list-user-policies.py [-h] [--profile PROFILE]

optional arguments:
  -h, --help         show this help message and exit
  --profile PROFILE  AWS credentials profile to use
````

If `--profile` is not used, the default will be used.

### Output

```
joe.blogs@example.com:
[{'PolicyName': 'AdministratorAccess', 'PolicyArn': 'arn:aws:iam::aws:policy/AdministratorAccess'}]
john.doe@example.com:
[{'PolicyName': 'AssumeDev', 'PolicyArn': 'arn:aws:iam::12345678910:policy/AssumeDev'},{'PolicyName': 'AssumeProd', 'PolicyArn': 'arn:aws:iam::12345678910:policy/AssumeProd'}]
```