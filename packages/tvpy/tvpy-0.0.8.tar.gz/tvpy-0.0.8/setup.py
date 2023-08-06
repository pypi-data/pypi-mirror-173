# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tvpy']

package_data = \
{'': ['*']}

install_requires = \
['1337x>=1.2.3,<2.0.0',
 'Pillow>=9.2.0,<10.0.0',
 'beautifulsoup4>=4.11.1,<5.0.0',
 'fire>=0.4.0,<0.5.0',
 'fs.smbfs>=1.0.5,<2.0.0',
 'libtorrent>=2.0.7,<3.0.0',
 'parse-torrent-title>=2.4,<3.0',
 'pyright>=1.1.273,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.5.1,<13.0.0',
 'toml>=0.10.2,<0.11.0',
 'tqdm>=4.64.0,<5.0.0',
 'websockets>=10.3,<11.0']

entry_points = \
{'console_scripts': ['tv-down = tvpy.main:tv_down',
                     'tv-html = tvpy.main:tv_html',
                     'tv-info = tvpy.main:tv_info',
                     'tv-json = tvpy.main:tv_json',
                     'tv-klyn = tvpy.main:tv_klyn',
                     'tv-renm = tvpy.main:tv_renm',
                     'tv-subs = tvpy.main:tv_subs',
                     'tvpy = tvpy.main:tvpy']}

setup_kwargs = {
    'name': 'tvpy',
    'version': '0.0.8',
    'description': '📺 TvPy',
    'long_description': '# 📺 TvPy \nBest command line to manage tv shows.\n\n[![asciicast](https://asciinema.org/a/c9vcmIziWPfZUXPDlVToBteyT.svg)](https://asciinema.org/a/c9vcmIziWPfZUXPDlVToBteyT)\n\n## Installation\n```shell\n> pip install tvpy\n```\n\n## Get an API Key\nYou need to get an API key from [TMDB](https://www.themoviedb.org/settings/api) and save it as `key.txt` in your working directory.\n\n## Usage\n```shell\n> mkdir Carnival.Row \n> tvpy Carnival.Row \n```\n',
    'author': 'Gilad Kutiel',
    'author_email': 'gilad.kutiel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gkutiel/tvpy/tree/master',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
