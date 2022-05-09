"""
AWS services helper classes and functions for Crabada project
"""

import boto3

class SecretsManager:
    def __init__(self):
        self.client = boto3.client("secretsmanager")

    def __del__(self):
        del self.client

    def create_or_change_secret(self, name, value, desc):
        try:
            sec = self.get_secret_value(SecretId=name)
        except:
            self.client.create_secret(Name=name, Description=desc, SecretString=value, ForceOverwriteReplicaSecret=True)
            return
        self.client.put_secret_value(SecretId=name, SecretString=value)

    def __setitem__(self, key, val):
        self.create_or_change_secret(key, val, "")

    def __getitem__(self, key):
        try:
            return self.client.get_secret_value(SecretId=key)
        except:
            raise KeyError(key)

    def __delitem__(self, key):
        try:
            self.client.delete_secret(SecretId=key)
        except:
            pass
