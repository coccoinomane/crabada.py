from src.helpers.general import secondOrNone
from src.helpers.reinforce import looterCanReinforce, getLooterReinforcementStatus
from src.libs.CrabadaWeb2Client.CrabadaWeb2Client import CrabadaWeb2Client
from pprint import pprint
from sys import argv

# VARS
mineId = secondOrNone(argv)
client = CrabadaWeb2Client()

if not mineId:
    print("Provide a game ID")
    exit(1)

mine = client.getMine(mineId)

# TEST FUNCTIONS
def test() -> None:
    print(">>> MINE")
    pprint(mine)
    print(">>> LOOTER REINFORCEMENT STATUS")
    pprint(getLooterReinforcementStatus(mine))
    print(">>> LOOTER CAN REINFORCE")
    pprint(looterCanReinforce(mine))


# EXECUTE
test()
