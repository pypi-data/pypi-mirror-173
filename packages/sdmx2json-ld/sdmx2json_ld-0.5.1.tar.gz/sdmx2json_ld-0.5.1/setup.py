# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sdmx2jsonld',
 'sdmx2jsonld.common',
 'sdmx2jsonld.exceptions',
 'sdmx2jsonld.transform']

package_data = \
{'': ['*'], 'sdmx2jsonld': ['grammar/*']}

install_requires = \
['docopt==0.6.2',
 'fastapi==0.85.1',
 'hi-dateinfer==0.4.6',
 'lark==1.1.3',
 'loguru==0.6.0',
 'python-multipart==0.0.5',
 'rdflib>=6.2.0,<6.3.0',
 'requests==2.28.1',
 'schema==0.7.5',
 'secure==0.3.0',
 'uvicorn==0.19.0']

setup_kwargs = {
    'name': 'sdmx2json-ld',
    'version': '0.5.1',
    'description': 'A SDMX in RDF Turtle 1.1 format parser to generate valid JSON-LD and send to FIWARE Context Brokers using ETSI NGSI-LD.',
    'long_description': '<div id="top"></div>\n\n# SDMX to JSON-LD Parser\n\n<!-- PROJECT SHIELDS -->\n[![Stable Version][version-shield]][version-url]\n[![Issues][issues-shield]][issues-url]\n[![Apache2.0 License][license-shield]][license-url]\n[![Python Versions][python-shield]][python-url]\n[![Package Status][package-shield]][package-url]\n[![LinkedIn][linkedin-shield]][linkedin-url]\n\n\n<!-- PROJECT LOGO -->\n<br />\n<div align="center">\n  <a href="https://github.com/flopezag/IoTAgent-Turtle">\n    <img src="https://raw.githubusercontent.com/flopezag/IoTAgent-Turtle/master/images/logo.png" \nalt="Logo" width="280" height="160">\n  </a>\n\n<h3 align="center">SDMX (Turtle) to NGSI-LD (JSON-LD) converter</h3>\n\n  <p align="center">\n    A SDMX to JSON-LD parser to communicate with FIWARE Context Brokers using ETSI NGSI-LD.\n    <br />\n    <a href="https://github.com/flopezag/IoTAgent-Turtle"><strong>Explore the docs »</strong></a>\n    <br />\n    <br />\n    <a href="https://github.com/flopezag/IoTAgent-Turtle">View Demo</a>\n    ·\n    <a href="https://github.com/flopezag/IoTAgent-Turtle/issues">Report Bug</a>\n    ·\n    <a href="https://github.com/flopezag/IoTAgent-Turtle/issues">Request Feature</a>\n  </p>\n</div>\n\n\n<!-- ABOUT THE PROJECT -->\n## About The Project\n\nA SDMX in RDF Turtle 1.1 format parser to generate valid JSON-LD and send to FIWARE Context Brokers using ETSI NGSI-LD.\n\nIt is based on a \n[EBNF LALR(1) grammar](https://github.com/flopezag/IoTAgent-Turtle/blob/master/sdmx2jsonld/grammar/grammar.lark).\n\nThis project is part of INTERSTAT. For more information about the INTERSTAT Project, please check the url \nhttps://cef-interstat.eu.\n\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n\n### Dependencies\n\nThe dependencies of the sdmx2jsonld python package are the following:\n\n* [Lark - a modern general-purpose parsing library for Python](https://lark-parser.readthedocs.io/en/latest).\n* [hi-dateinfer - a python library to infer date format from examples](https://github.com/hi-primus/hi-dateinfer).\n* [Loguru - a library which aims to bring enjoyable logging in Python](https://loguru.readthedocs.io/en/stable/index.html).\n* [Requests - an elegant and simple HTTP library for Python, built for human beings](https://requests.readthedocs.io).\n* [RDFLib - a pure Python package for working with RDF](https://rdflib.readthedocs.io).\n\nFor more details about the versions of each library, please refer to \n[requirements.txt](https://github.com/flopezag/IoTAgent-Turtle/blob/master/requirements.txt).\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n\n\n<!-- GETTING STARTED -->\n## Installing SDMX2JSON-LD and Supported Versions\nSDMX2JSON-LD is available on PyPI:\n\n```bash\n$ python -m pip install sdmx2jsonld\n```\n\nSDMX2JSON-LD officially supports Python 3.10+.\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n\n\n<!-- USAGE EXAMPLES -->\n## Usage\n\nTo execute the python module you can follow the following code to parse the RDF Turtle file to generate the JSON-LD \ncontent to be sent to the FIWARE Context Broker:\n\n```python\nfrom sdmx2jsonld.transform.parser import Parser\nfrom sdmx2jsonld.exceptions import UnexpectedEOF, UnexpectedInput, UnexpectedToken\n\nfile_in = open("structures-accounts.ttl")\ngenerate_files = True\n\n# Start parsing the file\nmy_parser = Parser()\n\ntry:\n    my_parser.parsing(content=file_in, out=generate_files)\nexcept UnexpectedToken as e:\n    print(e)\nexcept UnexpectedInput as e:\n    print(e)\nexcept UnexpectedEOF as e:\n    print(e)\n```\n\nWhere:\n* `file_in` is the RDF Turtle content that can be a string in StringIO class or a read file in TextIOWrapper class.\n* `file_out` is a boolean variable to indicate if we want to save the JSON-LD parser content into files (True) or we \nwant to show the content in the screen (False).\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n\n<!-- CONTRIBUTING -->\n## Contributing\n\nContributions are what make the open source community such an amazing place to learn, inspire, and create. \nAny contributions you make are **greatly appreciated**. If you have a suggestion that would make this better, \nplease fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".\nDon\'t forget to give the project a star! Thanks again!\n\n1. Fork the Project\n2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)\n3. Commit your Changes (`git commit -m \'Add some AmazingFeature\'`)\n4. Push to the Branch (`git push origin feature/AmazingFeature`)\n5. Open a Pull Request\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n\n<!-- CONTACT -->\n## Contact\n\nFernando López - [@flopezaguilar](https://twitter.com/flopezaguilar) - fernando.lopez@fiware.org\n\nProject Link: [https://github.com/flopezag/IoTAgent-Turtle](https://github.com/flopezag/IoTAgent-Turtle)\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n\n<!-- LICENSE -->\n## License\n\nDistributed under the Apache2.0 License. See [LICENSE](https://github.com/flopezag/IoTAgent-Turtle/blob/master/LICENSE) \nfor more information.\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n\n<!-- MARKDOWN LINKS & IMAGES -->\n<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->\n[issues-shield]: https://img.shields.io/github/issues/flopezag/IoTAgent-Turtle.svg?style=flat\n[issues-url]: https://github.com/flopezag/IoTAgent-Turtle/issues\n\n[license-shield]: https://img.shields.io/github/license/flopezag/IoTAgent-Turtle\n[license-url]: https://github.com/flopezag/IoTAgent-Turtle/blob/master/LICENSE\n\n[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat&logo=linkedin&colorB=555\n[linkedin-url]: https://linkedin.com/in/fernandolopezaguilar\n\n[python-shield]: https://img.shields.io/pypi/pyversions/sdmx2json-ld\n[python-url]: https://pypi.org/project/sdmx2json-ld\n\n[version-shield]: https://img.shields.io/pypi/v/sdmx2json-ld\n[version-url]: https://pypi.org/project/sdmx2json-ld/#history\n\n[package-shield]: https://img.shields.io/pypi/status/sdmx2json-ld\n[package-url]: https://pypi.org/project/sdmx2json-ld\n',
    'author': 'Fernando López',
    'author_email': 'fernando.lopez@fiware.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/flopezag/IoTAgent-Turtle',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
