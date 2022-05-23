from typing import Literal, TypedDict, List
from eth_typing import Address
from web3.types import Wei

"""
Possible states for a team
"""
TeamStatus = Literal["MINING", "LOOTING", "AVAILABLE"]


class GameProcess(TypedDict):
    action: Literal[
        "create-game",
        "attack",
        "reinforce-defense",
        "reinforce-attack",
        "settle",
        "close-game",
    ]
    transaction_time: int


class TeamMember(TypedDict):
    """
    Synthetic info about a team member as returned by mine endpoints
    """

    crabada_id: int
    photo: str
    hp: int
    speed: int
    armor: int
    damage: int
    critical: int


class Game(TypedDict):
    game_id: int
    winner_team_id: int
    status: Literal["open", "close"]
    # Defense
    team_id: int
    owner: Address
    defense_crabada_number: Literal[3, 4, 5]
    defense_point: int
    defense_mine_point: int
    # Attack
    attack_team_id: int
    attack_team_owner: Address
    attack_crabada_number: Literal[3, 4, 5]
    attack_point: int
    attack_mine_point: int
    # Rewards
    tus_reward: Wei
    cra_reward: Wei
    estimate_looter_lose_cra: Wei
    estimate_looter_lose_tus: Wei
    estimate_looter_win_cra: Wei
    estimate_looter_win_tus: Wei
    estimate_miner_lose_cra: Wei
    estimate_miner_lose_tus: Wei
    estimate_miner_win_cra: Wei
    estimate_miner_win_tus: Wei
    miner_cra_reward: Wei
    miner_tus_reward: Wei
    looter_cra_reward: Wei
    looter_tus_reward: Wei
    # Time
    start_time: int
    end_time: int
    round: Literal[0, 1, 2, 3, 4]
    process: List[GameProcess]
    attack_team_info: List[TeamMember]
    defense_team_info: List[TeamMember]


class Team(TypedDict):
    team_id: int
    battle_point: int
    crabada_1_armor: int
    crabada_1_class: int
    crabada_1_critical: int
    crabada_1_damage: int
    crabada_1_hp: int
    crabada_1_is_genesis: Literal[0, 1]
    crabada_1_is_origin: Literal[0, 1]
    crabada_1_legend_number: int
    crabada_1_photo: str
    crabada_1_speed: int
    crabada_1_type: int
    crabada_2_armor: int
    crabada_2_class: int
    crabada_2_critical: int
    crabada_2_damage: int
    crabada_2_hp: int
    crabada_2_is_genesis: Literal[0, 1]
    crabada_2_is_origin: Literal[0, 1]
    crabada_2_legend_number: int
    crabada_2_photo: str
    crabada_2_speed: int
    crabada_2_type: int
    crabada_3_armor: int
    crabada_3_class: int
    crabada_3_critical: int
    crabada_3_damage: int
    crabada_3_hp: int
    crabada_3_is_genesis: Literal[0, 1]
    crabada_3_is_origin: Literal[0, 1]
    crabada_3_legend_number: int
    crabada_3_photo: str
    crabada_3_speed: int
    crabada_3_type: int
    crabada_id_1: int
    crabada_id_2: int
    crabada_id_3: int
    game_end_time: int
    game_id: int
    game_round: Literal[0, 1, 2, 3, 4]
    game_start_time: int
    # Should we add 'looting' as a game_type?
    game_type: Literal["mining"]
    mine_end_time: int
    mine_point: int
    mine_start_time: int
    owner: Address
    process_status: Literal[
        "create-game", "attack", "reinforce-defence", "reinforce-attack", "settle"
    ]
    # Not sure LOOTING is an actual status...
    status: TeamStatus
    time_point: int


class CrabForLending(TypedDict):
    crabada_id: int
    id: int  # it seems to be the same as crabada_id...
    price: Wei  # IMPORTANT: this is expressed as the TUS price multiplied by 10^18 (like Wei), which means that a value of 100000000000000000 is 1 TUS
    crabada_name: str
    lender: Address
    is_being_borrowed: Literal[0, 1]
    borrower: Address
    game_id: int
    crabada_type: int
    crabada_class: int
    class_id: int
    class_name: str
    is_origin: Literal[0, 1]
    is_genesis: Literal[0, 1]
    legend_number: int
    pure_number: int
    photo: str
    hp: int
    speed: int
    damage: int
    critical: int
    armor: int
    battle_point: int
    time_point: int
    mine_point: int


class CrabFromInventory(TypedDict):
    crabada_id: int
    id: int  # it seems to be the same as crabada_id...
    crabada_name: str
    owner: str
    crabada_type: int
    crabada_class: int
    class_id: int
    class_name: str
    is_origin: Literal[0, 1]
    is_genesis: Literal[0, 1]
    legend_number: int
    pure_number: int
    photo: str
    hp: int
    speed: int
    damage: int
    critical: int
    armor: int
    battle_point: int
    time_point: int
    mine_point: int
