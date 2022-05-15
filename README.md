Scripts to interact with [Crabada](https://www.crabada.com)'s smart contracts 🦀

# 📣  Swimmer Network subnet

Crabada.py now works on the Swimmer Network subnet!

Make sure to follow our [migration tutorial](https://github.com/coccoinomane/crabada.py/discussions/104): it takes just a few minutes 🙂

# Features

- Completely automatic mining: start, reinforce & settle.
- Semi-automatic looting: reinforce and settle.
- Manage multiple teams at the same time.
- Telegram notifications.
- Self-reinforce from inventory

# Quick start

1. Make sure you have Python 3.9 or later installed.
2. Install dependencies: `pip install -r requirements.txt`.
3. Copy _.env.example_ in _.env_.
4. Configure _.env_. Crabada.py will only consider the teams you add there.
5. Run `python -m bin.mining.run <your address>` to automatically mine, reinforce and settle with all available teams. The command will keep running as long as your computer is turned on.

**IMPORTANT**: Do not run Crabada.py on a webserver! If you must do it, keep your _.env_ outside the public folder at all costs, otherwise your private key might be accessible via browser! For good measure, also restrict its permissions: `chmod 700 .env`.

# Documentation

- [💾 Install Python 3](https://github.com/coccoinomane/crabada.py/wiki/%F0%9F%92%BE--Install-Python-3)
- [🎮 Available commands](https://github.com/coccoinomane/crabada.py/wiki/%F0%9F%8E%AE-Available-commands)
- [🦀 Manage multiple teams](https://github.com/coccoinomane/crabada.py/wiki/%F0%9F%A6%80-Manage-multiple-teams)
- [📭 Telegram notifications](https://github.com/coccoinomane/crabada.py/wiki/%F0%9F%93%AD-Telegram-notifications)
- [💪 Reinforce strategies](https://github.com/coccoinomane/crabada.py/wiki/%F0%9F%92%AA-Reinforce-strategies)
- [🤖 Automate via cron job](https://github.com/coccoinomane/crabada.py/wiki/%F0%9F%A4%96-Automate-via-cron-job)
- [🐳 Run with docker](https://github.com/coccoinomane/crabada.py/wiki/%F0%9F%90%B3--Run-with-docker)
- [ℹ️ Common issues](https://github.com/coccoinomane/crabada.py/wiki/%E2%84%B9%EF%B8%8F-Common-issues)

# It doesn't work 😡

Don't panic! Instead...

1. Please check if your issue is listed in the [Common issues Wiki](https://github.com/coccoinomane/crabada.py/wiki/%E2%84%B9%EF%B8%8F-Common-issues).
2. If not, please search in the [Discussions section](https://github.com/coccoinomane/crabada.py/discussions/).
3. If even that does not help, consider [asking the community](https://github.com/coccoinomane/crabada.py/discussions/new) 🙂

# Donate ❤️

Building and maintaining Crabada.py requires time and passion: please consider expressing your gratitude by donating a small part of your rewards :-)

To donate, set the `DONATE_PERCENTAGE` parameter to a small value, for example `DONATE_PERCENTAGE=5%`; for more details, feel free to have a look in _.env.example_.