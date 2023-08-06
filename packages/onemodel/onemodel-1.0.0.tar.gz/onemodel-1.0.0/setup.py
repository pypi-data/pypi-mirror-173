# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['onemodel', 'onemodel.dsl', 'onemodel.objects', 'onemodel.utils']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.20,<4.0.0',
 'importlib-resources',
 'python-libsbml==5.19.2',
 'tabulate>=0.9.0,<0.10.0',
 'tatsu==4.4.0',
 'tomli']

entry_points = \
{'console_scripts': ['onemodel = onemodel.__main__:main']}

setup_kwargs = {
    'name': 'onemodel',
    'version': '1.0.0',
    'description': 'OneModel: an open-source SBML modeling tool',
    'long_description': '# OneModel\n\n[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n\n## Description\n\n**OneModel** is a Python package for defining dynamic synthetic biology models easily and efficiently.\n\nOneModel\'s syntax allows the definition of models with chemical reactions, ODEs and/or algebraic loops --which makes OneModel especially suitable for control theory applications where you need to combine biological processes with controllers implemented by DAEs.\nOneModel focuses on code readability and modularity; and provides the user with tools to check the coherence of the generated models.\nOneModel generates an [SBML](http://sbml.org/) model file as output, which can be easily converted to other language implementations (such as Matlab, Julia, OpenModelica) with sbml2dae, or you could use many of the great SBML software developed by the community.\n\n*This project is under active development.*\n\n\n- **Documentation**: https://onemodel.readthedocs.io/en/latest/\n\n## Installation\n\n*Requires Python 3.8 or greater installed.*\n\n```\n  pip install onemodel\n```\n\n## Citing\n\nIf you use OneModel in your research, please use the following citations in your published works:\n\n- Santos-Navarro, F. N., Navarro, J. L., Boada, Y., Vignoni, A., & Picó, J. (2022). "OneModel: an open-source SBML modeling tool focused on accessibility, simplicity, and modularity." *DYCOPS*.\n\n- Santos-Navarro, F. N., Vignoni, A., & Picó, J. (2022). "Multi-scale host-aware modeling for analysis and tuning of synthetic gene circuits for bioproduction." *PhD thesis*.\n\n## License\n\nCopyright 2022 Fernando N. Santos-Navarro, Jose Luis Herrero, Yadira Boada, Alejandro Vignoni, and Jesús Picó\n\nLicensed under the Apache License, Version 2.0 (the "License"); you may not use this software except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.\n',
    'author': 'Fernando N. Santos-Navarro',
    'author_email': 'fersann1@upv.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sb2cl/onemodel',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
