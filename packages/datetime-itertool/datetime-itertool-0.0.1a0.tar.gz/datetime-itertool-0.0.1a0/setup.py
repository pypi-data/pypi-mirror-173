# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datetime_itertool']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'datetime-itertool',
    'version': '0.0.1a0',
    'description': 'Simple datetime iterator',
    'long_description': '# datetime-itertool\n\n[![Build Status](https://github.com/a.ilaletdinov/datetime-itertool/workflows/test/badge.svg?branch=master&event=push)](https://github.com/a.ilaletdinov/datetime-itertool/actions?query=workflow%3Atest)\n[![codecov](https://codecov.io/gh/a.ilaletdinov/datetime-itertool/branch/master/graph/badge.svg)](https://codecov.io/gh/a.ilaletdinov/datetime-itertool)\n[![Python Version](https://img.shields.io/pypi/pyversions/datetime-itertool.svg)](https://pypi.org/project/datetime-itertool/)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\nSimple datetime iterator\n\n\n## Features\n\n- Fully typed with annotations and checked with mypy, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)\n\n\n## Installation\n\n```bash\npip install datetime-itertool\n```\n\n\n## Example\n\nShowcase how your project can be used:\n\n```python\nimport datetime\n\nfrom datetime_itertool.datetime_iterator import DateTimeIterator\n\n\nstart = datetime.datetime(2022, 2, 7)\nend = datetime.datetime(2022, 2, 10)\n\n\nfor date_time in DateTimeIterator(start, end):\n    print(date_time)\n\n# 2022-02-07 00:00:00\n# 2022-02-08 00:00:00\n# 2022-02-09 00:00:00\n```\n\n## License\n\n[MIT](https://github.com/a.ilaletdinov/datetime-itertool/blob/master/LICENSE)\n\n\n## Credits\n\nThis project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [5fe13ee2646d5cf38736bacfa8f9dbbfac092efb](https://github.com/wemake-services/wemake-python-package/tree/5fe13ee2646d5cf38736bacfa8f9dbbfac092efb). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/5fe13ee2646d5cf38736bacfa8f9dbbfac092efb...master) since then.\n',
    'author': 'Almaz Ilaletdinov',
    'author_email': 'a.ilaletdinov@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/blablatdinov/datetime-itertool',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
