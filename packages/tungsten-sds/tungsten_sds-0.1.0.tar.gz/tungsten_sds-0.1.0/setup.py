# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tungsten',
 'tungsten.parsers',
 'tungsten.parsers.globally_harmonized_system',
 'tungsten.parsers.supplier',
 'tungsten.parsers.supplier.sigma_aldrich']

package_data = \
{'': ['*']}

install_requires = \
['pdfminer.six>=20220524,<20220525']

setup_kwargs = {
    'name': 'tungsten-sds',
    'version': '0.1.0',
    'description': 'An MSDS parser.',
    'long_description': '<div align="center">\n    <a align="center" href="https://pypi.org/project/tungsten-sds/">\n        <img src="assets/tungsten-wide-dark-bg-pad.png" align="center" alt="Tungsten" />\n    </a>\n    <h1 align="center">Tungsten</h1>\n    <p align="center">A material safety data sheet parser.</p>\n</div>\n\n## Installation\nTungsten is available on PyPi via pip. To install, run the following command:\n```sh\npip install tungsten-sds\n```\n\n## Usage Example\n```python\nfrom pathlib import Path\n\nfrom tungsten import SigmaAldrichSdsParser\n\nsds_parser = SigmaAldrichSdsParser()\nsds_path = Path("sigma_aldrich_w4502.pdf")\n\n# Convert PDF file to parsed data\nwith open(sds_path, "rb") as f:\n    sds = sds_parser.parse_to_ghs_sds(f, sds_name=sds_path.stem)\n\n# Serialize parsed data to JSON and dump to a file\nwith open(sds_path.stem + ".json", "w") as f:\n    sds.dump(f)\n```\n\n## License\nThis work is licensed under MIT. Media assets in the `assets` directory are licensed under a\nCreative Commons Attribution-NoDerivatives 4.0 International Public License.\n',
    'author': 'Dennis Pham',
    'author_email': 'dennis@dennispham.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
