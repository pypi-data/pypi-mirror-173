# datetime-itertool

[![Build Status](https://github.com/a.ilaletdinov/datetime-itertool/workflows/test/badge.svg?branch=master&event=push)](https://github.com/a.ilaletdinov/datetime-itertool/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/a.ilaletdinov/datetime-itertool/branch/master/graph/badge.svg)](https://codecov.io/gh/a.ilaletdinov/datetime-itertool)
[![Python Version](https://img.shields.io/pypi/pyversions/datetime-itertool.svg)](https://pypi.org/project/datetime-itertool/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

Simple datetime iterator


## Features

- Fully typed with annotations and checked with mypy, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)


## Installation

```bash
pip install datetime-itertool
```


## Example

Showcase how your project can be used:

```python
import datetime

from datetime_itertool.datetime_iterator import DateTimeIterator


start = datetime.datetime(2022, 2, 7)
end = datetime.datetime(2022, 2, 10)


for date_time in DateTimeIterator(start, end):
    print(date_time)

# 2022-02-07 00:00:00
# 2022-02-08 00:00:00
# 2022-02-09 00:00:00
```

## License

[MIT](https://github.com/a.ilaletdinov/datetime-itertool/blob/master/LICENSE)


## Credits

This project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [5fe13ee2646d5cf38736bacfa8f9dbbfac092efb](https://github.com/wemake-services/wemake-python-package/tree/5fe13ee2646d5cf38736bacfa8f9dbbfac092efb). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/5fe13ee2646d5cf38736bacfa8f9dbbfac092efb...master) since then.
