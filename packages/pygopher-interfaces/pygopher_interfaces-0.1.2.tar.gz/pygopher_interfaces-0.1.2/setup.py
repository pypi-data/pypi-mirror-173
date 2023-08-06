# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pygopher']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata']

extras_require = \
{'docs': ['Sphinx', 'sphinx-rtd-theme']}

setup_kwargs = {
    'name': 'pygopher-interfaces',
    'version': '0.1.2',
    'description': 'Go-style interfaces for Python',
    'long_description': 'pygopher-interfaces\n===================\n\n.. rubric:: Go-style interfaces for Python\n\n|status| |pypi| |license| |documentation| |coverage| |analysis|\n\nInterfaces in the Go programming language are a bit different than those found in Java or C++, as they\nare `implicit <https://tour.golang.org/methods/10>`_.  This means that there is no explicit "implements" relationship\nbetween the interface definition and an implementation of the defined interface.  A type implements an interface by\nimplementing all of the methods defined.  When we wish to define an interface in Python, we typically use abstract\nbase classes to define them because we can enforce implementation of methods.  This requires us to use inheritance,\nwhich couples the interface and the implementation.\n\nThis package emulates Go-style interfaces by creating an ``Interface`` metaclass that can be used to construct Python\nclasses that override ``issubclass`` to test whether a class implements the methods of the interface class, rather than\nwhether it inherits from the interface class.\n\nThis is a tiny package that emulates on of my favorite features of Go.\n\n\nInstallation\n------------\n\n.. code-block:: console\n\n    pip install pygopher-interfaces\n    # or:\n    # pipenv install pygopher-interfaces\n    # poetry add pygopher-interfaces\n\nUsage\n-----\n\nTo create an interface class, use the ``Interface`` metaclass.\n\n.. code-block:: python\n\n    from pygopher.interfaces import Interface\n\n\n    class RepositoryInterface(metaclass=Interface):\n        def get(account_id: int) -> Account:\n            raise NotImplementedError\n\n        def add(account: Account):\n            raise NotImplementedError\n\n\n    class MysqlRepository:\n        def get(account_id: int) -> Account:\n            ...\n\n        def add(account: Account):\n            ...\n\n\n    >>> issubclass(MysqlRepository, RepositoryInterface)\n    True\n\n\n.. |status| image:: https://github.com/mrogaski/pygopher-interfaces/actions/workflows/pipeline.yml/badge.svg\n    :alt: Status\n    :target: https://github.com/mrogaski/pygopher-interfaces/actions\n\n.. |pypi| image:: https://img.shields.io/pypi/pyversions/pygopher-interfaces\n    :alt: PyPI - Python Version\n    :target: https://pypi.org/project/pygopher-interfaces/\n\n.. |license| image:: https://img.shields.io/pypi/l/pygopher-interfaces\n    :alt: PyPI - License\n    :target: https://github.com/mrogaski/pygopher-interfaces/blob/main/LICENSE\n\n.. |documentation| image:: https://img.shields.io/readthedocs/pygopher-interfaces\n    :alt: Read the Docs\n    :target: https://pygopher-interfaces.readthedocs.io/en/latest/\n\n.. |coverage| image:: https://codecov.io/gh/mrogaski/pygopher-interfaces/branch/main/graph/badge.svg?token=cu6sNIlaWt\n    :alt: Test Coverage\n    :target: https://codecov.io/gh/mrogaski/pygopher-interfaces\n\n.. |analysis| image:: https://app.codacy.com/project/badge/Grade/0516015cd3f94d66b7a7c8203255b6de\n    :alt: Code Quality\n    :target: https://www.codacy.com/gh/mrogaski/pygopher-interfaces/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=mrogaski/pygopher-interfaces&amp;utm_campaign=Badge_Grade\n\n',
    'author': 'Mark Rogaski',
    'author_email': 'mrogaski@pobox.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mrogaski/pygopher-interfaces',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
