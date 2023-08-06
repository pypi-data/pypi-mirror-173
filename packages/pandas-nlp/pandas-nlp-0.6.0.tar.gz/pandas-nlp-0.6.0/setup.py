# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandas_nlp', 'pandas_nlp.models']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'fasttext>=0.9.2,<0.10.0',
 'numpy>=1.15.0',
 'pandas>=1.3.0,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'spacy>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'pandas-nlp',
    'version': '0.6.0',
    'description': 'Pandas extension with NLP functionalities',
    'long_description': '# Pandas NLP\n\nIt\'s an extension for pandas providing some NLP functionalities for strings.\n\n[![build](https://github.com/jaume-ferrarons/pandas-nlp/actions/workflows/push-event.yml/badge.svg?branch=master)](https://github.com/jaume-ferrarons/pandas-nlp/actions/workflows/push-event.yml)\n[![version](https://img.shields.io/pypi/v/pandas_nlp?logo=pypi&logoColor=white)](https://pypi.org/project/pandas-nlp/)\n[![codecov](https://codecov.io/gh/jaume-ferrarons/pandas-nlp/branch/master/graph/badge.svg?token=UQUSYGANFQ)](https://codecov.io/gh/jaume-ferrarons/pandas-nlp)\n[![pyversion-button](https://img.shields.io/pypi/pyversions/pandas_nlp.svg)](https://pypi.org/project/pandas-nlp/)\n## Setup\n### Requirements \n- python >= 3.8\n\n### Installation\nExecute:\n```bash\npip install -U pandas-nlp\n```\nTo install the default spacy English model:\n```bash\nspacy install en_core_web_md\n```\n\n\n## Key features\n\n### Language detection\n```python\nimport pandas as pd\nimport pandas_nlp\n\npandas_nlp.register()\n\ndf = pd.DataFrame({\n    "id": [1, 2, 3, 4, 5],\n    "text": [\n        "I like cats",\n        "Me gustan los gatos",\n        "M\'agraden els gats",\n        "J\'aime les chats",\n        "Ich mag Katzen",\n    ],\n})\ndf.text.nlp.language()\n```\n**Output**\n```\n0    en\n1    es\n2    ca\n3    fr\n4    de\nName: text_language, dtype: object\n```\nwith confidence:\n```python\ndf.text.nlp.language(confidence=True).apply(pd.Series)\n```\n**Output**\n```\n  language  confidence\n0       en    0.897090\n1       es    0.982045\n2       ca    0.999806\n3       fr    0.999713\n4       de    0.997995\n```\n\n### String embedding\n```python\nimport pandas as pd\nimport pandas_nlp\n\npandas_nlp.register()\n\ndf = pd.DataFrame(\n    {"id": [1, 2, 3], "text": ["cat", "dog", "violin"]}\n)\ndf.text.nlp.embedding()\n```\n**Output**\n```\n0    [3.7032, 4.1982, -5.0002, -11.322, 0.031702, -...\n1    [1.233, 4.2963, -7.9738, -10.121, 1.8207, 1.40...\n2    [-1.4708, -0.73871, 0.49911, -2.1762, 0.56754,...\nName: text_embedding, dtype: object\n```\n\n### Closest concept\n```python\nimport pandas as pd\nimport pandas_nlp\n\npandas_nlp.register()\n\nthemed = pd.DataFrame({\n    "id": [0, 1, 2, 3],\n    "text": [\n        "My computer is broken",\n        "I went to a piano concert",\n        "Chocolate is my favourite",\n        "Mozart played the piano"\n    ]\n})\n\nthemed.text.nlp.closest(["music", "informatics", "food"])\n```\n**Output**\n```\n0    informatics\n1          music\n2           food\n3          music\nName: text_closest, dtype: object\n```\n\n### Sentence extraction\n```python\nimport pandas as pd\nimport pandas_nlp\n\npandas_nlp.register()\n\ndf = pd.DataFrame(\n    {"id": [0, 1], "text": ["Hello, how are you?", "Code. Sleep. Eat"]}\n)\ndf.text.nlp.sentences()\n```\n**Output**\n```python\n0    [Hello, how are you?]\n1     [Code., Sleep., Eat]\nName: text_sentences, dtype: object\n```',
    'author': 'Jaume Ferrarons',
    'author_email': 'jaume.ferrarons@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jaume-ferrarons/pandas-nlp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
