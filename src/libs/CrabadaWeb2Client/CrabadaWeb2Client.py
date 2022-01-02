
from typing import Any
from eth_typing import Address
import requests
from requests.models import Response

class CrabadaWeb2Client:
    """Access the HTTP endpoints of the Crabada P2E game"""

    baseUri = 'https://idle-api.crabada.com/public/idle'

    def getMine(self, mineId: int, params: dict[str, Any] = {}) -> Response:
        """Get information from the given mine"""
        url = self.baseUri + '/mine/' + str(mineId)
        return requests.request("GET", url, params=params)

    def listMines(self, params: dict[str, Any] = {}) -> Response:
        """Get all mines.
        
        If you want only the open mines, pass status=open in the params.
        If you want only a certain user's mines, use the user_address param.
        """
        url = self.baseUri + '/mines'
        defaultParams = {
            "limit": 5,
            "page": 1,
        }
        actualParams = defaultParams | params
        return requests.request("GET", url, params=actualParams)

    def listTeams(self, userAddress: Address, params: dict[str, Any] = {}) -> Response:
        """Get all teams of a given user address.
        
        If you want only the available teams, pass is_team_available=1
        in the params.
        It is currently not possible to list all users' teams, you can
        only see the teams of a specific user.
        """
        url = self.baseUri + '/mines'
        defaultParams = {
            "limit": 5,
            "page": 1,
        }
        actualParams = defaultParams | params
        actualParams['user_address'] = userAddress
        return requests.request("GET", url, params=actualParams)
