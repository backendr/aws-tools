#!/usr/bin/env python
import argparse
import boto3
import yaml


class Data:
    def __init__(self):
        self.data = {'Roles': {}}
        pass

    def add_role(self, role_name):
        self.data['Roles'][role_name] = {}

    def add_principal_type(self, role_name, principal_type):
        self.data['Roles'][role_name] = {'PrincipalTypes': {}}
        self.data['Roles'][role_name]['PrincipalTypes'][principal_type] = []

    def add_principal(self, role_name, principal_type, principal):
        self.data['Roles'][role_name]['PrincipalTypes'][principal_type].append(principal)

    def print(self):
        print(yaml.dump(self.data))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', help='AWS credentials profile to use')
    args = parser.parse_args()

    if args.profile:
        iam = boto3.session.Session(profile_name=args.profile).client('iam')
    else:
        iam = boto3.client('iam')
    roles = iam.list_roles()
    data = Data()

    while True:
        for role in roles.get('Roles', []):
            data.add_role(role['RoleName'])
            if not role['AssumeRolePolicyDocument']:
                pass
            statements = role['AssumeRolePolicyDocument'].get('Statement', [])
            for statement in statements:
                for principal_type in statement['Principal']:
                    data.add_principal_type(role['RoleName'], principal_type)
                    data.add_principal(role['RoleName'],
                                       principal_type,
                                       statement['Principal'][principal_type])

        if not roles['IsTruncated']:
            break
        roles = iam.list_roles(Marker=roles['Marker'])

    data.print()
