"""
VAULT services helper classes and functions for Crabada project
"""

import os
import hvac
from src.common.logger import logger

class VaultSecretsManager:
    def __init__(self):
        logger.debug("Initializing VAULT client")
        self.url = os.environ["VAULT_URL"]
        self.token = os.environ["VAULT_TOKEN"]
        self.client = hvac.Client(url=self.url, token=self.token)

    def __del__(self):
        del self.client

    def create_or_change_secret(self, name, value, desc):
        logger.debug("Creating/Updating VAULT secret: %s"%name)
        self.client.secrets.kv.v2.create_or_update_secret(path=name, secret=value)

    def __setitem__(self, key, val):
        self.create_or_change_secret(key, val, "")

    def __getitem__(self, key):
        try:
            secret_version_response = self.client.secrets.kv.v2.read_secret_version(path=key)
            return secret_version_response["data"]["data"]
        except:
            logger.error("VAULT secret not found: %s"%key)
            raise KeyError(key)

    def __delitem__(self, name):
        try:
            logger.debug("Removing VAULT secret: %s"%name)
            self.client.adapter.request("DELETE", "v1/secret/data/%s"%name)
        except KeyboardInterrupt:
            logger.error("Handled error happens during removal of VAULT secret: %s"%name)
            pass

    def keys(self):
        res = self.client.adapter.request("GET", "v1/secret/data?list=1")
        return res["data"]["keys"]
