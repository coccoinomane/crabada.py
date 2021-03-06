from abc import ABC


class CrabadaWeb2Client(ABC):
    """
    Base class to access the HTTP endpoints of the Crabada P2E game.
    """

    baseUri: str
    """
    The base URL of the API
    """

    browserHeaders = {
        "authority": "idle-game-api.crabada.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://idle.crabada.com",
        "pragma": "no-cache",
        "referer": "https://idle.crabada.com/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    }

    def __init__(self, userAgent: str = None) -> None:
        super().__init__()
        if userAgent:
            self.browserHeaders["user-agent"] = userAgent
