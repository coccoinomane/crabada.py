"""Helper functions to handle Crabada games"""

from src.common.logger import logger
from src.common.txLogger import txLogger
from src.helpers.General import firstOrNone
from src.helpers.Dates import getPrettySeconds
from src.helpers.Sms import sendSms
from typing import List
from time import time

from src.common.clients import crabadaWeb2Client, crabadaWeb3Client
from eth_typing import Address

from src.libs.CrabadaWeb2Client.types import Game

def getNextGameToFinish(games: List[Game]) -> Game:
    """Given a list of games, return the game that is open and
    next to finish; returns None if there are no unfinished games.
    
    If a game is already finished, it won't be considered"""
    unfinishedGames = [ g for g in games if not gameIsFinished(g) ]
    return firstOrNone(sorted(unfinishedGames, key=lambda g: g['end_time']))

def closeFinishedGames(userAddress: Address) -> int:
    """Close all open games whose end time is due; return
    the number of closed games. Tested only with mining
    games, not yet with looting games.

    TODO: implement paging"""
    
    # Get open games and the filter only those where
    # the reward has yet to be claimed
    openGames = crabadaWeb2Client.listMines({
        "limit": 200,
        "status": "open",
        "user_address": userAddress})
    finishedGames = [ g for g in openGames if gameIsFinished(g) ]
    
    # Print a useful message in case there aren't finished games 
    if not finishedGames:
        message = f'No games to close for user {str(userAddress)}'
        nextGameToFinish = getNextGameToFinish(openGames)
        if nextGameToFinish:
            message += f' (next in {getRemainingTimeFormatted(nextGameToFinish)})'
        logger.info(message)
        return 0

    # Close the finished games
    for i, g in enumerate(finishedGames):
        gameId = g['game_id']
        logger.info(f'Closing game {gameId}...')
        txHash = crabadaWeb3Client.closeGame(gameId)
        txLogger.info(txHash)
        tx_receipt = crabadaWeb3Client.getTransactionReceipt(txHash)
        logger.info(f'Game {gameId} closed')
        if tx_receipt['status'] != 1:
            sendSms(f'Crabada: ERROR closing > {txHash}')
    
    return i+1

def sendAvailableTeamsMining(userAddress: Address) -> int:
    """Send all available teams of crabs to mine; a game will be started
    for each available team; returns the number of games opened.

    TODO: implement paging"""
    availableTeams = crabadaWeb2Client.listTeams(userAddress, {
        "is_team_available": 1,
        "limit": 200,
        "page": 1})

    if not availableTeams:
        logger.info('No teams to send for user ' + str(userAddress))
        return 0

    for i, t in enumerate(availableTeams):
        teamId = t['team_id']
        logger.info(f'Sending team {teamId} to mine...')
        txHash = crabadaWeb3Client.startGame(teamId)
        txLogger.info(txHash)
        tx_receipt = crabadaWeb3Client.getTransactionReceipt(txHash)
        txLogger.debug(tx_receipt)
        logger.info(f'Team {teamId} sent')
        # TODO: log the game that was created
        if tx_receipt['status'] != 1:
            sendSms(f'Crabada: ERROR sending > {txHash}')
        else:
            sendSms(f'Crabada: Team sent > {txHash}')

    return i+1

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
