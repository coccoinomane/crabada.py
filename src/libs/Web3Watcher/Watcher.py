from __future__ import annotations
from typing import cast, Union, Any, Callable, List
from logging import Logger

from src.libs.Web3Client.Web3Client import Web3Client
from web3.types import FilterParams, LogReceipt
from abc import ABC
import logging
import time
import asyncio
from web3.types import BlockParams


class Watcher(ABC):
    """
    Base class representing a blockchain watcher.

    1. Set a filter with either setFilter() or setFilterParams().
    2. Register as many callbacks as you wish with addHandler().
    3. Start the watcher with run().

    The filter will be used to sieve the blockchain for corresponding
    log entries; each time a log is found, it is passed to the handlers.
    The handlers are executed in the same order they are provided.

    Glossary: A log entry is an event submitted by a smart contract; for
    this reason, "log entry" will be used interchangeably with "event".

    Nota bene: Please use a websocket URI to run the watcher, otherwise
    you might run into errors (for example 'filter not found') or slow
    execution.

    Docs: https://web3py.readthedocs.io/en/stable/filters.html
    """

    # Settable
    logger: Logger = logging  # type: ignore
    filterParams: Union[FilterParams, BlockParams] = {}
    handlers: List[Callable[[LogReceipt], None]] = []
    notFoundHandlers: List[Callable[[], None]] = []

    # Derived
    filter: Any = None

    def __init__(self, client: Web3Client, doAsync: bool = False) -> None:
        self.client = client
        self.doAsync = doAsync
        pass

    def addHandler(self, handler: Callable[[LogReceipt], None]) -> Watcher:
        """
        Add a handler to the queue; all handlers will be executed when a log
        entry is found, in the order they were added.
        """
        self.handlers.append(handler)
        return self

    def addNotFoundHandler(self, notFoundHandler: Callable[[], None]) -> Watcher:
        """
        Add a handler to the 'not found' queue; all handlers will be executed
        when a log entry is NOT found, in the order they were added.
        """
        self.notFoundHandlers.append(notFoundHandler)
        return self

    def setFilterParams(self, params: Union[FilterParams, BlockParams]) -> Watcher:
        """
        Given valid filter parameters, create and set the filter to
        use to sieve the blockchain logs.
        """
        self.filterParams = params
        self.setFilter(self.client.w3.eth.filter(self.filterParams))
        return self

    def setFilter(self, filter: Any) -> Watcher:
        """
        Set the filter to use to sieve the blockchain logs.
        """
        self.filter: Any = filter
        return self

    def setLogger(self, logger: Logger) -> Watcher:
        self.logger = logger
        return self

    def loop(self, filter: Any, pollInterval: float) -> None:
        """
        Infinite loop where we look for new log entries and fire
        the handlers to process them
        """
        while True:
            newLogs = cast(List[LogReceipt], filter.get_new_entries())
            if not newLogs:
                self.logger.debug("Watcher: No new log entry found")
                self.handleNotFound()
            for logEntry in newLogs:
                self.logger.debug("Watcher: New log entry!")
                self.handleLogEntry(logEntry)
            time.sleep(pollInterval)

    async def asyncLoop(self, filter: Any, pollInterval: float) -> None:
        """
        Infinite loop where we look for new log entries and fire
        the handlers asynchronously to process them
        """
        while True:
            newLogs = cast(List[LogReceipt], filter.get_new_entries())
            if not newLogs:
                self.logger.debug("Watcher: No new log entry found")
                self.handleNotFound()
            for logEntry in newLogs:
                self.logger.debug("Watcher: New log entry!")
                self.handleLogEntry(logEntry)
            await asyncio.sleep(pollInterval)

    def handleLogEntry(self, logEntry: LogReceipt) -> None:
        """
        Given a log entry, run all handlers in the order they
        were added
        """
        for handler in self.handlers:
            handler(logEntry)

    def handleNotFound(self) -> None:
        """
        What to do in the event no log is found in the latest poll
        """
        for notFoundHandler in self.notFoundHandlers:
            notFoundHandler()

    def run(self, pollInterval: float) -> None:
        """
        Start watching for log entries
        """
        if self.doAsync:
            loop = asyncio.get_event_loop()
            try:
                loop.run_until_complete(
                    asyncio.gather(self.asyncLoop(self.filter, pollInterval))
                )
            finally:
                loop.close()
        else:
            self.loop(self.filter, pollInterval)
