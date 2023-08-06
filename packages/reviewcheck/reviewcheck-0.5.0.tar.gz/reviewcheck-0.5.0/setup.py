# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reviewcheck', 'reviewcheck.common']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0',
 'pyyaml>=5.1,<6.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=12.4.4,<13.0.0',
 'shtab>=1.5.4,<2.0.0']

entry_points = \
{'console_scripts': ['reviewcheck = reviewcheck.app:run']}

setup_kwargs = {
    'name': 'reviewcheck',
    'version': '0.5.0',
    'description': "Tool to stay up to date with your reviews on GitLab – Don't let a comment slip you by",
    'long_description': '![reviewcheck logo](logo-short.png)\n\n# Reviewcheck\n\nReviewcheck is a tool to stay up to date with your reviews on GitLab. You can\nconfigure it to use any GitLab instance you have access to. The tool checks all\nopen merge requests in the repos chosen by you, and lets you know if there are\nopen threads that need your attention.\n\nReviewcheck is in active development.\n\n## Installation\n\nWhile the project is still in development, the best way to install it is by\ncloning the repository and running `poetry run reviewcheck` from within it. You\nwill need to have poetry installed. The process looks as follows:\n\n```\npip install poetry\ngit clone https://github.com/volvo-cars/Reviewcheck\ncd reviewcheck\npoetry run reviewcheck\n```\n\n## Documentation\n\nFor now, the only documentation is this README and the `--help` flag of the\nprogram itself. A proper\n[Wiki](https://github.com/volvo-cars/Reviewcheck/wiki) is\nunder construction.\n\n## FAQ [NYI]\n\nSee [FAQ (NYI)](docs/faq/faq.md) for more questions.\n\n## Support\n\nFor support or other queries, contact project owner [Simon\nBengtsson](mailto:simon.bengtsson.3@volvocars.com) or project maintainer [Pontus\nLaos](mailto:pontus.laos@volcoars.com).\n\n## Contributing\n\nSee the [contributing guide](CONTRIBUTING.md) for detailed instructions on how to get\nstarted with this project.\n\n## Code of Conduct\n\nThis project adheres to the [Code of Conduct](./.github/CODE_OF_CONDUCT.md). By\nparticipating, you are expected to honor this code.\n\n## License\n\nThis repository is licensed under [Apache License 2.0](LICENSE) © 2022 Volvo Cars.\n',
    'author': 'Simon Bengtsson',
    'author_email': 'simon.bengtsson.3@volvocars.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/volvo-cars/Reviewcheck',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)
