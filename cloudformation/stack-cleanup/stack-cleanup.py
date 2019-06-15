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

import boto3
import argparse
from datetime import datetime, timezone
from operator import itemgetter
from botocore.exceptions import ClientError
from time import sleep

SLEEP = 0.5
STACK_STATUS_FILTER = ['CREATE_COMPLETE',
                       'CREATE_FAILED',
                       'ROLLBACK_FAILED',
                       'ROLLBACK_COMPLETE',
                       'DELETE_FAILED',
                       'UPDATE_COMPLETE',
                       'UPDATE_ROLLBACK_FAILED',
                       'UPDATE_ROLLBACK_COMPLETE']

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', help='AWS credentials profile to use')
    parser.add_argument('--region', help='Region to search. Eg: eu-west-1')
    parser.add_argument('--age', action='store', required=True,
                        help='Age in days a stack needs to be to be considered for removal')
    parser.add_argument('--dry', action='store_true', help='Only print. Donesn\'t make changes')
    args = parser.parse_args()

    if args.profile and args.region:
        cfn_client = boto3.session.Session(profile_name=args.profile).client('cloudformation', region_name=args.region)
    elif args.profile:
        cfn_client = boto3.session.Session(profile_name=args.profile).client('cloudformation')
    elif args.region:
        cfn_client = boto3.client('cloudformation', region_name=args.region)
    else:
        cfn_client = boto3.client('cloudformation')

    # collect stacks which match STACK_STATUS_FILTER
    paginator = cfn_client.get_paginator('list_stacks')
    stacks = [stack
              for page in paginator.paginate(StackStatusFilter=STACK_STATUS_FILTER)
              for stack in page['StackSummaries']]

    # read whitelist file and ignore comments / empty lines
    whitelist_lines = [line.rstrip() for line in open('whitelist')]
    whitelist = [line.lower() for line in whitelist_lines if line and not line.startswith('#')]

    # add stacks to whitelisted / deleted lists
    print('Processing Stacks. This may take up to {}s\n'.format(len(stacks) * SLEEP))
    sleep(1)
    whitelisted, deleted = [], []
    for stack in stacks:
        # append stack age to stack dict
        stack_datetime = stack['LastUpdatedTime'] if 'LastUpdatedTime' in stack else stack['CreationTime']
        stack['age'] = datetime.now(timezone.utc) - stack_datetime

        # if delete has failed then try to delete again
        if 'DELETE_FAILED' in stack['StackStatus'] or stack['age'].days >= int(args.age):
            if [True for white in whitelist if white in stack['StackName'].lower()]:
                whitelisted.append(stack)
                continue
            # if deletion protection enabled, move to whitelist
            result = cfn_client.describe_stacks(StackName=stack['StackName'])
            if result['Stacks'][0]['EnableTerminationProtection']:
                whitelisted.append(stack)
            else:
                deleted.append(stack)
        sleep(SLEEP)

    print('\nOVER {} DAYS AND WHITELISTED / TERMINATION PROTECTED: {}'.format(int(args.age), len(whitelisted)))
    print('\n'.join(stack['StackName'] for stack in sorted(whitelisted, key=itemgetter('StackName'))))
    print('\n\nTO REMOVE: {}'.format(len(deleted)))
    print('\n'.join(stack['StackName'] for stack in sorted(deleted, key=itemgetter('StackName'))))
    print('\nSUMMARY:\nStacks over {} days and in the state:\n{}\nWhitelist / Termination Protected count: {}\n'
          'To Remove count: {}\n'.format(int(args.age), STACK_STATUS_FILTER, len(whitelisted), len(deleted)))

    if not args.dry:
        confirmation = input('\n\nContinue? Protected Stacks will not be removed [y/N]: ')
        if confirmation.lower() in ['y', 'yes']:
            for stack in deleted:
                try:
                    cfn_client.delete_stack(StackName=stack['StackName'])
                    print('[DELETION STARTED] {}'.format(stack['StackName']))
                except ClientError:
                    print('[SKIPPING] {} Termination Protection Enabled.'.format(stack['StackName']))
                    continue

