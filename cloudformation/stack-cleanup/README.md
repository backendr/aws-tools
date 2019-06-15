# Stack Cleanup
Allows you to find stacks that have not been updated for a period and remove them.

Will collect all stacks that are not being updated, check its age and print the results.

You must confirm the list before removal happens.

Stacks that are Termination Protected will not be removed.

### Use Cases

+ Automated cleanup of stacks in a development environment

### Requirement

+ `boto3`
+ IAM user with `Cloudformation::list_stacks`, `Cloudformation::describe_stacks`, `Cloudformation::delete_stack`

### Usage
```
stack-cleanup.py [-h] [--profile PROFILE] [--region REGION] --age AGE
                        [--dry]

optional arguments:
  -h, --help         show this help message and exit
  --profile PROFILE  AWS credentials profile to use
  --region REGION    Region to search. Eg: eu-west-1
  --age AGE          Age in days a stack needs to be to be considered for
                     removal
  --dry              Only print. Donesn't make changes
```
`--age` is required, which is the number of days since the stack was last updated.

`--dry` will only print the stacks. Use this to validate the stacks to remove.

##### Example Usage
`./stack-cleanup --age 30 --dry`

> Check output

`./stack-cleanup --age 30`

> Check output and enter \`Y\`

### Whitelist
For added control you can use the whitelist file.

If the strings in the whitelist file are in the stack name, the stack will be ignored.

This can be useful if you dont want to, or unable to, set stack termination protection.
The whitelist can be used in conjunction with Termination Protection.

For example, you can add a line `s3` to the whitelist to ensure stacks with that string are not removed.
This can be useful if you dont want to remove stateful stacks with common names.

Stack name matching is case insensitive.

### Output
```
Processing Stacks. This may take up to 147.0s


OVER 30 DAYS AND WHITELISTED / TERMINATION PROTECTED: 32
Development-S3-Service-Bucket
Development-Frontend-Resources
...

TO REMOVE: 29
Development-EnvResources-ExportService
Development-Lambda-ExportProxy
...

SUMMARY:
Stacks over 30 days and in the state:
['CREATE_COMPLETE', 'CREATE_FAILED', 'ROLLBACK_FAILED', 'ROLLBACK_COMPLETE', 'DELETE_FAILED', 'UPDATE_COMPLETE', 'UPDATE_ROLLBACK_FAILED', 'UPDATE_ROLLBACK_COMPLETE']
Whitelist / Termination Protected count: 32
To Remove count: 29
```