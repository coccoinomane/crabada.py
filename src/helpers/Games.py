"""Helper functions to handle Crabada games"""

from web3.main import Web3
from src.common.exceptions import CrabBorrowPriceTooHigh
from src.common.logger import logger
from src.common.txLogger import txLogger, logTx
from src.helpers.General import firstOrNone
from src.helpers.Dates import getPrettySeconds
from src.helpers.Reinforce import isTooExpensiveForUser, minerCanReinforce
from src.helpers.Sms import sendSms
from typing import List, Literal
from time import time

from src.common.clients import crabadaWeb2Client, crabadaWeb3Client
from eth_typing import Address
from src.helpers.Users import getUserConfig

from src.libs.CrabadaWeb2Client.types import Game
from src.strategies.reinforce.CheapestCrabStrategy import CheapestCrabStrategy
from src.strategies.reinforce.HighestBpStrategy import HighestBpStrategy
from src.strategies.reinforce.HighestMpStrategy import HighestMpStrategy
from src.strategies.loot.LowestBpStrategy import LowestBpStrategy

def getNextGameToFinish(games: List[Game]) -> Game:
    """Given a list of games, return the game that is open and
    next to finish; returns None if there are no unfinished games.
    
    If a game is already finished, it won't be considered"""
    unfinishedGames = [ g for g in games if not gameIsFinished(g) ]
    return firstOrNone(sorted(unfinishedGames, key=lambda g: g['end_time']))

def closeFinishedMines(userAddress: Address) -> int:
    """Close all open mining games whose end time is due; return
    the number of closed games.

    TODO: implement paging"""

    openGames = crabadaWeb2Client.listMines({
        "limit": 200,
        "status": "open",
        "user_address": userAddress})
    
    return _closeGivenGames(openGames, userAddress, 'mine')

def closeFinishedLoots(userAddress: Address) -> int:
    """Close all open looting games whose end time is due; return
    the number of closed games.

    TODO: implement paging"""

    openGames = crabadaWeb2Client.listMines({
        "limit": 200,
        "status": "open",
        "looter_address": userAddress})

    return _closeGivenGames(openGames, userAddress, gameType='loot')


def _closeGivenGames(games: List[Game], userAddress: Address, gameType: Literal['mine', 'loot']) -> int:
    """
    Helper function to close the given games
    """

    # Games with a reward to claim
    finishedGames = [ g for g in games if gameIsFinished(g) ]

    # Print a useful message in case there aren't finished games 
    if not finishedGames:
        message = f'No {gameType}s to close for user {str(userAddress)}'
        nextGameToFinish = getNextGameToFinish(games)
        if nextGameToFinish:
            message += f' (next in {getRemainingTimeFormatted(nextGameToFinish)})'
        logger.info(message)
        return 0

    nClosedGames = 0

    # Close the finished games
    for g in finishedGames:
        gameId = g['game_id']
        logger.info(f'Closing game {gameId}...')
        txHash = crabadaWeb3Client.closeGame(gameId)
        txLogger.info(txHash)
        txReceipt = crabadaWeb3Client.getTransactionReceipt(txHash)
        logTx(txReceipt)
        if txReceipt['status'] != 1:
            logger.error(f'Error closing game {gameId}')
            sendSms(f'Crabada: ERROR closing > {txHash}')
        else:
            nClosedGames += 1
            logger.info(f'Game {gameId} closed correctly')
    
    return nClosedGames

def sendAvailableTeamsMining(userAddress: Address) -> int:
    """Send all available teams of crabs to mine; a game will be started
    for each available team; returns the number of games opened.

    TODO: implement paging"""
    availableTeams = crabadaWeb2Client.listTeams(userAddress, {
        "is_team_available": 1,
        "limit": 200,
        "page": 1})

    if not availableTeams:
        logger.info('No available teams to send mining for user ' + str(userAddress))
        return 0

    # Send the teams
    nSentTeams = 0
    for t in availableTeams:
        teamId = t['team_id']
        logger.info(f'Sending team {teamId} to mine...')
        txHash = crabadaWeb3Client.startGame(teamId)
        txLogger.info(txHash)
        txReceipt = crabadaWeb3Client.getTransactionReceipt(txHash)
        logTx(txReceipt)
        # TODO: log the game that was created
        if txReceipt['status'] != 1:
            sendSms(f'Crabada: ERROR sending > {txHash}')
            logger.error(f'Error sending team {teamId}')
        else:
            nSentTeams += 1
            logger.info(f'Team {teamId} sent succesfully')

    return nSentTeams

def sendAvailableTeamsLooting(userAddress: Address) -> int:
    """Send all available teams of crabs to loot; a game will be started
    for each available team; returns the number of games opened.

    TODO: implement paging"""
    availableTeams = crabadaWeb2Client.listTeams(userAddress, {
        "is_team_available": 1,
        "limit": 200,
        "page": 1})

    if not availableTeams:
        logger.info('No available teams to send looting for user ' + str(userAddress))
        return 0

    # Send the teams
    nAttackedMines = 0
    for t in availableTeams:

        teamId = t['team_id']
        logger.info(f'Sending team {teamId} to loot...')

        # Find best mine to loot
        strategy: LowestBpStrategy = LowestBpStrategy(crabadaWeb2Client).setParams(team=t)
        mine = strategy.getMine()
        if not mine:
            logger.warning(f"Could not find a suitable mine to loot for team {teamId}")
            continue

        # Send the attack tx
        txHash = crabadaWeb3Client.attack(mine['game_id'], teamId)
        txLogger.info(txHash)
        txReceipt = crabadaWeb3Client.getTransactionReceipt(txHash)
        logTx(txReceipt)
        if txReceipt['status'] != 1:
            sendSms(f'Crabada: ERROR attacking > {txHash}')
            logger.error(f'Error attacking mine {str(mine["game_id"])} with team {teamId}')
        else:
            nAttackedMines += 1
            logger.info(f'Team {teamId} sent succesfully')

    return nAttackedMines

def reinforceWhereNeeded(userAddress: Address) -> int:
    """Check if any of the mining teams of the user can be
    reinforced, and do so if this is the case; return the
    number of borrowed reinforcements
    
    TODO: implement paging
    TODO: implement lending strategies other than cheapest crab"""
    
    user = getUserConfig(userAddress)
    openMines = crabadaWeb2Client.listMyOpenMines(userAddress)
    reinforceableMines = [ m for m in openMines if minerCanReinforce(m) ]
    if not reinforceableMines:
        logger.info('No mines to reinforce for user ' + str(userAddress))
        return 0

    # Reinforce the mines
    nBorrowedReinforments = 0
    for mine in reinforceableMines:

        mineId = mine['game_id']

        # Find best reinforcement crab to borrow
        maxPrice = getUserConfig(userAddress).get('maxPriceToReinforceInTus')

        # strategy: HighestMpStrategy = HighestMpStrategy(crabadaWeb2Client).setParams(mine, maxPrice)
        strategy: HighestBpStrategy = HighestBpStrategy(crabadaWeb2Client).setParams(mine, maxPrice)

        try:
            reinforcementCrab = strategy.getCrab()
        except CrabBorrowPriceTooHigh:
            logger.warning(f"Price of crab is {Web3.fromWei(price, 'ether')} TUS which exceeds the user limit of {user['maxPriceToReinforceInTus']}")
            continue
        if not reinforcementCrab:
            logger.warning(f"Could not find a crab to lend for mine {mineId}")
            continue
        crabId = reinforcementCrab['crabada_id']
        price = reinforcementCrab['price']
        logger.info(f"Borrowing crab {crabId} for mine {mineId} at {Web3.fromWei(price, 'ether')} TUS...")

        # Borrow the crab
        txHash = crabadaWeb3Client.reinforceDefense(mineId, crabId, price)
        txLogger.info(txHash)
        txReceipt = crabadaWeb3Client.getTransactionReceipt(txHash)
        logTx(txReceipt)
        if txReceipt['status'] != 1:
            sendSms(f'Crabada: ERROR reinforcing > {txHash}')
            logger.error(f'Error reinforcing mine {mineId}')
        else:
            nBorrowedReinforments += 1
            logger.info(f"Mine {mineId} reinforced correctly")
            
    return nBorrowedReinforments

def getRemainingTime(game: Game) -> int:
    """Seconds to the end of the given game"""
    return int(game['end_time'] - time())

def getRemainingTimeFormatted(game: Game) -> str:
    """Hours, minutes and seconds to the end of the given
    game"""
    return getPrettySeconds(getRemainingTime(game))

def gameIsFinished(game: Game) -> bool:
    """Return true if the given game is past its end_time"""
    return getRemainingTime(game) <= 0

def gameIsClosed(game: Game) -> bool:
    """Return true if the given game is closed (meaning the
    reward has been claimed"""
    crabadaWeb2Client.getMine(game['game_id'])
    return game['status'] == 'close'
