# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymcfunction', 'pymcfunction.commands']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.2,<0.11.0', 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['pmf = pymcfunction.cli.app:run',
                     'pyfunction = pymcfunction.cli.app:run',
                     'pymcfunction = pymcfunction.cli.app:run']}

setup_kwargs = {
    'name': 'pymcfunction',
    'version': '0.1.1',
    'description': 'PyMCFunction is a tool to write Minecraft datapacks in Python.',
    'long_description': '# PyFunction\n\nPyMCFunction is a tool to write Minecraft datapacks in Python.\n\n## Usage\n\nCheck pymcfunction/pyfunction/pmf --help\n\n## Docs\n\nHopefully coming soon, for now, ask somthing like IntelliSense.\n\n## Command support\n\nThese are the currently supported commands. Feel free to create a PR, the goal is to support every command.\n\n - [ ] /advancement\n - [ ] /attribute\n - [ ] /ban\n - [ ] /ban-ip\n - [ ] /banlist\n - [ ] /bossbar\n - [x] /clear\n - [ ] /clone\n - [ ] /data\n - [ ] /datapack\n - [ ] /debug\n - [x] /defaultgamemode\n - [x] /deop\n - [ ] /difficultiy\n - [ ] /effect\n - [ ] /enchant\n - [x] /execute\n - [ ] /experience (/xp)\n - [ ] /fill\n - [ ] /forceload\n - [x] /function\n - [ ] /gamemode\n - [ ] /gamerule\n - [ ] /give\n - [ ] /item\n - [ ] /kick\n - [ ] /kill\n - [ ] /locate\n - [ ] /loot\n - [ ] /msg (/tell and /w)\n - [ ] /op\n - [ ] /pardon\n - [ ] /pardon-ip\n - [ ] /particle\n - [ ] /place\n - [ ] /playsound\n - [ ] /publish\n - [ ] /recipe\n - [ ] /save-all\n - [ ] /save-off\n - [ ] /save-on\n - [x] /say\n - [ ] /schedule\n - [x] /scoreboard\n - [ ] /seed\n - [ ] /setblock\n - [ ] /setidletimeout\n - [ ] /setworldspawn\n - [ ] /spawnpoint\n - [ ] /spectate\n - [ ] /spreadplayers\n - [ ] /stop\n - [ ] /stopsound\n - [ ] /summon\n - [ ] /tag\n - [ ] /team\n - [ ] /teammsg (/tm)\n - [ ] /teleport (/tp)\n - [ ] /tellraw\n - [ ] /time\n - [ ] /title\n - [ ] /trigger\n - [ ] /weather\n - [ ] /whitelist\n - [ ] /worldborder\n\n## Feedback\n\nIf you have any feedback, feature request, or think you know how a feature could be improved, feel free to open an issue.',
    'author': 'PaddeCraft',
    'author_email': 'paddecraft@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
