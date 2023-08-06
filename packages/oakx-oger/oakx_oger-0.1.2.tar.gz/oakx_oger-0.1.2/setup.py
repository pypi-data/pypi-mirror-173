# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['oakx_oger']

package_data = \
{'': ['*'], 'oakx_oger': ['input/*', 'input/tmp/*']}

install_requires = \
['OGER>=1.5,<2.0',
 'click>=8.1.3,<9.0.0',
 'importlib>=1.0.4,<2.0.0',
 'oaklib>=0.1.49,<0.2.0',
 'pystow>=0.4.6,<0.5.0',
 'setuptools>=65.0.1,<66.0.0',
 'tox>=3.25.1,<4.0.0']

extras_require = \
{':extra == "docs"': ['sphinx[docs]>=5.3.0,<6.0.0',
                      'sphinx-rtd-theme[docs]>=1.0.0,<2.0.0',
                      'sphinx-autodoc-typehints[docs]>=1.19.4,<2.0.0',
                      'sphinx-click[docs]>=4.3.0,<5.0.0',
                      'myst-parser[docs]>=0.18.1,<0.19.0']}

entry_points = \
{'console_scripts': ['oaker = oakx_oger.cli:main'],
 'oaklib.plugins': ['oger = oakx_oger.oger_implementation:OGERImplementation']}

setup_kwargs = {
    'name': 'oakx-oger',
    'version': '0.1.2',
    'description': 'oakx-oger',
    'long_description': '# oakx-oger\n\n[OGER](https://github.com/OntoGene/OGER) wrapper for oaklib.\n\n**ALPHA**\n\n## Usage\n\n```\npip install oakx-oger\nrunoak -i oger:sqlite:obo:envo annotate cultured organisms polar ecosystems atmospheric gas exchange\n```\n\n## How it works\n\nThis plugin implements an [OGER](https://github.com/OntoGene/OGER) wrapper.\n\nThere are two possible inputs to this wrapper:\n1. A `.txt` file [`runoak -i oger:sqlite:obo:envo annotate --text-file text.txt`]\n2. Words that need to be annotated.[`runoak -i oger:sqlite:obo:envo annotate cultured organisms polar ecosystems atmospheric gas exchange`]\n\nInput ontologies generally used `oaklib` can be used with an `oger:` prefix.\nNote: This has been tested only with `oger:sqlite:obo:*` for now.\n\n\n## Acknowledgements\n\nThis [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/README.html) project was developed from the [oakx-plugin-cookiecutter](https://github.com/INCATools/oakx-plugin-cookiecutter) template and will be kept up-to-date using [cruft](https://cruft.github.io/cruft/).',
    'author': 'Harshad Hegde',
    'author_email': 'hhegde@lbl.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
