from typing import Any, List
from eth_typing import Address
import requests
from src.helpers.general import firstOrNone, secondOrNone
from web3.types import Wei
from src.libs.CrabadaWeb2Client.CrabadaWeb2Client import CrabadaWeb2Client

from src.libs.CrabadaWeb2Client.types.idleGameTypes import (
    CrabForLending,
    Game,
    Team,
    CrabFromInventory,
)


class IdleGameWeb2Client(CrabadaWeb2Client):
    """
    Access the HTTP endpoints of the Crabada Idle game.
    """

    baseUri = "https://idle-game-api.crabada.com/public/idle"

    def getMine(self, mineId: int, params: dict[str, Any] = {}) -> Game:
        """Get information from the given mine"""
        res = self.getMine_Raw(mineId, params)
        return res["result"]

    def getMine_Raw(self, mineId: int, params: dict[str, Any] = {}) -> Any:
        url = self.baseUri + "/mine/" + str(mineId)
        return requests.get(url, headers=self.browserHeaders, params=params).json()

    def listMines(self, params: dict[str, Any] = {}) -> List[Game]:
        """
        Get all mines.

        If you want only the open mines, pass status=open in the params.
        If you want only a certain user's mines, use the user_address param.
        """
        res = self.listMines_Raw(params)
        try:
            return res["result"]["data"] or []
        except:
            return []

    def listOpenMines(self, params: dict[str, Any] = {}) -> List[Game]:
        """
        Get open mines
        """
        params["status"] = "open"
        return self.listMines(params)

    def listLootableMines(
        self, looterAddress: Address, params: dict[str, Any] = {}
    ) -> List[Game]:
        """
        Get mines that are lootable; it is required to provide a user
        address.
        """
        params["can_loot"] = 1
        params["looter_address"] = looterAddress
        params["status"] = "open"
        return self.listMines(params)

    def listMyOpenMines(
        self, userAddress: Address, params: dict[str, Any] = {}
    ) -> List[Game]:
        """
        Get all mines that belong to the given user address
        and that are open
        """
        params["user_address"] = userAddress
        params["status"] = "open"
        return self.listMines(params)

    def listMyOpenLoots(
        self, looterAddress: Address, params: dict[str, Any] = {}
    ) -> List[Game]:
        """
        Get all mines that are being looted by the given looter address
        and that are open
        """
        params.pop("user_address", None)
        params["looter_address"] = looterAddress
        params["status"] = "open"
        return self.listMines(params)

    def listMines_Raw(self, params: dict[str, Any] = {}) -> Any:
        url = self.baseUri + "/mines"
        defaultParams: dict[str, Any] = {"limit": 5, "page": 1}
        actualParams = defaultParams | params
        response = requests.get(
            url,
            headers=self.browserHeaders,
            params=actualParams,
        )
        return response.json()

    def getTeam(self) -> None:
        raise Exception("The team route does not exit on the server!")

    def listTeams(
        self, userAddress: Address, params: dict[str, Any] = {}
    ) -> List[Team]:
        """
        Get all teams of a given user address.

        If you want only the available teams, pass is_team_available=1
        in the params.
        It is currently not possible to list all users' teams, you can
        only see the teams of a specific user.
        """
        res = self.listTeams_Raw(userAddress, params)
        try:
            return res["result"]["data"] or []
        except:
            return []

    def listAvailableTeams(
        self, userAddress: Address, params: dict[str, Any] = {}
    ) -> List[Team]:
        """
        Get all available teams of a given user address.
        """
        actualParams = params | {"is_team_available": 1}
        return self.listTeams(userAddress, actualParams)

    def listTeams_Raw(self, userAddress: Address, params: dict[str, Any] = {}) -> Any:
        url = self.baseUri + "/teams"
        defaultParams: dict[str, Any] = {
            "limit": 5,
            "page": 1,
        }
        actualParams = defaultParams | params
        actualParams["user_address"] = userAddress
        return requests.get(
            url, headers=self.browserHeaders, params=actualParams
        ).json()

    def listCrabsForLending(self, params: dict[str, Any] = {}) -> List[CrabForLending]:
        """
        Get all crabs available for lending as reinforcements; you can use
        sortBy and sort parameters, default is orderBy": 'price' and
        "order": 'asc'

        IMPORTANT: The price is expressed as the TUS price multiplied by
        10^18 (like with Weis), which means that price=100000000000000000
        (18 zeros) is just 1 TUS
        """
        res = self.listCrabsForLending_Raw(params)
        try:
            return res["result"]["data"] or []
        except:
            return []

    def getCheapestCrabForLending(self, params: dict[str, Any] = {}) -> CrabForLending:
        """
        Return the cheapest crab on the market available for lending,
        or None if no crab is found
        """
        params["limit"] = 1
        params["orderBy"] = "price"
        params["order"] = "asc"
        return firstOrNone(self.listCrabsForLending(params))

    def getSecondCheapestCrabForLending(
        self, params: dict[str, Any] = {}
    ) -> CrabForLending:
        """
        Return the second cheapest crab on the market available for lending,
        or None if no crab is found
        """
        params["limit"] = 2
        params["orderBy"] = "price"
        params["order"] = "asc"
        return secondOrNone(self.listCrabsForLending(params))

    def listCrabsForLending_Raw(self, params: dict[str, Any] = {}) -> Any:
        url = self.baseUri + "/crabadas/lending"
        defaultParams: dict[str, Any] = {
            "limit": 10,
            "page": 1,
            "orderBy": "price",
            "order": "asc",
        }
        actualParams = defaultParams | params
        return requests.get(
            url, headers=self.browserHeaders, params=actualParams
        ).json()

    def listCrabsFromInventory(
        self, userAddress: Address, params: dict[str, Any] = {}
    ) -> List[CrabFromInventory]:
        """
        Get all crabs available as reinforcements from the user's
        own inventory.
        """
        res = self.listCrabsFromInventory_Raw(userAddress, params)
        try:
            return res["result"]["data"] or []
        except:
            return []

    def listCrabsFromInventory_Raw(
        self, userAddress: Address, params: dict[str, Any] = {}
    ) -> Any:
        url = self.baseUri + "/crabadas/can-join-team"
        params["user_address"] = userAddress
        return requests.get(url, headers=self.browserHeaders, params=params).json()
