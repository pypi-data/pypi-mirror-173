# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyqupa', 'pyqupa.assets', 'pyqupa.assets.screenshots']

package_data = \
{'': ['*'], 'pyqupa': ['db/*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'folium>=0.12.1,<0.13.0',
 'lxml>=4.9.1,<5.0.0',
 'numpy>=1.23.2,<2.0.0',
 'plotly>=5.10.0,<6.0.0',
 'pydeck>=0.7.1,<0.8.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'rich>=12.5.1,<13.0.0',
 'streamlit-folium>=0.6.15,<0.7.0',
 'streamlit>=1.12.2,<2.0.0',
 'tinydb>=4.7.0,<5.0.0']

setup_kwargs = {
    'name': 'pyqupa',
    'version': '0.1.1',
    'description': 'PYthon Qualdich.de mountain PAss data processor.',
    'long_description': '# PYQUPA: PYthon wrapper for [QUaeldich.de](https://www.quaeldich.de) mountain PAss data\n\nA Python interface to access data in [quaeldich.de](https://www.quaeldich.de).\n\n[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://pypass.streamlitapp.com)\n\nQuaeldich.de owns all rights to the data. I am therefore willing to give up the repository upon request from quaeldich.de.\n\n## Installation\n\nYou can use either [poetry](https://python-poetry.org) or pip.\n\n```bash\npip install pyqupa\n# or\npoetry add pyqupa\n```\n\n## How it works\n\n[Quaeldich.de](https://www.quaeldich.de) stores all mountain pass data in json files with unique data-ids. For example, **Mont Ventoux** approaching from **Bédoin** has geopositioning data (latitude, longitude, elevation, and distance) identified by `data-id=127_189`. Therefore, data can be accessed via the URL `https://www.quaeldich.de/qdtp/anfahrten/127_189.json`. We scraped all pass data URLs from the website and saved them in `pypass/db/passes.json`. Whenever you attempt to search for pass information, the code will first look for the URL and process data for you.\n\n\n## Basic usage\n\nBelow shows basic search options you can use with `pypass`.\n\n```python\n>>> from pypass.passees import PassDB\n>>> passdb = PassDB()\n>>> passdb.search("Mont Ventoux", "name")\n# List of a Pass with length == 1\n[Pass(name="Mont Ventoux", coord=[44.1736, 5.27879], ...)]\n>>> passdb.search("alpen", "region") # Only works for german names\n# List of Passes matching criteria\n[Pass(name="Stilfser Joch", ...), Pass(...), ...]\n# Below commands returns similar return type shown above\n>>> passdb.search("italien", "country") # Only works for german name\n>>> passdb.search([1800, 2000], "height")\n>>> passdb.search([10.0, 15.0], "distance")\n>>> passdb.search([500, 1000], "elevation")\n```\n\n## Features\n\n### Extract data\n\n- You can use cli command to extract data from quaeldich.de.\n    - You need two arguments `-e` and `-d`.\n    - If you set give 0 for `-e`, it will extract all data registered in quaeldich.de.\n    - If you don\'t set `-d` option, it will save db to `pypass/db/`.\n    - DB doesn\'t contain geopositioning data. Only relevant URLs to be processed later on.\n\n- Mac OS or Linux\n    ```zsh\n    python -m pypass -e NUMBER_OF_PASS_TO_BE_EXTRACTED -d DIRECTORY_TO_BE_SAVE_DB\n    ```\n- Windows\n    ```zsh\n    py -m pypass -e NUMBER_OF_PASS_TO_BE_EXTRACTED -d DIRECTORY_TO_BE_SAVE_DB\n    ```\n\n### DB structure\n\n`pypass` has two different DBs.\n- `pypass/db/passes.json`: DB contains all scraped Pass data from quaeldic.de. And the DB looks like:\n```json\n// pypass/db/passes.json\n{\n    "_default":\n    {\n        "1":\n        {\n            "name": ..., // name of Pass\n            "coord": ..., // coordinate of the summit\n            "country": ...,\n            "region": ...,\n            "height": ...,\n            "total_distance": ..., // distances of all paths to the summit\n            "total_elevation": ..., // elevation gain of all paths to the summit\n            "avg_grad": ..., // average gradient of each paths\n            "max_distance": ...,\n            "min_distance": ...,\n            "max_elevation": ...,\n            "min_elevation": ...,\n            "url": ..., // Pass url at quaeldich.de\n            "gpts": ..., // geopositioning data. No actual data, only links.\n            "status": ..., // HTTP reponse code. Always 200.\n        },\n        ...\n    }\n}\n```\n- `pypass/db/pass_names.json`: DB only contains all Pass names, regions, and country. If Pass has alternative name, it also stored as `alt`.\n\n\n### Search and access Pass data\n\n- You can search Pass data by region, name, height, distance, and elevation gain.\n\n- Each `Pass` class contains all paths to the top including information regarding distance, elevation, and gradient.\n```python\n>>> from pypass.passees import PassDB\n>>> passdb = PassDB()\n>>> Pass = passdb.search("Mont Ventoux", "name")  # Always return list[Pass]\n>>> Pass[0].path_names\n[\'South Side from Bédoin\', \'West Side from Malaucène\', \'East Side from Sault\']\n# Mont Ventoux has 3 access points.\n>>> Pass[0].total_distance\n[21169.514785722, 20846.819408688, 25365.999999999996]  # in meter\n>>> Pass[0].total_elevation\n[1592.295991259, 1572.2721899565, 1152.0] # in meter\n>>> Pass[0].avg_grad\n[7.521646137742093, 7.5420243209918585, 4.54151226050619] # in %\n>>> Pass[0].elevation\n[array([ 313, ..., 1905.29599126]), ...]\n# GPT log data for the elevation in meter (from start to end)\n```\n\n- Name suggestion for a typo when searching the pass.\n```python\n>>> from pypass.passees import PassDB\n>>> passdb = PassDB()\n>>> Pass = passdb.search("Mont Venoux", "name") # Wrong input name\n...\nNameError: The given name (Mont Ventox) is not in our database. Did you mean [\'Mont Ventoux\']?\n# Raise `NameError` and will give name suggestion for the close match.\n```\n\n\n### Running GUI\n\nWe created GUI using [steamlit](https://streamlit.io).\n\n- You can run GUI by typing following command in the file directory (git cloned directory):\n\n```zsh\npython -m streamlit run pypass/app.py\n```\n\n- Or you can simply run\n\n```zsh\npython -m pypass --gui # -g also works\n```\n\nIt is possible to access via [URL](https://pypass.streamlitapp.com)\n\n#### Demos:\n\n* Search by name:\n    - Pass can be searched by its name (supports drop-down menu).\n    - Visual representation of paths in 2D (Folium) and 3D (Deck.gl) map.\n    - Plots for the gradient profiles.\n\n<img src="./pypass/assets/screenshots/search_by_name.png" alt="search by name" width="500"/>\n\n* Search by distance/elevation/height:\n    - Passes are searched from the given range (using slider).\n    - If a number of searched data is larger than 10, display statistics (histogram).\n    - List of all searched data.\n\n<img src="./pypass/assets/screenshots/search_by_distance.png" alt="search by elevation" width="500"/>\n\n* Search by region/country:\n    - Passes are searched from the given region/country.\n    - Only works with German. However, you can search with drop-down menu.\n\n<img src="./pypass/assets/screenshots/search_by_region.png" alt="search by region" width="500"/>\n\n\n### Current issues/WIPs\n\nBelow is the list of issues or WIPs.\n\n#### DBs\n- [ ] Function to update DB data efficiently.\n\n#### GUI\n- [ ] Sorting table properly.\n\n#### MISC\n- [ ] Proper translation (German - English).\n- [ ] Fix all broken Pass names.\n- [ ] Make proper test files\n',
    'author': 'Kyoungseoun Chung',
    'author_email': 'kyoungseoun.chung@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
