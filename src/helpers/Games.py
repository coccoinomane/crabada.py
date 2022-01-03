"""Helper functions to handle Crabada games"""

from src.common.logger import logger
from src.common.txLogger import txLogger
from src.helpers.Twilio import sendSms
from typing import Any
from time import time

from web3.types import BlockData
from src.common.clients import crabadaWeb2Client, crabadaWeb3Client
from eth_typing import Address

from src.common.types import CrabadaGame
from src.libs.CrabadaWeb3Client.CrabadaWeb3Client import CrabadaWeb3Client
from src.libs.Web3Client.Helpers.Debug import printTxInfo

def closeFinishedGames(userAddress: Address) -> int:
    """Close all open games whose end time is due; return
    the number of closed games. Tested only with mining
    games, not yet with looting games.

    TODO: implement paging"""
    openGames = crabadaWeb2Client.listMines({
        "limit": 200,
        "status": "open",
        "user_address": userAddress})
    
    finishedGames = [ g for g in openGames if gameIsFinished(g) ]
    
    if not finishedGames:
        logger.info('No games to close for user ' + str(userAddress))
        return 0
    
    for i, g in enumerate(finishedGames):
        gameId = g['game_id']
        logger.info(f'Closing game {gameId}...')
        txHash = crabadaWeb3Client.closeGame(gameId)
        txLogger.info(txHash)
        tx_receipt = crabadaWeb3Client.w3.eth.wait_for_transaction_receipt(txHash)
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
        tx_receipt = crabadaWeb3Client.w3.eth.wait_for_transaction_receipt(txHash)
        txLogger.debug(tx_receipt)
        logger.info(f'Team {teamId} sent')
        # TODO: log the game that was created
        if tx_receipt['status'] != 1:
            sendSms(f'Crabada: ERROR sending > {txHash}')
        else:
            sendSms(f'Crabada: Team sent > {txHash}')

    return i+1

def gameIsFinished(game: CrabadaGame) -> bool:
    """Return true if the given game is past its end_time"""
    return game['end_time'] <= time()

def gameIsClosed(game: CrabadaGame) -> bool:
    """Return true if the given game is closed (meaning the
    reward has been claimed"""
    crabadaWeb2Client.getMine(game['game_id'])
    return game['status'] == 'close'
