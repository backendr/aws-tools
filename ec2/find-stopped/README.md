# Find Stopped EC2
Finds stopped EC2 instances.

Example use cases:

+ Finding instances that can be terminated

### Usage
```
usage: find-stopped-ec2.py [-h] [--profile PROFILE] [--region REGION]

optional arguments:
  -h, --help         show this help message and exit
  --profile PROFILE  AWS credentials profile to use
  --region REGION    Region to search. Eg: eu-west-1

```
If no `--profile` is provided, the default will be used.

### Output
```
Name: INSTANCE_NAME
InstanceId: INSTANCE_ID
Location: VPCID SUBNETID
State: INSTANCE_STATE
Date Stopped: DATE

...

...
```
