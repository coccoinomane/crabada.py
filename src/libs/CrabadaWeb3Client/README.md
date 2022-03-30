The idle game contract can be found at the following link:

- [Crabada: Game](https://snowtrace.io/address/0x82a85407bd612f52577909f4a58bfc6873f14da8) > [Decompiled](https://snowtrace.io/bytecode-decompiler?a=0x82a85407bd612f52577909f4a58bfc6873f14da8)

# Mining transactions

- [Start mining expedition tx](https://snowtrace.io/tx/0x46594658e0f65181d65bd6c229837d9fff962a0480e13d21f542733c0c1dbbb6)
- [First reinforcement tx](https://snowtrace.io/tx/0x1d8e002f497b925fba9f76b8909fa87d59a45d99e7e8ca9a1e0f6119b23da4b7)
- [Second reinforcemente tx](https://snowtrace.io/tx/0xe1cd5862278930acb1bf861ecba18fbb63e5696cb5779c3bcc590f8a397ad3b3)
- [Claim tx](https://snowtrace.io/tx/0x55a75966158e03c22058ac24dbe855ee7aa2437d719c61b54cf14c4a906d9631)
- [Claim tx](https://snowtrace.io/tx/0x65d7d2783f7817f3302cee3b5f1ca0dd3bb7ace19b172770df00800a51403124) (different sequence)

# Looting transactions

This client does not support attacking mines since March 2022, due to the anti-bot patch released by the Crabada team. For more details on this chouce, see https://github.com/coccoinomane/crabada.py/issues/3#issuecomment-1073066318.

- [Attack tx](https://snowtrace.io/tx/0x071646483181b2a14874bd10e978ca7c0124b00c793c8d550b2b3074a452b503)
- [Attack tx (before the anti-loot patch of March 2022)](https://snowtrace.io/tx/0x21a7f94f6e02103b55d9b9fa53243ae1ac0eab8531f5588cfc4a0e6ace126902)
- [Settle tx](https://snowtrace.io/tx/0xb6853b50dd85e59062964a060e796ffcd13e3d72711e0789127f2f3d81f523d1)
- [startGame](https://snowtrace.io/tx/0x429bf6ad1fadf7666bb32e004572b2cd7e95f88fc6aeac2fd6052d338f663fc7) attacked [after 2 blocks](https://snowtrace.io/tx/0xa416719950157ebb7e2fc7078cd1ae3a98232c9229fc4f27ef678b38a3618205); look [how many tried to attack](https://snowtrace.io/txs?block=10345304) it without success!
- [startGame](https://snowtrace.io/tx/0x1ea87957255498b626423f578b8ca01e950deca53c7ada96b94c55012aa0c307) attacked [after 1 block](https://snowtrace.io/tx/0x47766dce7c005f796d6f6272a4a3365ac473eb8d7f8a39d2ec195ddc9f2e56e8).
- [startGame](https://snowtrace.io/tx/0xb1cac8f04de6f432858ddabb687f23c221cc5ed34b80639b54f54807afb3a793) attacked [after 2 blocks](https://snowtrace.io/tx/0x9363a133c736b06233688425978e8d7fd8b09f02a6b92129c3ee72f07e08ebbf).

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
