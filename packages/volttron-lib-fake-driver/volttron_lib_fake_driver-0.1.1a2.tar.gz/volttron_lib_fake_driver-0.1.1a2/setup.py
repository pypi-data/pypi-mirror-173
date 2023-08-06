# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['volttron', 'volttron.driver.interfaces.fake']

package_data = \
{'': ['*']}

install_requires = \
['volttron-lib-base-driver>=0.1.1a0,<0.2.0']

setup_kwargs = {
    'name': 'volttron-lib-fake-driver',
    'version': '0.1.1a2',
    'description': 'Fake Driver supported and maintained by the Volttron team.',
    'long_description': '# volttron-lib-fake-driver\n\n![Passing?](https://github.com/VOLTTRON/volttron-lib-fake-driver/actions/workflows/run_tests.yml/badge.svg)\n[![pypi version](https://img.shields.io/pypi/v/volttron-lib-fake-driver.svg)](https://pypi.org/project/volttron-lib-fake-driver/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nThis project contains Drivers supported and maintained by the Volttron team.\n\n# Prerequisites\n\n* Python 3.8\n* Poetry 1.2.2\n\n## Python\n\n<details>\n<summary>To install Python 3.8, we recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>\n\n```bash\n# install pyenv\ngit clone https://github.com/pyenv/pyenv ~/.pyenv\n\n# setup pyenv (you should also put these three lines in .bashrc or similar)\nexport PATH="${HOME}/.pyenv/bin:${PATH}"\nexport PYENV_ROOT="${HOME}/.pyenv"\neval "$(pyenv init -)"\n\n# install Python 3.8\npyenv install 3.8.10\n\n# make it available globally\npyenv global system 3.8.10\n```\n</details>\n\n\n## Poetry\n\nThis project uses `poetry` to install and manage dependencies. To install poetry,\nfollow these [instructions](https://python-poetry.org/docs/master/#installation).\n\n# Installation\n\nWith `pip`:\n\n```shell\npython3.8 -m pip install volttron-lib-fake-driver\n\n# Develop mode\npython3.8 -m pip install --editable volttron-lib-fake-driver\n```\n\n# Development\n\n## Environment\n\nSet the environment to be in your project directory:\n\n```poetry config virtualenvs.in-project true```\n\nIf you want to install all your dependencies, including dependencies to help with developing your agent, run this command:\n\n```poetry install```\n\nIf you want to install only the dependencies needed to run your agent, run this command:\n\n```poetry install --no-dev```\n\nActivate the virtual environment:\n\n```shell\n# using Poetry\npoetry shell\n\n# using \'source\' command\nsource "$(poetry env info --path)/bin/activate"\n```\n\n## Source Control\n\n1. To use git to manage version control, create a new git repository in your local agent project.\n\n```git init```\n\n2. Then create a new repo in your Github or Gitlab account. Copy the URL that points to that new repo in\nyour Github or Gitlab account. This will be known as our \'remote\'.\n\n3. Add the remote (i.e. the new repo URL from your Github or Gitlab account) to your local repository. Run the following command:\n\n```git remote add origin <my github/gitlab URL>```\n\nWhen you push to your repo, note that the default branch is called \'main\'.\n\n\n## Optional Configurations\n\n### Precommit\n\nNote: Ensure that you have created the virtual environment using Poetry\n\nInstall pre-commit hooks:\n\n```poetry run pre-commit install```\n\nTo run pre-commit on all your files, run this command:\n\n```poetry run pre-commit run --all-files```\n\nIf you have precommit installed and you want to ignore running the commit hooks\nevery time you run a commit, include the `--no-verify` flag in your commit. The following\nis an example:\n\n```git commit -m "Some message" --no-verify```\n\n\n# Publishing to PyPi\n\nPublishing your Driver module to PyPi is automated through the continuous integration workflow provided in `~/.github/workflows/publish_to_pypi.yml`.\nYou can update that Github Workflow with your credentials to ensure that publishing to PyPi will succeed. The default behavior of\nthat workflow is to publish to PyPi when a release has been published. If you want to change this behavior, you can modify the\nworkflow to publish to PyPi based on whatever desired event; see [Github Workflows docs](https://docs.github.com/en/actions/using-workflows/triggering-a-workflow)\non how to change the events that trigger a workflow.\n\n\n# Documentation\n\nTo build the docs, navigate to the \'docs\' directory and build the documentation:\n\n```shell\ncd docs\nmake html\n```\n\nAfter the documentation is built, view the documentation in html form in your browser.\nThe html files will be located in `~<path to project directory>/docs/build/html`.\n\n**PROTIP: To open the landing page of your documentation directly from the command line, run the following command:**\n\n```shell\nopen <path to project directory>/docs/build/html/index.html\n```\n\nThis will open the documentation landing page in your default browsert (e.g. Chrome, Firefox).\n',
    'author': 'Mark Bonicillo',
    'author_email': 'volttron@pnnl.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/eclipse-volttron/volttron-lib-fake-driver',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
