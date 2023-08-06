# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pilotis',
 'pilotis.commands',
 'pilotis.domain',
 'templates',
 'templates.init.project.{{project_slug}}.python.tests',
 'templates.init.project.{{project_slug}}.python.tests.{{python_package_name}}.application',
 'templates.init.project.{{project_slug}}.python.{{python_package_name}}',
 'templates.init.project.{{project_slug}}.python.{{python_package_name}}.application',
 'templates.init.project.{{project_slug}}.python.{{python_package_name}}.domain',
 'templates.init.project.{{project_slug}}.python.{{python_package_name}}.domain.persistence',
 'templates.init.project.{{project_slug}}.python.{{python_package_name}}.domain.persistence.landing']

package_data = \
{'': ['*'],
 'templates': ['aws/*',
               'aws/project/infrastructure/*',
               'aws/project/makefiles/*',
               'aws/project/python/docs/*',
               'aws/project/scripts/*',
               'git/commons/*',
               'git/commons/project/*',
               'git/commons/project/makefiles/*',
               'git/commons/project/workdir/landing/parsed/*',
               'git/commons/project/workdir/landing/raw/*',
               'git/commons/project/workdir/use_cases/{{projectSlug}}/datasets/*',
               'git/commons/project/workdir/use_cases/{{projectSlug}}/exports/*',
               'git/commons/project/workdir/use_cases/{{projectSlug}}/models/*',
               'git/github/*',
               'git/github/project/*',
               'git/gitlab/*',
               'git/gitlab/project/*',
               'init/*',
               'init/project/{{project_slug}}/*',
               'init/project/{{project_slug}}/containers/base/*',
               'init/project/{{project_slug}}/containers/dash/*',
               'init/project/{{project_slug}}/containers/tests/*',
               'init/project/{{project_slug}}/makefiles/*',
               'init/project/{{project_slug}}/python/*',
               'init/project/{{project_slug}}/python/docs/*',
               'init/project/{{project_slug}}/python/notebooks/*',
               'init/project/{{project_slug}}/scripts/*',
               'init/project/{{project_slug}}/workdir/landing/parsed/*',
               'init/project/{{project_slug}}/workdir/landing/raw/*',
               'init/project/{{project_slug}}/workdir/use_cases/{{projectSlug}}/datasets/*',
               'init/project/{{project_slug}}/workdir/use_cases/{{projectSlug}}/exports/*',
               'init/project/{{project_slug}}/workdir/use_cases/{{projectSlug}}/models/*']}

install_requires = \
['GitPython>=3.1.13,<4.0.0',
 'click>=7.1.2,<8.0.0',
 'copier>=7.0.1,<8.0.0',
 'inquirer>=2.7.0,<3.0.0',
 'mkdocs-material>=7.1.9,<8.0.0',
 'toml>=0.10.2,<0.11.0']

extras_require = \
{'test': ['pytest>=5.1,<6.0',
          'pytest-mock>=3.5.1,<4.0.0',
          'PyHamcrest>=2.0.2,<3.0.0']}

entry_points = \
{'console_scripts': ['pilotis = pilotis.cli:main']}

setup_kwargs = {
    'name': 'pilotis',
    'version': '0.3.0a0',
    'description': 'Pilotis is the core package of an opinionated framework aiming at facilitating and accelerating the creation of Data Science python applications, from prototyping till usage in production',
    'long_description': 'None',
    'author': 'ekinox',
    'author_email': 'contact@ekinox.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
