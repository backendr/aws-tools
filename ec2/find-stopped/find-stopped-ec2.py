#!/usr/bin/env python3

# Copyright (c) 2019 Matthew Lowe
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import argparse

import boto3


def find_name(instance):
    for tag in instance['Tags']:
        if 'Name' in tag['Key']:
            return tag['Value']
    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', help='AWS credentials profile to use')
    parser.add_argument('--region', help='Region to search. Eg: eu-west-1')
    args = parser.parse_args()

    if args.profile and args.region:
        ec2 = boto3.session.Session(profile_name=args.profile).client('ec2', region_name=args.region)
    elif args.profile:
        ec2 = boto3.session.Session(profile_name=args.profile).client('ec2')
    elif args.region:
        ec2 = boto3.client('ec2', region_name=args.region)
    else:
        ec2 = boto3.client('ec2')

    # fetch instance metadata
    response = ec2.describe_instances()
    if not response:
        print('Problem fetching instances.')
        exit(1)
    if not response['Reservations']:
        print('No instances found')
        exit(0)

    # find stopped instances
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            if 'stopped' in instance['State']['Name']:
                print('Name: %s' % find_name(instance))
                print('InstanceId: %s' % (instance['InstanceId']))
                print('Location: %s %s' % (instance['VpcId'], instance['SubnetId']))
                print('State: %s' % instance['State']['Name'])
                print('Date stopped: %s' % instance['StateTransitionReason'])
                print()
