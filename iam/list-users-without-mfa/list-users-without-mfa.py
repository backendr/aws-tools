#!/usr/bin/env python

import argparse
import boto3

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', help='AWS credentials profile to use')
    args = parser.parse_args()
    iam = boto3.session.Session(profile_name=args.profile).client('iam') if args.profile else boto3.client('iam')

    for users in iam.get_paginator('list_users').paginate():
        for user in users['Users']:
            mfa_devices = iam.list_mfa_devices(UserName=user['UserName'])
            if not mfa_devices['MFADevices']:
                print(user['UserName'])
