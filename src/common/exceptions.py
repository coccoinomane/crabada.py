
#################
# User
#################

class UserException(Exception):
    pass

#################
# Strategies
#################

class StrategyException(Exception):
    pass

class StrategyNotApplicable(StrategyException):
    pass

class CrabBorrowPriceTooHigh(StrategyException):
    pass

#################
# Config
#################

class ConfigException(Exception):
    pass

class MissingConfig(ConfigException):
    pass

class InvalidConfig(ConfigException):
    pass

