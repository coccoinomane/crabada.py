from typing import cast
from eth_typing import Address

# Lower-case addresses of ERC20 token contracts
tokens: dict[str, dict[str, Address]] = {
    "Avalanche": {
        "TUS": cast(Address, "0xf693248f96fe03422fea95ac0afbbbc4a8fdd172"),
        "CRA": cast(Address, "0xa32608e873f9ddef944b24798db69d80bbb4d1ed"),
    },
    "SwimmerNetwork": {
        "WTUS": cast(Address, "0x9c765eee6eff9cf1337a1846c0d93370785f6c92"),
        "CRA": cast(Address, "0xc1a1f40d558a3e82c3981189f61ef21e17d6eb48"),
    },
}

# Lower-case externally owned addresses
eoas: dict[str, Address] = {
    "project": cast(Address, "0xb697fAC04e7c16f164ff64355D5dCd9247aC5434")
}
