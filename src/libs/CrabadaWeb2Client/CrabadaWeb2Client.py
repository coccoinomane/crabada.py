from typing import Any, List, Tuple
from eth_typing import Address
import requests
from src.helpers.general import firstOrNone, secondOrNone

from src.libs.CrabadaWeb2Client.types import CrabForLending, Game, Team


class CrabadaWeb2Client:
    """
    Access the HTTP endpoints of the Crabada P2E game.

    All endpoints have a 'raw' parameter that you can set to true
    in order to get the full JSON response. By default it is false,
    which means you only get the data contained in the response (a
    list for list endpoints, a dict for specific endpoints)
    """

    baseUri = "https://idle-api.crabada.com/public/idle"

    def getMine(self, mineId: int, params: dict[str, Any] = {}) -> Game:
        """Get information from the given mine"""
        res = self.getMine_Raw(mineId, params)
        return res["result"]

    def getMine_Raw(self, mineId: int, params: dict[str, Any] = {}) -> Any:
        url = self.baseUri + "/mine/" + str(mineId)
        return requests.request("GET", url, params=params).json()

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
        defaultParams = {
            "limit": 5,
            "page": 1,
        }
        actualParams = defaultParams | params
        return requests.request("GET", url, params=actualParams).json()

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
        defaultParams = {
            "limit": 5,
            "page": 1,
        }
        actualParams = defaultParams | params
        actualParams["user_address"] = userAddress
        return requests.request("GET", url, params=actualParams).json()

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
        defaultParams = {
            "limit": 10,
            "page": 1,
            "orderBy": "price",
            "order": "asc",
        }
        actualParams = defaultParams | params
        return requests.request("GET", url, params=actualParams).json()  # type: ignore

    def listCrabsForLendingFromInventory(
        self, user_address: Address, params: dict[str, Any] = {}
    ) -> List[CrabForLending]:
        """
        Get all crabs available for lending as reinforcements from users own inventory.
        """
        params["user_address"] = user_address
        res = self.listCrabsForLendingFromInventory_Raw(params)
        try:
            crabadas = res["result"]["data"] or []
            for cra in crabadas:
                # lending(tavern) and can-join-team(inventory) api has different fields for crabs.
                # add missing information for this endpoint.

                # price is important, it is required by the contract
                # and we may use it for ordering and stuff...
                cra["price"] = 0

                # others not so much...
                cra["lender"] = ""
                cra["is_being_borrowed"] = 0
                cra["borrower"] = ""
                cra["game_id"] = 0
            return crabadas
        except:
            return []

    def listCrabsForLendingFromInventory_Raw(self, params: dict[str, Any] = {}) -> Any:
        url = self.baseUri + "/crabadas/can-join-team"
        return requests.request("GET", url, params=params).json()  # type: ignore
