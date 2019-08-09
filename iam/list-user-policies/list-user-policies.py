import argparse
import boto3

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', help='AWS credentials profile to use')
    args = parser.parse_args()
    iam = boto3.session.Session(profile_name=args.profile).client('iam') if args.profile else boto3.client('iam')

    for users in iam.get_paginator('list_users').paginate():
        for user in users['Users']:
            attached_policies = iam.list_attached_user_policies(UserName=user['UserName'])
            if attached_policies['AttachedPolicies']:
                print(f'{user["UserName"]}:\n{attached_policies["AttachedPolicies"]}')
