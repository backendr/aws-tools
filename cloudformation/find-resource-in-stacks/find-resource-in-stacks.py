#!/usr/bin/env python3

import argparse
import boto3
import backoff
from botocore.exceptions import ClientError

STACK_FILTER = ['CREATE_COMPLETE',
                'DELETE_FAILED',
                'UPDATE_COMPLETE',
                'UPDATE_ROLLBACK_COMPLETE']

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('resource', help='Physical Resource Id')
    parser.add_argument('--profile', help='AWS credentials profile to use')
    parser.add_argument('--region', help='Region to search. Eg: eu-west-1')
    args = parser.parse_args()

    if args.profile and args.region:
        cfn = boto3.session.Session(profile_name=args.profile).client('cloudformation', region_name=args.region)
    elif args.profile:
        cfn = boto3.session.Session(profile_name=args.profile).client('cloudformation')
    elif args.region:
        cfn = boto3.client('cloudformation', region_name=args.region)
    else:
        cfn = boto3.client('cloudformation')

    # get all stack names
    paginator = cfn.get_paginator('list_stacks')
    stack_names = [stack['StackName']
                   for page in paginator.paginate(StackStatusFilter=STACK_FILTER)
                   for stack in page['StackSummaries']]

    # search through stacks till finding a hit
    paginator = cfn.get_paginator('list_stack_resources')

    @backoff.on_exception(backoff.expo, ClientError)
    def find_resource_in_stack(stack_id):
        found = []
        for page in paginator.paginate(StackName=stack_id):
            for stack_resources in page['StackResourceSummaries']:
                if args.resource in stack_resources['PhysicalResourceId']:
                    found.append(stack_resources['PhysicalResourceId'])
        return found

    print(f'Searching for {args.resource} in {len(stack_names)} Stacks...')
    results = {}
    count = 1
    try:
        for stack_name in stack_names:
            print(f'[CHECKING {count}/{len(stack_names)}] {stack_name}')
            findings = find_resource_in_stack(stack_name)
            if findings:
                print(f'[FOUND] {stack_name}')
                results[stack_name] = findings
            count += 1
    except KeyboardInterrupt:
        print('KeyboardInterupt')

    # print a summary
    print('\n\nSUMMARY:')
    print(f'Stacks Checked: {count}')
    if results:
        for k in results.keys():
            print(f'Stack Name:\n\t{k}\nPhysical Resource IDs:')
            for v in results[k]:
                print(f'\t{v}')
            print()
    else:
        print('Nothing found')
