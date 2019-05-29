# Find ELB in Route53
Finds a matching Route53 entry for the given ELB DNS Name

### Usage
```
usage: find-elb-in-route53.py [-h] [--profile PROFILE] [--region REGION]
                              elb_dns

positional arguments:
  elb_dns            ELB DNS Name

optional arguments:
  -h, --help         show this help message and exit
  --profile PROFILE  AWS credentials profile to use
  --region REGION    Region to search. Eg: eu-west-1
```

### Output
```
example.com.
service-discovery.example.com.
```
or if no results
```
No record sets found
```
