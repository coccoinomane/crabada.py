from typing import cast
from eth_typing import Address

# Lower-case addresses of ERC20 token contracts
tokens: dict[str, Address] = {
    "TUS": cast(Address, "0xf693248f96fe03422fea95ac0afbbbc4a8fdd172"),
    "CRA": cast(Address, "0xa32608e873f9ddef944b24798db69d80bbb4d1ed"),
}

# Lower-case externally owned addresses
eoas: dict[str, Address] = {
    "project": cast(Address, "0x5818a5f1ff6df3b7f5dad8ac66e100cce9e33e8e")
}
