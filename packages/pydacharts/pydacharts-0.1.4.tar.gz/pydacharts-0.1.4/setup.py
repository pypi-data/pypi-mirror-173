# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydacharts', 'pydacharts.plugins']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.0,<2.0.0']

setup_kwargs = {
    'name': 'pydacharts',
    'version': '0.1.4',
    'description': '',
    'long_description': '# pydacharts\n\nPydantic :heart: chartjs\nThis is a code generator for [ChartJS](https://www.chartjs.org) configuration JSON.\n\n## Set Up\n\n1. Pip install the package with `pip install pydacharts` or clone the repo\n2. Use the class generator to write a "config" file. One simple example\n\n```py\nfrom pydacharts.models import Config, Data, Dataset\n\ndef spending_by_year_chartjs() -> Config:\n    """\n    Return a chartjs "config" object for sip dataset\n    charting\n    """\n    return Config(\n        type="bar",\n        data=Data(\n            labels=["Green is nice", "Red is angry", "Blue is calming"],\n            datasets=[Dataset(\n                backgroundColor = ["green", "red", "blue"],\n                data = [1,2,3],\n                label = "We love colors"\n            )]\n        )\n    )\n```\n\n(This example should work standalone)\n\nFor running examples\n\n### Run Examples\n\n```\npip install flask\ncd serve\nflask run\n```\n\ngo to localhost:5000\n\n### Building\n\n```\npoetry build\npoetry version patch # or "major", "minor"\npoetry publish\n```\n\n### Developing\n\nClone in `editable` mode\n`pip install -e git+git://github.com/joshbrooks/pydacharts/#egg=pydacharts`\n',
    'author': 'Josh Brooks',
    'author_email': 'josh@catalpa.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
