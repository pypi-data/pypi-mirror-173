# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dvbctrl']

package_data = \
{'': ['*']}

install_requires = \
['psutil>=5.9.1,<6.0.0']

setup_kwargs = {
    'name': 'dvbctrl',
    'version': '0.3.1',
    'description': 'Controls a local dvbstreamer',
    'long_description': '# dvbctrl\n\n## starting\n\n```python\nfrom dvbctrl.dvbstreamer import DVBStreamer\n\nadapter = 0\ndvbs = DVBStreamer(adapter)\nrunning = dvbs.start()\nif not running:\n    raise Exception(f"Failed to start dvbstreamer on adapter {adapter}")\n```\n\n## stopping\n\n```python\nfrom dvbctrl.dvbstreamer import DVBStreamer\n\nadapter = 0\ndvbs = DVBStreamer(adapter)\n\n...\n\nif dvbs.isRunning():\n    dvbs.stop()\n```\n\n## commands\n\n```python\nfrom dvbctrl.commands import DVBCommand\n\nkwargs = {\n    "adapter": 0,\n    "host": "127.0.0.1"\n    "pass": "dvbctrl"\n    "user": "dvbctrl"\n}\ndvbc = DVBCommand(**kwargs)\n\n# services (channels)\nchans = dvbc.lsservices()\n```\n',
    'author': 'ccdale',
    'author_email': 'chris.charles.allison+dvbctrl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
