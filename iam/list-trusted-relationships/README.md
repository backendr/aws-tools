# List Trusted Relationships
Prints role names and the trusted relationships for the provided `profile`.

Example use cases:

  + You want a quick overview of role access
  + You want to audit trusted relationships for roles
  + You want to parse the YAML output for processing

### Requirements

+ Your `profile` credentials must allow you to `iam:ListRoles`.

+ `boto3` must be installed.

### Usage

`./list-trusted-relationships {profile}`

Where `profile` is the name of the credentials you want to use.

### Output

Output is in `yaml`:

```yaml
Roles:
  <role_name>:
    PrincipalTypes:
      <principal_type>:
      - [<item1>, <item2>, <item3>]
```

Example output:

```yaml
Roles:
  rds-monitoring-role:
    PrincipalTypes:
      Service:
      - [monitoring.rds.amazonaws.com, rds.amazonaws.com]
  developer-role:
    PrincipalTypes:  
      AWS:
      - ['arn:aws:iam::12345678910:root', 'arn:aws:iam::12345678910:root']
```

