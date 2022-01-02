from typing import Literal, TypedDict, List
from eth_typing import Address

class ConfigTeam(TypedDict):
    id: int
    userAddress: Address

class ConfigUser(TypedDict):
    name: str
    address: Address
    privateKey: str
    teams: List[ConfigTeam]

class ConfigContract(TypedDict):
    address: Address
    abi: str

class CrabadaGameProcess(TypedDict):
    action: Literal['create-game', 'attack', 'reinforce-defence', 'reinforce-attack', 'settle']
    transaction_time: int

class CrabadaGame(TypedDict):
    game_id: int
    winner_team_id: int
    status: Literal['open', 'close']
    # Defense
    team_id: int
    owner: Address
    defense_crabada_number: Literal[3,4,5]
    defense_point: int
    defense_mine_point: int
    # Attack
    attack_team_id: int
    attack_team_owner: Address
    attack_crabada_number: Literal[3,4,5]
    attack_point: int
    attack_mine_point: int
    # Rewards
    tus_reward: int
    cra_reward: int
    estimate_looter_lose_cra: int
    estimate_looter_lose_tus: int
    estimate_looter_win_cra: int
    estimate_looter_win_tus: int
    estimate_miner_lose_cra: int
    estimate_miner_lose_tus: int
    estimate_miner_win_cra: int
    estimate_miner_win_tus: int
    # Time
    start_time: int
    end_time: int
    round: Literal[0,1,2,3,4]
    process: List[CrabadaGameProcess]

class CrabadaTeam(TypedDict):
    battle_point: int
    crabada_1_armor: int
    crabada_1_class: int
    crabada_1_critical: int
    crabada_1_damage: int
    crabada_1_hp: int
    crabada_1_is_genesis: Literal[0,1]
    crabada_1_is_origin: Literal[0,1]
    crabada_1_legend_number: int
    crabada_1_photo: str
    crabada_1_speed: int
    crabada_1_type: int
    crabada_2_armor: int
    crabada_2_class: int
    crabada_2_critical: int
    crabada_2_damage: int
    crabada_2_hp: int
    crabada_2_is_genesis: Literal[0,1]
    crabada_2_is_origin: Literal[0,1]
    crabada_2_legend_number: int
    crabada_2_photo: str
    crabada_2_speed: int
    crabada_2_type: int
    crabada_3_armor: int
    crabada_3_class: int
    crabada_3_critical: int
    crabada_3_damage: int
    crabada_3_hp: int
    crabada_3_is_genesis: Literal[0,1]
    crabada_3_is_origin: Literal[0,1]
    crabada_3_legend_number: int
    crabada_3_photo: str
    crabada_3_speed: int
    crabada_3_type: int
    crabada_id_1: int
    crabada_id_2: int
    crabada_id_3: int
    game_end_time: int
    game_id: int
    game_round: Literal[0,1,2,3,4]
    game_start_time: int
    # Should we add 'looting' as a game_type?
    game_type: Literal['mining']
    mine_end_time: int
    mine_point: int
    mine_start_time: int
    owner: Address
    process_status: Literal['create-game', 'attack', 'reinforce-defence', 'reinforce-attack', 'settle']
    # Not sure LOOTING is an actual status...
    status: Literal['MINING', 'LOOTING']
    team_id: int
    time_point: int
