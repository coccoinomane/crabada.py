"""
Private key retirval
"""

import os
from src.helpers.aws import SecretsManager
from src.helpers.vault import VaultSecretsManager


def get_private_key(userPrefix: str) -> str:
    keyname = "%s_PRIVATE_KEY"%userPrefix
    if os.getenv("AWS_ACCESS_KEY_ID") and os.getenv("AWS_SECRET_ACCESS_KEY"):
        try:
            sm = SecretsManager()
            private_key = sm[keyname]
            private_key = private_key["SecretString"]
        except KeyError:
            private_key = os.getenv(keyname)
        finally:
            return private_key
    elif os.getenv("VAULT_TOKEN") and os.getenv("VAULT_URL"):
        try:
            vm = VaultSecretsManager()
            private_key = vm[keyname]
        except KeyError:
            private_key = os.getenv(keyname)
        finally:
            return private_key
    else:
        return os.getenv(keyname)
    return None
