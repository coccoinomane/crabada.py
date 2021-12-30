import requests

class Web2Client:
    """Access web endpoints of the game Crabada"""

    baseUri = 'https://idle-api.crabada.com/public/idle'

    def getMine(self, mineId: int, params: dict = {}):
        """Get information from the given mine"""
        url = self.baseUri + '/mine/' + str(mineId)
        return requests.request("GET", url, params=params)

    def getTeams(self, userAddress: str, params: dict = {}):
        """Get all teams of a given user address.
        
        If you want only the available teams, pass is_team_available=1
        in the params.
        """
        url = self.baseUri + '/teams'
        defaultParams = {
            "limit": 5,
            "page": 1,
        }
        actualParams = defaultParams | params
        actualParams['user_address'] = userAddress
        return requests.request("GET", url, params=actualParams)
