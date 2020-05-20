# Find Resources in Stacks
Finds one or more `PhysicalResourceId`s in stacks which are not updating.

Handles Keyboard Interupts, so that you can kill a search and view any processed stacks.

Uses `backoff` for faster cloudformation API calls.

Will stop scanning stacks once all resources have been found.

### Use case
+ Trying to find if a resource is managed by Cloudformation, and which stack.
+ Finding resources with non human readable names in stacks

### Requirements
+ `boto3`
+ `backoff`
+ IAM permissions for `cloudformation:ListStacks`, `cloudformation:ListStackResources`

### Usage
```
usage: find-resources-in-stacks.py [-h]
                                   [--resources RESOURCES [RESOURCES ...]]
                                   [--profile PROFILE] [--region REGION]

optional arguments:
  -h, --help            show this help message and exit
  --resources RESOURCES [RESOURCES ...]
                        One or more Physical Resource Ids
  --profile PROFILE     AWS credentials profile to use
  --region REGION       Region to search. Eg: eu-west-1

```

### Output
```
Searching for abc-le-1g76sm69fpb3n abc-le-1k8qcnhfm52ql in 584 Stacks ...
[FOUND 1/584] Reddis-Stack
[CHECKING 2/584] Another-Stack-Name
[CHECKING 3/584] Jenkins-Instance
[FOUND 4/584] Another-Reddis-Stack

...

SUMMARY:
Stacks Checked: 4
Stack Name:
	MtgApi-Stage-LegoResources
Physical Resource ID:
	abc-le-1g76sm69fpb3n

Stack Name:
	MtgApi-Prod-LegoResources
Physical Resource ID:
	abc-le-1k8qcnhfm52ql

```
or if nothing found
```
Nothing Found
```