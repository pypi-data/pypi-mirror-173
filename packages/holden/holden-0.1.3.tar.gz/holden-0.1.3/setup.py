# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['holden']

package_data = \
{'': ['*']}

install_requires = \
['amos>=0.1.10,<0.2.0', 'miller>=0.1.2,<0.2.0']

setup_kwargs = {
    'name': 'holden',
    'version': '0.1.3',
    'description': 'lightweight, accessible, flexible composite data structures',
    'long_description': '[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![Documentation Status](https://readthedocs.org/projects/holden/badge/?version=latest)](http://holden.readthedocs.io/?badge=latest)\n\n<p align="center">\n<img src="https://media.giphy.com/media/3ornjRyce6SukW8INi/giphy.gif" />\n</p>\n\nThis package is named after the Roci\'s captain in The Expanse, James Holden, who was adept at furling his brow and recognizing connections. In a similar vein, holden offers users easy-to-use composite data structures without the overhead or complexity of larger graph packages. The included graphs are built for basic workflow design or analysis of conditional relationships. They are not meant for big data network analysis or similar large-scale projects (although nothing prevents you from using them in that manner). Rather, the goal of holden is to provide lightweight, turnkey, extensible graphs without all of the stuff you don\'t need in packages like [networkx](https://github.com/networkx/networkx) or [airflow](https://github.com/apache/airflow).\n\n## Simple\n\nThe basic building blocks provided are:\n* Graph: the base class for all graph data structures\n* Edge: an optional edge class which can be treated as a drop-in tuple replacement or extended for greater functionality\n* Node: an optional vertex class which provides universal hashability and some other convenient functions\n* Forms: a dictionary that automatically stores all direct Graph subclasses to allow flexible subtype checking of and transformation between graph subtypes using the \'classify\' and \'transform\' methods\n\nOut of the box, Graph has several subtypes with varying internal storage formats:\n* Adjacency: an adjacency list using a dict(Hashable, set(Hashable)) structure\n* Matrix: an adjacency matrix that uses a list[list[Hashable]] for mapping edges and a separate list[str] attribute that corresponds to the list of lists matrix\n* Edges: an edge list structure that uses a list[tuple[Hashable, Hashable]] format\n  \nYou can use holden without any regard to what is going on inside the graph. The methods and properties are the same regardless of which internal format is used. But the different forms are provided in case you want to utilize the advantages of each form or avoid certain drawbacks. Unless you want to design a different graph form, you should design subclasses to inherit from one of the\nincluded types and add mixins to expand functionality.\n\n## Flexible\n\n Various traits can be added to graphs, nodes, and edges as mixins including:\n* Weighted edges (Weighted)\n* Abilty to create a graph from or convert any graph to any recognized form (Fungible)\n* Directed graphs (Directed)\n* Automatically names objects if a name is not passed (Labeled)\n* Ability to store nodes internally for easy reuse separate from the graph structure (Storage)\n\nholden provides transformation methods between all of the internal storage forms as well as functions to convert graphs into a set of paths (Parallel) or a single path (Serial). The transformation methods can be used as class properties or with functions using an easy-to-understand naming convention (e.g., adjacency_to_edges or edges_to_parallel).\n\nholden\'s framework supports a wide range of coding styles. You can create complex multiple inheritance structures with mixins galore or simpler, compositional objects. Even though the data structures are necessarily object-oriented, all of the tools to modify them are also available as functions, for those who prefer a more functional approaching to programming.\n\n## Contributing\n\nThe project is also highly documented so that users and developers and make holden work with their projects. It is designed for Python coders at all levels. Beginners should be able to follow the readable code and internal documentation to understand how it works. More advanced users should find complex and tricky problems addressed through efficient code.\n\nI hope you find holden useful and feel free to contribute, leave suggestions, or report bugs.\n\n<p align="center">\n<img src="https://media.giphy.com/media/3oKIPwyf0EBAGnAkWk/giphy.gif" />\n</p>\n',
    'author': 'Corey Rayburn Yung',
    'author_email': 'coreyrayburnyung@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/WithPrecedent/holden',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
