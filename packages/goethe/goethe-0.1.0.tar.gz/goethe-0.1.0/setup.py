# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['goethe']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.4,<2.0.0']

setup_kwargs = {
    'name': 'goethe',
    'version': '0.1.0',
    'description': 'Create Sphinx RST documents programmatically with Python',
    'long_description': 'goethe\n######\n\nCreate RST documents programmatically with Python\n\nIntroduction\n************\n\nGoethe gives you the opportunity to create your individual RST project in Python\n\n1. **programmatically** - write your project as Python script in OOP style, place variables where ever you want\n2. **dynamically** - render the project to dict, json or actual files and even PDF\n\nSetup\n*****\n\nVia Pip:\n\n.. code-block:: bash\n\n    pip install goethe\n\nVia Github (latest):\n\n.. code-block:: bash\n\n    pip install git+https://github.com/earthobservations/goethe\n\nStructure\n*********\n\nGoethe uses 3 main levels of abstraction:\n\n- Goethe - initialize an RST project with a Goethe\n- FlatChapter - add a chapter based on one file at the same level as the Goethe\n- DeepChapter - add a chapter based on a folder with its own index\n\nA simple project could look like e.g.\n\n.. code-block:: python\n\n    Goethe("myproj")\n    FlatChapter("overview")\n    DeepChapter("depper_level)\n        FlatChapter("overview")\n        DeepChapter("second_chapter")\n\n\nwith following file structure:\n\n.. code-block:: python\n\n    ./\n    index.rst\n    overview.rst\n\n    ./deeper_level\n    index.rst\n    overview.rst\n\n    ./deeper_level/second_chapter\n    index.rst\n\nFeatures\n********\n\n- setup a RST project\n- export to dict, files or html\n- flat and deep chapters to build unlimited depth of documentation\n- modules of RST:\n    - toctree\n    - paragraph\n\nBacklog\n*******\n\nExamples\n********\n\nVisualized examples can be found in the ``examples`` folder.\n\nLicense\n*******\n\nDistributed under the MIT License. See ``LICENSE`` for more info.\n\nBacklog\n*******\n\nChangelog\n*********\n\nDevelopment\n===========\n',
    'author': 'Benjamin Gutzmann',
    'author_email': 'gutzemann@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/earthobservations/goethe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
