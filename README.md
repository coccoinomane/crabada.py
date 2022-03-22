Scripts to interact with [Crabada](play.crabada.com)'s smart contracts 🦀

# Features

- Automatically send crabs mining.
- Automatically reinforce mines & loots.
- Automatically claim rewards for mines & loots.
- Choose between several reinforcement strategies.
- Run the bot without human supervision.
- Manage multiple teams at the same time.

# Quick start

1. Make sure you have Python 3.9 or later installed.
1. Install dependencies: `pip install -r requirements.txt`.
1. Copy _.env.example_ in _.env_ and customize the latter.
1. Make sure you `cd` in the root folder of the project (the same where this readme is)
1. Run any of the scripts in the _bin_ folder.

# Mining scripts

- Run `python -m bin.mining.sendTeamsMining <your address>` to send available teams mining.
- Run `python -m bin.mining.closeMines <your address>` to close and claim rewards on finished mines.
- Run `python -m bin.mining.reinforceDefense <your address>` to reinforce all open mines with a crab from the tavern, using the reinforcement strategy specified in the .env file.

# Looting scripts

- Run `python -m bin.looting.reinforceAttack <your address>` to reinforce all attacking teams with a crab from the tavern, using the reinforcement strategy specified in the .env file.
- Run `python -m bin.looting.closeLoots <your address>` to settle and claim rewards on loots that can be settled.

### What about attacking? 🤔

The bot can only help looters with automatic reinforcement & settling.

I have no plans to implement automatic looting/attacking [for the reasons outlined here](https://github.com/coccoinomane/crabada.py/issues/3#issuecomment-1073066318).

# Run without human supervision

In order to run the bot without human supervision, you'll need to set a cron job.

I would recommend to do it on a remote server, for example on Vultr, AWS or Google Cloud; if you can't be bothered, you can also do it on your computer: just make sure you keep the computer turned on all the time.

### Linux & Mac instructions

Follow these instructions to send all available teams mining & to collect rewards for you:

1. Find the path of Python 3 in your system by running `which python3` or `which python`.
2. Open crontab > `env EDITOR=nano crontab -e`
3. Insert the following lines:
    ```
    0,30 * * * * cd $HOME/crabada.py && /path/to/python3 -m bin.mining.sendTeamsMining <your address>
    15,45 * * * * cd $HOME/crabada.py && /path/to/python3 -m bin.mining.closeMines <your address>
    ```
3. Customize with the path to Python 3 (`/path/to/python3`), the path to the script folder (`$HOME/crabada.py`) and your wallet address (`<your address>`).
4. The cron job will run twice every 30 minutes. Feel free to change the frequency, if in doubt see [Crontab Guru](https://crontab.guru/).
5. If you want to reinforce defense too, just add another line to run `bin.mining.reinforceDefense`, for example:
   ```
   2,12,22,32,42,52 * * * * cd $HOME/crabada.py && python -m bin.mining.reinforceDefense <your address>
   ```


# Support for multiple teams

The bot can handle multiple teams, you just need to register their IDs in the .env file:

```bash
USER_1_TEAM_1="1111"
USER_1_TEAM_2="2222"
USER_1_TEAM_3="3333"
```

Then, you can run any of the scripts described above and they will apply to all of the registered teams.

# System requirements

The bot requires Python 3.9; I have personally tested it on:

- **Mac Os 11 (Big Sur)** > Install python3 and pip3 with [Homebrew](https://brew.sh/) > `brew install python3`
- **Debian GNU/Linux 11 (bullseye)** > Install python3 and pip with apt-get > `apt-get install python3 pip git`

Users told me that they managed to run the bot on Ubuntu, too.

# To do

* Avoid losing gas on failed reinforce
* Fix `closeLoots`
* Use a virtual environment to manage dependencies
* Multi-user support: send teams from multiple wallets

# Might do

* Looting reinforcement: Implement faction advantage
* Use cron library to schedule scripts
* Gas control: Stop if wallet has less than X ETH + set daily gas limit
* Better gas estimation ([eth_baseFee and eth_maxPriorityFeePerGas](https://docs.avax.network/learn/platform-overview/transaction-fees/))
* Use web3 default variable WEB3_PROVIDER_URI instead of WEB3_NODE_URI
* Use @property to define classattributes > https://realpython.com/python-property/
