#!/usr/bin/env python

import argparse
import boto3


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', help='AWS credentials profile to use')
    parser.add_argument('--region', help='Region to search. Eg: eu-west-1')
    args = parser.parse_args()

    if args.profile and args.region:
        ec2 = boto3.session.Session(profile_name=args.profile).client('ec2', region_name=args.region)
        autoscaling = boto3.session.Session(profile_name=args.profile).client('autoscaling', region_name=args.region)
    elif args.profile:
        ec2 = boto3.session.Session(profile_name=args.profile).client('ec2')
        autoscaling = boto3.session.Session(profile_name=args.profile).client('autoscaling')
    elif args.region:
        ec2 = boto3.client('ec2', region_name=args.region)
        autoscaling = boto3.client('autoscaling', region_name=args.region)
    else:
        ec2 = boto3.client('ec2')
        autoscaling = boto3.client('autoscaling')

    # fetch instance ids
    paginator = ec2.get_paginator('describe_instances')
    instance_ids = [instance['InstanceId']
                    for page in paginator.paginate()
                    for reservation in page['Reservations']
                    for instance in reservation['Instances']]
    if not instance_ids:
        print('No instances found. Exiting')
        exit(1)

    # fetch asgs instance ids
    paginator = autoscaling.get_paginator('describe_auto_scaling_groups')
    asg_instance_ids = [instance['InstanceId']
                        for page in paginator.paginate()
                        for asg in page['AutoScalingGroups']
                        for instance in asg['Instances']]

    non_asg_instances = set(instance_ids) - set(asg_instance_ids)
    print('{} Non-ASG Instances:'.format(len(non_asg_instances)))
    print(*non_asg_instances, sep='\n')

