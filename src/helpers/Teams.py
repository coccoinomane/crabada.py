from src.libs.CrabadaWeb2Client.types import Team

def teamCanLoot(team: Team) -> bool:
    """
    Return True if the given team is free to loot
    """
    return team['status'] == 'AVAILABLE'