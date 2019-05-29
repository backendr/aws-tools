#!/usr/bin/env python3

import argparse
import boto3
from time import sleep

STACK_FILTER = ['CREATE_COMPLETE',
                'DELETE_FAILED',
                'UPDATE_COMPLETE']

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('resource', help='Physical Resource Id')
    parser.add_argument('--profile', help='AWS credentials profile to use')
    parser.add_argument('--region', help='Region to search. Eg: eu-west-1')
    args = parser.parse_args()

    if args.profile and args.region:
        cloudformation = boto3.session.Session(profile_name=args.profile).client('cloudformation', region_name=args.region)
    elif args.profile:
        cloudformation = boto3.session.Session(profile_name=args.profile).client('cloudformation')
    elif args.region:
        cloudformation = boto3.client('cloudformation', region_name=args.region)
    else:
        cloudformation = boto3.client('cloudformation')

    # get all stacks
    paginator = cloudformation.get_paginator('list_stacks')
    stack_names = [stack['StackName']
                   for page in paginator.paginate(StackStatusFilter=STACK_FILTER)
                   for stack in page['StackSummaries']]

    # search through stacks till finding a hit
    paginator = cloudformation.get_paginator('list_stack_resources')

    def has_resource_in_stack(stack_id):
        for page in paginator.paginate(StackName=stack_id):
            for stack_resources in page['StackResourceSummaries']:
                if args.resource in stack_resources['PhysicalResourceId']:
                    return True
        return False

    print('Searching for {} in {} Stacks ...\nThis can take up to {} seconds\n'.format(
        args.resource, len(stack_names), int(0.3 * len(stack_names))))
    for stack_name in stack_names:
        if has_resource_in_stack(stack_name):
            print(stack_name)
            exit(0)
        sleep(0.3)

    print('No matching resource found in {} stacks'.format(len(stack_names)))
