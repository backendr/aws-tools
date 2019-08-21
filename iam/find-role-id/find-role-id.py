#!/usr/bin/env python3

import argparse
import boto3


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('id', help='Role ID to search for')
    parser.add_argument('--profile', help='AWS credentials profile to use')
    parser.add_argument('--region', help='Region to search. Eg: eu-west-1')
    args = parser.parse_args()

    if args.profile and args.region:
        iam = boto3.session.Session(profile_name=args.profile).client('iam', region_name=args.region)
    elif args.profile:
        iam = boto3.session.Session(profile_name=args.profile).client('iam')
    elif args.region:
        iam = boto3.client('iam', region_name=args.region)
    else:
        iam = boto3.client('iam')

    # get all stack names
    paginator = iam.get_paginator('list_roles')
    roles = [role
             for page in paginator.paginate()
             for role in page['Roles']]

    for role in roles:
        if args.id in role['RoleId']:
            print(f'Path: {role["Path"]}')
            print(f'RoleName: {role["RoleName"]}')
            print(f'RoleId: {role["RoleId"]}')
            print(f'Arn: {role["Arn"]}')
            print(f'CreateDate: {role["CreateDate"]}')
            print(f'AssumeRolePolicyDocument: {role["AssumeRolePolicyDocument"]}')
            exit(0)

    print('No match found')
