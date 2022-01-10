"""
Helper functions to send mining/looting all available teams
of a given user
"""

from web3.main import Web3
from src.common.exceptions import CrabBorrowPriceTooHigh
from src.common.logger import logger
from src.common.txLogger import txLogger, logTx
from src.helpers.Reinforce import minerCanReinforce
from src.helpers.Sms import sendSms
from typing import List, Literal

from src.common.clients import crabadaWeb2Client, crabadaWeb3Client
from eth_typing import Address
from src.helpers.Users import getUserConfig

from src.libs.CrabadaWeb2Client.types import Game
from src.strategies.reinforce.HighestBpStrategy import HighestBpStrategy
from src.strategies.reinforce.HighestMpStrategy import HighestMpStrategy
from src.strategies.loot.LowestBpStrategy import LowestBpStrategy

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
