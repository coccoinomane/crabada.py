from typing import Any, List
import requests
from src.libs.CrabadaWeb2Client.CrabadaWeb2Client import CrabadaWeb2Client
from src.libs.CrabadaWeb2Client.types.marketTypes import CrabForSale, SearchParameters


class MarketWeb2Client(CrabadaWeb2Client):
    """
    Access the HTTP endpoints of the Crabada marketplace
    """

    baseUri = "https://market-api.crabada.com/public/crabada"

    def listCrabsForSale_Raw(self, params: SearchParameters = {}) -> Any:
        url = self.baseUri + "/selling"
        defaultParams: dict[str, Any] = {"limit": 20, "page": 1}
        actualParams = defaultParams | params
        response = requests.get(
            url,
            headers=self.browserHeaders,
            params=actualParams,
        )
        return response.json()

    def listCrabsForSale(self, params: SearchParameters = {}) -> List[CrabForSale]:
        """
        Get crabs for sale.
        """
        res = self.listCrabsForSale_Raw(params)
        try:
            return res["result"]["data"] or []
        except:
            return []
