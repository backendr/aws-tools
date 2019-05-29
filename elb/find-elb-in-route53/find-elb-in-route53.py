#! /usr/bin/env python3
import argparse
import boto3

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('elb_dns', help='ELB DNS Name')
    parser.add_argument('--profile', help='AWS credentials profile to use')
    parser.add_argument('--region', help='Region to search. Eg: eu-west-1')
    args = parser.parse_args()

    if args.profile and args.region:
        route53 = boto3.session.Session(profile_name=args.profile).client('route53', region_name=args.region)
    elif args.profile:
        route53 = boto3.session.Session(profile_name=args.profile).client('route53')
    elif args.region:
        route53 = boto3.client('route53', region_name=args.region)
    else:
        route53 = boto3.client('route53')

    # fetch all of the hosted zones
    paginator = route53.get_paginator('list_hosted_zones')
    hosted_zones = [hosted_zone
                    for page in paginator.paginate()
                    for hosted_zone in page['HostedZones']]

    # try and find the elb dns in the record sets of each hosted zone
    paginator = route53.get_paginator('list_resource_record_sets')
    found_record_sets = []
    for hosted_zone in hosted_zones:
        record_sets = [record_set['Name']
                       for page in paginator.paginate(HostedZoneId=hosted_zone['Id'])
                       for record_set in page['ResourceRecordSets']
                       if 'AliasTarget' in record_set
                       if args.elb_dns in record_set['AliasTarget']['DNSName']]
        if record_sets:
            found_record_sets.append(record_sets[0])

    if found_record_sets:
        print(*found_record_sets, sep='\n')
    else:
        print('No record sets found')



