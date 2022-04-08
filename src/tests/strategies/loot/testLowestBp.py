from src.common.config import users
from src.helpers.general import findInListOfDicts
from src.strategies.loot.LowestBp import LowestBp
from src.common.clients import makeCrabadaWeb2Client

# VARS
client = makeCrabadaWeb2Client()
userAddress = users[0]["address"]
teamId = users[0]["teams"][0]["id"]
teams = client.listTeams(userAddress)
team = findInListOfDicts(teams, "team_id", teamId)  # type: ignore

if not team:
    print("Error getting team with ID " + str(teamId))
    exit(1)

strategy: LowestBp = LowestBp(client).setParams(team)

# TEST FUNCTIONS
def test() -> None:

    print(">>> IS STRATEGY APPLICABLE?")
    print(strategy.isApplicable())

    print(">>> CHOSEN MINE")
    try:
        print(strategy.getMine())
    except Exception as e:
        print("ERROR RAISED: " + e.__class__.__name__ + ": " + str(e))


# EXECUTE
test()
