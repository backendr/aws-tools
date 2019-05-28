# Find Non ASG Instances
Finds all EC2 instances that are not part of an Auto Scaling Group

### Usage
```
usage: find-non-asg-instances.py [-h] [--profile PROFILE] [--region REGION]

optional arguments:
  -h, --help         show this help message and exit
  --profile PROFILE  AWS credentials profile to use
  --region REGION    Region to search. Eg: eu-west-1
```

### Output
Outputs the number of non-asg instances, and their instance ids
```
5 non asg instances:
i-xxxxxxxxxxxxxxxxx
i-xxxxxxxxxxxxxxxxx
i-xxxxxxxxxxxxxxxxx
i-xxxxxxxxxxxxxxxxx
i-xxxxxxxxxxxxxxxxx
```