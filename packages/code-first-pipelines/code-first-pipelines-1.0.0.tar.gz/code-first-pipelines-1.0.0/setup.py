# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cf_pipelines', 'cf_pipelines.base']

package_data = \
{'': ['*']}

install_requires = \
['cookiecutter>=2.1.1,<3.0.0',
 'mlflow>=1.29.0,<2.0.0',
 'ploomber>=0.21.1,<0.22.0',
 'typer>=0.6.1,<0.7.0']

extras_require = \
{'graphviz': ['pygraphviz>=1.10,<2.0']}

entry_points = \
{'console_scripts': ['pipelines = cf_pipelines.cli.__main__:main']}

setup_kwargs = {
    'name': 'code-first-pipelines',
    'version': '1.0.0',
    'description': 'A framework built on top of Ploomber that allows code-first definition of pipelines.',
    'long_description': 'Code-First Pipelines\n====================\n\nA framework built on top of [Ploomber](https://ploomber.io/) that allows code-first definition of pipelines. \n**No YAML needed!**  \n\n## Installation\n\nTo get the minimum code needed to use the pipelines, install it from PyPI:\n\n```shell\npip install code-first-pipelines\n```\n\n## Usage\n\n### Pipelines\n\n```python\nimport pandas as pd\nfrom sklearn import datasets\nfrom cf_pipelines import Pipeline\n\niris_pipeline = Pipeline("My Cool Pipeline")\n\n@iris_pipeline.step("Data ingestion")\ndef data_ingestion():\n    d = datasets.load_iris()\n    df = pd.DataFrame(d["data"])\n    df.columns = d["feature_names"]\n    df["target"] = d["target"]\n    return {"raw_data.csv": df}\n\niris_pipeline.run()\n```\n\nSee the [tutorial notebook](tutorials/Introduction%20to%20Pipelines.ipynb) for a more comprehensive example.\n\n### ML Pipelines\n\n```python\nimport pandas as pd\nfrom sklearn import datasets\nfrom cf_pipelines.ml import MLPipeline\n\niris_pipeline = MLPipeline("My Cool Pipeline")\n\n@iris_pipeline.data_ingestion\ndef data_ingestion():\n    d = datasets.load_iris()\n    df = pd.DataFrame(d["data"])\n    df.columns = d["feature_names"]\n    df["target"] = d["target"]\n    return {"raw_data.csv": df}\n\niris_pipeline.run()\n```\n\nSee the [tutorial notebook](tutorials/Introduction%20to%20ML%20Pipelines.ipynb) for a more comprehensive example.\n\n## Getting started with a template \n\nOnce installed, you can create a new pipeline template by running:\n\n```shell\npipelines new [pipeline name]\n```\n',
    'author': 'Prediction and Learning at Simply Business',
    'author_email': 'pal@simplybusiness.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
