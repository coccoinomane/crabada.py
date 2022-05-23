from typing import Literal, TypedDict, List
from eth_typing import Address
from web3.types import Wei
import enum


class CrabClasses(enum.Enum):
    SURGE = 1
    SUNKEN = 2
    PRIME = 3
    BULK = 4
    CRABOID = 5
    RUINED = 6
    GEM = 7
    ORGANIC = 8


class CrabForSale(TypedDict):
    armor: int
    atlas_photo: str
    birthday: int
    body_class: int
    body_id: int
    body_name: str
    body_photo: str
    breed_count: int
    class_id: int
    class_name: str
    cnt: str
    crabada_class: int
    crabada_id: int
    crabada_subclass: int
    crabada_type: int
    created_at: str
    creator: Address
    critical: int
    damage: int
    description: str
    dna: str
    eyes_class: int
    eyes_id: int
    eyes_name: str
    eyes_photo: str
    horn_class: int
    horn_id: int
    horn_name: str
    horn_photo: str
    hp: int
    id: int
    is_genesis: Literal[0, 1]
    is_origin: Literal[0, 1]
    legend_number: int
    mouth_class: int
    mouth_id: int
    mouth_name: str
    mouth_photo: str
    name: str
    order_id: int
    order_time: str
    owner: Address
    owner_full_name: str
    owner_nft_avatar: str
    owner_photo: str
    photo: str
    pincers_class: int
    pincers_id: int
    pincers_name: str
    pincers_photo: str
    price: float
    pure_number: int
    shell_class: int
    shell_id: int
    shell_name: str
    shell_photo: str
    speed: int
    stage: int
    type: str
    updated_at: str


SearchParameters = TypedDict(
    "SearchParameters",
    {
        # Pagination
        "limit": int,
        "page": int,
        # Ordering
        "order": Literal["asc", "desc"],
        "orderBy": Literal["price", "order_time"],
        # Price
        "from_price": Wei,  # in TUS
        "to_price": Wei,  # in TUS
        # Type filters
        "class_ids[]": List[int],  # use CrabClasses enum to translate from names to ids
        "is_origin": Literal[0, 1],
        "type": int,  # 2 is genesis
        "stage": Literal[0, 1],
        "from_breed_count": Literal[0, 1, 2, 3, 4, 5],
        "to_breed_count": Literal[0, 1, 2, 3, 4, 5],
        "from_pure": Literal[0, 1, 2, 3, 4, 5, 6],
        "to_pure": Literal[0, 1, 2, 3, 4, 5, 6],
        "from_legend": Literal[0, 1, 2, 3, 4, 5, 6],
        "to_legend": Literal[0, 1, 2, 3, 4, 5, 6],
        # Battle game filters
        "from_speed": int,
        "to_speed": int,
        "from_damage": int,
        "to_damage": int,
        "from_armor": int,
        "to_armor": int,
        "from_hp": int,
        "to_hp": int,
        "from_critical": int,
        "to_critical": int,
        # Idle game filters
        "from_battle_point": int,
        "to_battle_point": int,
        "from_mine_point": int,
        "to_mine_point": int,
    },
    total=False,
)
