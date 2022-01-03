Scripts to interact with [Crabada](play.crabada.com)'s smart contracts.

# Quick start

1. Copy .env.local in .env and customize .env
2. Run one of the scripts in the script folder, for example `python3 -m scripts.example` to run example.py.

# Contracts

- [Crabada: Game](https://snowtrace.io/address/0x82a85407bd612f52577909f4a58bfc6873f14da8) > [Decompiled](https://snowtrace.io/bytecode-decompiler?a=0x82a85407bd612f52577909f4a58bfc6873f14da8)

# Crabada.com Endpoints

The Crabada API has REST endpoints with base uri https://idle-api.crabada.com/public/idle/.

For a list of endpoints, see the [Postman collection](https://go.postman.co/workspace/Crypto~19d2a5ae-faa1-4999-af6e-e1c4c8428a7e/collection/18622998-191ed6a2-1026-4ae2-8fbd-a9f5b233bc9c).

# Response examples

- [Start mining expedition tx](https://snowtrace.io/tx/0x46594658e0f65181d65bd6c229837d9fff962a0480e13d21f542733c0c1dbbb6)
- [First reinforcement tx](https://snowtrace.io/tx/0x1d8e002f497b925fba9f76b8909fa87d59a45d99e7e8ca9a1e0f6119b23da4b7)
- [Second reinforcemente tx](https://snowtrace.io/tx/0xe1cd5862278930acb1bf861ecba18fbb63e5696cb5779c3bcc590f8a397ad3b3)
- [Claim tx](https://snowtrace.io/tx/0x55a75966158e03c22058ac24dbe855ee7aa2437d719c61b54cf14c4a906d9631)
- [Claim tx](https://snowtrace.io/tx/0x65d7d2783f7817f3302cee3b5f1ca0dd3bb7ace19b172770df00800a51403124) (different sequence)

# To do

* Write startGame script
* Write closeGame script
* Use cron library to schedule scripts
* Write reinforcement script
* Stop if wallet has less than X ETH
* In AVAX should we be using eth_baseFee and eth_maxPriorityFeePerGas? (https://docs.avax.network/learn/platform-overview/transaction-fees/)

# Done

* Reasonable defaults for gasLimit and maxPriorityFeePerGas for Avalanche
* Make it work for different chains than AVAX (gas limit, poa middleware...)
* Use EIP-1559 gas
* Embed gas estimation in client (without need to use parameters)