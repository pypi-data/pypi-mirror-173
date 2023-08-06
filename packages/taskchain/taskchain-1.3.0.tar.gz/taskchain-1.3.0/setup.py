# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['taskchain', 'taskchain.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'filelock>=3.8.0,<4.0.0',
 'h5py>=3.7.0,<4.0.0',
 'icecream>=2.1.3,<3.0.0',
 'networkx>=2.8.7,<3.0.0',
 'pandas>=1.5.1,<2.0.0',
 'pytest>=7.2.0,<8.0.0',
 'seaborn>=0.12.1,<0.13.0',
 'tabulate>=0.9.0,<0.10.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'taskchain',
    'version': '1.3.0',
    'description': 'Utility for running data and ML pipelines',
    'long_description': '# TaskChain\n\n[Documentation](https://flowerchecker.github.io/taskchain/)\n\n\n## Install\n\n```bash\npip install taskchain\n```\n\n#### From source\n```bash\ngit clone https://github.com/flowerchecker/taskchain\ncd taskchain\npython setup.py install\n# or\npython setup.py develop\n```\n\n## Changelog\n\n#### 1.2.1\n- fixes\n\n\n#### 1.2.0\n- remove redundant module `taskchain.task`\n- add support for task exclusion, just use `exluded_tasks` in your config\n- add tools for testing, check `taskchain.utils.testing`\n- finish documentation\n- remove some redundant methods\n\n#### 1.1.1\n- improve chain representation in jupyter\n- add `tasks_df` parameter to chains\n- add support for `uses` in contexts (same syntax as in configs)\n- improve create_readable_filenames\n  - use config name as default name\n  - better verbose mode\n- `force` method of both Chain and Task now supports `delete_data` parameter which delete persisted data \n  - it defaults to `False`\n  - be careful with this\n- add [Makefile](Makefile)\n\n#### 1.1.0\n- release to PIP\n\n#### 1.0.3\n- more types can be used for `run` method, e.g. `dict` or `Dict[str, int]`\n- forbid some names of parameters with special meaning in configs (`uses`, `tasks`, ...)\n- you should import from `taskchain` instead of `taskchain.taks`, later is deprecated and will be removed\n  - use `from taskchain import Task, Config, Chain` or `import taskchain as tc; tc.Task`\n- MultiChain are now more robust, you can use them with configs with context, and it will work correctly \n\n## Development\n\n#### Release new version to PIP\n\n```bash\npip install bumpversion twine\n\nmake version-patch\n# OR\nmake version-minor\n\nmake publish\n```\n\n#### Develop docs\nrun server which dynamically serves docs web.\n```bash\nmake docs-develop\n```\n\n#### Build docs\n\nCreate documentation as static files. \n```bash\nmake docs-build\n```\n\n\n#### Build docs\n\nBuilds documentation and deploys it to GitHub Pages\n```bash\nmake make docs-publish\n```\n',
    'author': ' Jiří Thran Řihák',
    'author_email': 'exthran@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://flowerchecker.github.io/taskchain/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
