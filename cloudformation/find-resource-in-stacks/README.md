# Find Resource in Stacks
Finds the `PhysicalResourceId` of a resource in stacks which are not updating.

Handles Keyboard Interupts, so that you can kill a search and view any processed stacks.

Uses `backoff` for faster cloudformation API calls

### Use case
Trying to find if a resource is managed by Cloudformation, and which stack.

### Requirements
+ `boto3`
+ `backoff`
+ IAM permissions for `cloudformation:ListStacks`, `cloudformation:ListStackResources`

### Usage
```
usage: find-resource-in-stacks.py [-h] [--profile PROFILE] [--region REGION]
                                  resource

positional arguments:
  resource           Physical Resource Id

optional arguments:
  -h, --help         show this help message and exit
  --profile PROFILE  AWS credentials profile to use
  --region REGION    Region to search. Eg: eu-west-1
```

### Output
```
Searching for Jenkins in 584 Stacks ...
[CHECKING 1/584] Some-Stack-Name
[CHECKING 2/584] Another-Stack-Name
[CHECKING 3/584] Jenkins-Role
[CHECKING 4/584] Jenkins-Instance
...

SUMMARY:
Stacks Checked: 584
Stack Name:
    Jenkins-Role
Physical Resource IDs:
    Jenkins-role-HTF89AN83S
    Jenkins-Policy-ASDERF543E

Stack Name:
    Jenkins-Instance
Physical Resource IDs:
    Jenkins-Instance-HTFGF987UHB

```
or if nothing found
```
Nothing Found
```