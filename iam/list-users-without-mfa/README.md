# List Users Without MFA
Lists users without an MFA device attached to their IAM user.

Example use cases:
+ Security

### Requirements
+ Your `profile` must be able to `iam:ListUsers` and `iam:ListMFADevices`
+ `boto3` must be installed

### Usage
```
usage: list-users-without-mfa.py [-h] [--profile PROFILE]

optional arguments:
  -h, --help         show this help message and exit
  --profile PROFILE  AWS credentials profile to use

```

### Output
```
joe.blogs@example.com
john.doe@example.com

```


