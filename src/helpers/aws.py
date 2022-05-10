"""
AWS services helper classes and functions for Crabada project
"""

import boto3
from src.common.logger import logger

class SecretsManager:
    def __init__(self):
        logger.debug("Initializing AWS SN client")
        self.client = boto3.client("secretsmanager")

    def __del__(self):
        del self.client

    def create_or_change_secret(self, name, value, desc):
        try:
            sec = self.get_secret_value(SecretId=name)
        except:
            logger.debug("Creating AWS SM secret: %s"%name)
            self.client.create_secret(Name=name, Description=desc, SecretString=value, ForceOverwriteReplicaSecret=True)
            return
        logger.debug("Creating AWS SM secret: %s"%name)
        self.client.put_secret_value(SecretId=name, SecretString=value)

    def __setitem__(self, key, val):
        self.create_or_change_secret(key, val, "")

    def __getitem__(self, key):
        try:
            return self.client.get_secret_value(SecretId=key)
        except:
            logger.error("AWS SM secret not found: %s"%name)
            raise KeyError(key)

    def __delitem__(self, name):
        try:
            logger.debug("Removing AWS SM secret: %s"%name)
            self.client.delete_secret(SecretId=name)
        except:
            logger.error("Handled error happens during removal of AWS SM secret: %s"%name)
            pass

    def keys(self):
        res = self.client.list_secrets(SortOrder="asc")
        rsp = res["ResponseMetadata"]
        logger.debug("AWS RequestId: %s"%rsp["RequestId"])
        return res["SecretList"]
