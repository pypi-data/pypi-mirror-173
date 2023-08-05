# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fakesmtpd']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=4.0.1,<5.0.0']

entry_points = \
{'console_scripts': ['fakesmtpd = fakesmtpd.server:main']}

setup_kwargs = {
    'name': 'fakesmtpd',
    'version': '2022.10.1',
    'description': 'SMTP server for testing mail functionality',
    'long_description': '# FakeSMTPd\n\n[![License](https://img.shields.io/pypi/l/FakeSMTPd.svg)](https://pypi.python.org/pypi/FakeSMTPd/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fakesmtpd)\n[![GitHub Release](https://img.shields.io/github/release/srittau/fakesmtpd/all.svg)](https://github.com/srittau/FakeSMTPd/releases/)\n[![pypi Release](https://img.shields.io/pypi/v/FakeSMTPd.svg)](https://pypi.python.org/pypi/FakeSMTPd/)\n[![Build Status](https://travis-ci.org/srittau/FakeSMTPd.svg?branch=master)](https://travis-ci.org/srittau/FakeSMTPd)\n\nFakeSMTPd is an SMTP server for testing mail functionality. Any mail sent via\nthis server will be saved, but will not be forwarded any further.\n\nMail is printed to stdout by default in default mbox format, as defined in\n[RFC 4155](https://www.ietf.org/rfc/rfc4155.txt). The SMTP mail receivers\nare added in X-FakeSMTPd-Receiver headers.\n\nUsage\n-----\n\n`fakesmtpd [OPTIONS]`\n\nSupported options:\n\n  * `-o`, `--output-filename [FILENAME]` mbox file for output, default: stdout\n  * `-b`, `--bind [ADDRESS]` IP addresses to listen on, default: 127.0.0.1\n  * `-p`, `--port [PORT]` SMTP port to listen on\n\nDocker image [available](https://hub.docker.com/r/srittau/fakesmtpd/).\n',
    'author': 'Sebastian Rittau',
    'author_email': 'srittau@rittau.biz',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/srittau/fakesmtpd',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
