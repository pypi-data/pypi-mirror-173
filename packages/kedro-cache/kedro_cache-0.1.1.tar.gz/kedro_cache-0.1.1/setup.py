# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kedro_cache',
 'kedro_cache.config',
 'kedro_cache.framework',
 'kedro_cache.framework.cli',
 'kedro_cache.framework.hooks',
 'kedro_cache.template',
 'kedro_cache.utils']

package_data = \
{'': ['*'], 'kedro_cache.template': ['config/*']}

install_requires = \
['joblib>=1.2.0', 'kedro>=0.18.0', 'pydantic>=1.10.2', 'sqlitedict>=2.0.0']

entry_points = \
{'kedro.hooks': ['cache_hook = '
                 'kedro_cache.framework.hooks.cache_hook:cache_hook'],
 'kedro.project_commands': ['kedro_cache = '
                            'kedro_cache.framework.cli.cli:commands']}

setup_kwargs = {
    'name': 'kedro-cache',
    'version': '0.1.1',
    'description': 'A kedro-plugin that adds caching to kedro pipelines',
    'long_description': '# Kedro Cache\n\n> :warning: _This plugin is still under active developement and not fully tested. Do not use this in any production systems. Please report any issues that you find._\n\n## 📝 Description\n\n`kedro-cache` is a [kedro](https://kedro.org/) plugin that plugin that enables the caching of data sets.\nThe advantage is that the data sets are loaded from data catalog and not recomputed if they have not changed.\nIf the input data sets or code have changed, the outputs are recomputed and the data catalog is updated.\nThis plugin works out of the box with any kedro project without having to change the code.\nThe logic on how to determine if the cached data set in the catalog should be used is described in the flow chart below.\n\n![Caching Flowchart](static/img/caching_flowchart.svg)\n\n**Disclaimer:** _The caching strategy determines if a node function has changes by simply looking at the immediate function body.\nThis does not take into account other things such as called function, global variable etc. that might also have changed._\n\n## 🏆 Features\n\n- Caching of node outputs in catalog\n- No change to kedro project needed\n- Integration with kedro data catalog\n- Configuration via `config.yml` file\n\n## 🏗 Installation\n\nThe plugin can be install with `pip`\n\n```bash\npip install kedro-cache\n```\n\n## 🚀 Enable Caching\n\nIn the root directory of your kedro project, run\n\n```bash\nkedro cache init\n```\n\nThis will create a new file `cache.yml` in the `conf` directory of your kedro project in which you can configure the `kedro-cache` module.\nAlthough this step is optional as the plugin comes with default configurations.\n\nNext let\'s assume that you have the following kedro pipeline for which you want to add caching.\nThere are two nodes.\nOne that reads data from a `input` dataset, does some computations and writes it to a `intermediate` dataset and one that reads the data from the `intermediate` dataset and writes it to the `output` dataset.\n\n```python\n# pipeline.py\n\ndef register_pipelines() -> Dict[str, Pipeline]:\n    default_pipeline = pipeline(\n        [\n            node(\n                func=lambda x: x,\n                inputs="input",\n                outputs="intermediate",\n            ),\n            node(\n                func=lambda x: x,\n                inputs="intermediate",\n                outputs="output",\n            ),\n        ],\n    )\n    return {"__default__": default_pipeline}\n```\n\nIn order to add logging we simply just have to register all used data sets in the data catalog.\nBecause if the first node want to use the cached output instead of recalculating it, it need to load it from the data catalog.\nThis is only possible if it was stored there.\n\n```yaml\n# catalog.yml\n\ninput:\n  type: pandas.CSVDataSet\n  filepath: input.csv\n\nintermediate:\n  type: pandas.CSVDataSet\n  filepath: intermediate.csv\n\noutput:\n  type: pandas.CSVDataSet\n  filepath: output.csv\n```\n\nAnd that was it. Just by adding all files to the catalog you enabled caching.\n',
    'author': 'An Hoang',
    'author_email': 'anhoang31415@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/AnH0ang/kedro-cache',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
