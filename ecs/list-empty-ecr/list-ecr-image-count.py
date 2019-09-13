#! /usr/bin/env python3

# File: find_empty_ecr.py
# Author: matthew.lowe
# Description: Find ECR repositories with no images

import argparse
import boto3

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', help='AWS credentials profile to use')
    parser.add_argument('--region', help='Region to search. Eg: eu-west-1')
    parser.add_argument('--empty', action='store_true', help='Display only empty ECR')
    args = parser.parse_args()

    if args.profile and args.region:
        ecr = boto3.session.Session(profile_name=args.profile).client('ecr', region_name=args.region)
    elif args.profile:
        ecr = boto3.session.Session(profile_name=args.profile).client('ecr')
    elif args.region:
        ecr = boto3.client('ecr', region_name=args.region)
    else:
        ecr = boto3.client('ecr')

    print('Checking ECR...')
    repos = ecr.describe_repositories()
    for repo in repos['repositories']:
        images = ecr.list_images(repositoryName=repo['repositoryName'])
        if args.empty:
            if not images['imageIds']:
                print(f'{repo["repositoryName"]}')
            continue
        print(f'{repo["repositoryName"]}: {len(images["imageIds"])}')
