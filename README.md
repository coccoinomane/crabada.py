Scripts to interact with [Crabada](play.crabada.com)'s smart contracts.

# Quick start

1. Copy .env.local in .env and customize .env
2. Make sure you `cd` in the root folder of the project (the same where this readme is)
3. Run one of the scripts in the script folder, for example `python3 -m bin.sendTeams` to run sendTeams.py

# Contracts

- [Crabada: Game](https://snowtrace.io/address/0x82a85407bd612f52577909f4a58bfc6873f14da8) > [Decompiled](https://snowtrace.io/bytecode-decompiler?a=0x82a85407bd612f52577909f4a58bfc6873f14da8)

# Crabada.com Endpoints

The Crabada API has REST endpoints with base uri https://idle-api.crabada.com/public/idle/.

For a list of endpoints, see the [Postman collection](https://go.postman.co/workspace/Crypto~19d2a5ae-faa1-4999-af6e-e1c4c8428a7e/collection/18622998-191ed6a2-1026-4ae2-8fbd-a9f5b233bc9c).

# Response examples

### Mining

- [Start mining expedition tx](https://snowtrace.io/tx/0x46594658e0f65181d65bd6c229837d9fff962a0480e13d21f542733c0c1dbbb6)
- [First reinforcement tx](https://snowtrace.io/tx/0x1d8e002f497b925fba9f76b8909fa87d59a45d99e7e8ca9a1e0f6119b23da4b7)
- [Second reinforcemente tx](https://snowtrace.io/tx/0xe1cd5862278930acb1bf861ecba18fbb63e5696cb5779c3bcc590f8a397ad3b3)
- [Claim tx](https://snowtrace.io/tx/0x55a75966158e03c22058ac24dbe855ee7aa2437d719c61b54cf14c4a906d9631)
- [Claim tx](https://snowtrace.io/tx/0x65d7d2783f7817f3302cee3b5f1ca0dd3bb7ace19b172770df00800a51403124) (different sequence)

### Looting

- [Attack tx](https://snowtrace.io/tx/0x21a7f94f6e02103b55d9b9fa53243ae1ac0eab8531f5588cfc4a0e6ace126902)
- [Settle tx](https://snowtrace.io/tx/0xb6853b50dd85e59062964a060e796ffcd13e3d72711e0789127f2f3d81f523d1)

# Events

### startGame

- Method > 0xe5ed1d59
- Example transaction > [0x41705baf18b1ebc8ec204926a8524d3530aada11bd3c249ca4a330ed047f005e](https://snowtrace.io/tx/0x41705baf18b1ebc8ec204926a8524d3530aada11bd3c249ca4a330ed047f005e) (click on "Logs")
- Topics:
 0. 0x0eef6f7452b7d2ee11184579c086fb47626e796a83df2b2e16254df60ab761eb
 1. Mine number, e.g. 605198
 2. Team number, e.g. 4476
 3. Game duration in seconds, e.g. 14400 is 4 hours
 4. CRA reward for miner win, in Wei, e.g. 4125000000000000000 is 4.125 CRA (with prime)
 5. TUS reward for miner win, in Wei, e.g. 334125000000000000000 is 334.125 TUS (with prime)

# To do

* Use cron library to schedule scripts
* Validate config values from .env
* Gas control: Stop if wallet has less than X ETH + set daily gas limit
* In AVAX should we be using eth_baseFee and eth_maxPriorityFeePerGas? (https://docs.avax.network/learn/platform-overview/transaction-fees/)
* Why use our own env variable for node uri (WEB3_NODE_URI) when web3 has a builtin one (WEB3_PROVIDER_URI)?

# Done

* Web3Client: Allow to specify contract and ABI ovverriding props
* In Python all class attributes are static > should declare them in the constructor? Even better: declare them only in docstring
* Implement a team's task parameter; more in general: how to run cron job for mining vs for looting?
* Find a way to differentiate/manage mines & loots
* Write reinforcement script
* Write startGame script
* Write closeGame script
* Reasonable defaults for gasLimit and maxPriorityFeePerGas for Avalanche
* Make it work for different chains than AVAX (gas limit, poa middleware...)
* Use EIP-1559 gas
* Embed gas estimation in client (without need to use parameters)