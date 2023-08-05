# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['flake8_import_rules']
entry_points = \
{'flake8.extension': ['I013 = flake8_import_rules:ImportRulesChecker']}

setup_kwargs = {
    'name': 'flake8-import-rules',
    'version': '0.2.0',
    'description': '',
    'long_description': "Helps to prevent import of certain modules from certain modules.\n\nIt's useful if you have many modules in your project and want to keep them kind of\nisolated.\n\nAfter installing just add `import-rules` option to your `setup.cfg` file.\n\n```\n[flake8]\n...\nimport-rules= \n\t# yaml format here\n\t- module_one:\n\t\t- allow module_two\n\t\t- deny any\n\t- module_two:\n\t\t- deny module_one.sub.submodule\n\t- module_two.sumbodule:\n\t\t- deny module_one\n\t- module_three: allow any\n\n\t# many sectin for the same module are allowed\n\t# for example\n\t- module_two:\n\t\t- deny some_other_module\n\n\t# this will prevent any import everywhere\n\t- any:\n\t\t- deny any\n\n\t# default behaviour is\n\t- any:\n\t\t- allow any\n\n...\n```\nRules are checking top-down. The Order Matters.\n\nIf current module name match section name or is submodule, then it will check all imports by rules from the section.\n\nThere can be one or more rules in section.\nThere can be one or more sections for the same module/submodule.\n\n`allow modulepath` - means allow imports from `modulepath` and its submodules\n\n`deny modulepath` - means deny imports from `modulepath` and its submodules.\n\nKeyword `any` (or `all`) - menas any module (like `*`)\n\n\n",
    'author': 'VL',
    'author_email': '1844144@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
