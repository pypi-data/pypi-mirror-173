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
    'version': '0.1.4',
    'description': 'PyMCFunction is a tool to write Minecraft datapacks in Python.',
    'long_description': '# PyMCFunction\n\nPyMCFunction is a tool to write Minecraft datapacks in Python.\n\n## Usage\n\nCheck `pymcfunction/pyfunction/pmf --help`\n\n## Docs\n\nHopefully coming soon, for now, ask somthing like IntelliSense.\n\n## Command support\n\nThese are the currently supported commands. Feel free to create a PR, the goal is to support every command.\n\n - [ ] /advancement\n - [ ] /attribute\n - [x] /ban\n - [x] /ban-ip\n - [x] /banlist\n - [x] /bossbar\n - [x] /clear\n - [ ] /clone\n - [ ] /data\n - [ ] /datapack\n - [ ] /debug\n - [x] /defaultgamemode\n - [x] /deop\n - [x] /difficulty\n - [ ] /effect\n - [ ] /enchant\n - [x] /execute\n - [ ] /experience (/xp)\n - [ ] /fill\n - [ ] /forceload\n - [x] /function\n - [x] /gamemode\n - [x] /gamerule\n - [x] /give\n - [x] /item\n - [x] /kick\n - [x] /kill\n - [ ] /locate\n - [ ] /loot\n - [x] /op\n - [x] /pardon\n - [x] /pardon-ip\n - [ ] /particle\n - [ ] /place\n - [ ] /playsound\n - [ ] /publish\n - [ ] /recipe\n - [x] /save-all\n - [x] /save-off\n - [x] /save-on\n - [x] /say\n - [ ] /schedule\n - [x] /scoreboard\n - [x] /seed\n - [ ] /setblock\n - [x] /setidletimeout\n - [x] /setworldspawn\n - [x] /spawnpoint\n - [x] /spectate\n - [ ] /spreadplayers\n - [x] /stop\n - [x] /stopsound\n - [x] /summon\n - [x] /tag\n - [x] /team\n - [x] /teammsg (/tm)\n - [x] /teleport (/tp)\n - [ ] /tellraw\n - [ ] /time\n - [ ] /title\n - [ ] /trigger\n - [x] /weather\n - [ ] /whitelist\n - [ ] /worldborder\n\n## Feedback\n\nIf you have any feedback, feature request, or think you know how a feature could be improved, feel free to open an issue.',
    'author': 'PaddeCraft',
    'author_email': 'paddecraft@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PaddeCraft/PyMCFunction',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
