# Find Public IPs
Finds EC2 instances with `PublicIpAddress`.

Example use cases:

+ Finding instances have public IPs
    + Auditing
    + Instance should not have public IP

### Usage
```
usage: find-public-ips.py [-h] [--profile PROFILE] [--region REGION]

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
LaunchTime: DATE
PublicIp: PUBLIC_IP
State: INSTANCE_STATE
Location: VPCID SUBNETID

...

...
```
