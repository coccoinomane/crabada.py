# awssecrets is a AWS Secrets Manager key management script

What awssecrets is doing, is just that: adding, updating, listing and removing crabada.py private keys from AWS SM service.

## Installation

You gonna need a Python and a boto3. If you have running crabada.py (with Vladimir's updates) source tree, likely you will be okay. Copy script to your favorite location or run it from ./sbin directory of crabada.py

## Configuration.

You have to specify three AWS variables in your environment.

```
export AWS_ACCESS_KEY_ID=Your AWS access key goes here
export AWS_SECRET_ACCESS_KEY=Your AWS secret key goes here
export AWS_DEFAULT_REGION=us-west-1 or any other default AWS region
```

## Create or Update key

```
awssecrets create "vulogov1_PRIVATE_KEY" "secret1"
```

## List existing keys

```
awssecrets list
```

Samle output:

```
src.common.logger - DEBUG - Initializing AWS SN client
src.common.logger - DEBUG - AWS Secrets management tool
src.common.logger - DEBUG - list command invocated
src.common.logger - DEBUG - AWS RequestId: 979e5184-4318-486c-bcf8-ed05ae809cf9
Name                  Created                           Updated
--------------------  --------------------------------  --------------------------------
key2                  2022-05-09 20:06:01.538000-06:00  2022-05-09 20:06:01.577000-06:00
vulogov1_PRIVATE_KEY  2022-05-10 21:39:41.255000-06:00  2022-05-10 21:39:41.291000-06:00
```

## Delete key

```
awssecrets drop key2
```
