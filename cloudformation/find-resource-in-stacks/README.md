# Find Resource in Stacks
Finds the `PhysicalResourceId` of a resource in stacks which are not updating

### Use case
Trying to find if a resource is managed by Cloudformation, and which stack.

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
Searching for SomeName-ElasticL-XXXXXXXXXX in 584 Stacks ...
This can take up to 175 seconds

StackName-SomeName-Jenkins
```
or if nothing found
```
No matching resource found in 584 stacks
```