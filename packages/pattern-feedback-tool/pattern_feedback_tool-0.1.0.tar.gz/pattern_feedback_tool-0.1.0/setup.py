# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pattern_feedback_tool']

package_data = \
{'': ['*']}

install_requires = \
['beartype>=0.11.0',
 'better-exceptions>=0.3.3',
 'calcipy>=0.20.1',
 'code2flow>=2.5.0',
 'doit>=0.34.2',
 'flake8-SQL>=0.4.1',
 'flake8-bandit>=3.0.0',
 'flake8-black>=0.3.3',
 'flake8-blind-except>=0.2.1',
 'flake8-breakpoint>=1.1.0',
 'flake8-broken-line>=0.4.0',
 'flake8-bugbear>=22.4.25',
 'flake8-builtins>=1.5.3',
 'flake8-comprehensions>=3.10.0',
 'flake8-debugger>=4.1.2',
 'flake8-eradicate>=1.2.1',
 'flake8-expression-complexity>=0.0.11',
 'flake8-functions>=0.0.7',
 'flake8-isort>=4.1.1',
 'flake8-pep3101>=1.3.0',
 'flake8-print>=5.0.0',
 'flake8-printf-formatting>=1.1.2',
 'flake8-return>=1.1.3',
 'flake8-simplify>=0.19.0',
 'flake8-string-format>=0.3.0',
 'flake8-super>=0.1.3',
 'flake8-tuple>=0.4.1',
 'flake8-typing-imports>=1.13.0',
 'flake8-use-pathlib>=0.3.0',
 'flake8>=5.0.4',
 'isort>=5.10.1',
 'mypy>=0.981',
 'pycg>=0.0.6',
 'pydantic>=1.8.1',
 'pylint>=2.13.9',
 'pyparsing>=3.0.9',
 'pytest-watcher>=0.2.3',
 'pytest>=7.1.2',
 'radon>=5.1.0',
 'rich>=12.6.0',
 'tomlkit>=0.11.5',
 'tryceratops>=1.1.0',
 'unimport>=0.11.3',
 'vulture>=2.4']

setup_kwargs = {
    'name': 'pattern-feedback-tool',
    'version': '0.1.0',
    'description': 'Design Pattern Feedback Tool',
    'long_description': '# pattern_feedback_tool\n\nDesign Pattern Feedback Tool\n\n## Installation\n\n1. `poetry add `\n\n1. ...\n\n   ```sh\n   import\n\n   # < TODO: Add example code here >\n   ```\n\n1. ...\n\n## Usage\n\n<!-- < TODO: Show an example (screenshots, terminal recording, etc.) > -->\n\nFor more example code, see the [scripts] directory or the [tests].\n\n## Project Status\n\nSee the `Open Issues` and/or the [CODE_TAG_SUMMARY]. For release history, see the [CHANGELOG].\n\n## Contributing\n\nWe welcome pull requests! For your pull request to be accepted smoothly, we suggest that you first open a GitHub issue to discuss your idea. For resources on getting started with the code base, see the below documentation:\n\n- [DEVELOPER_GUIDE]\n- [STYLE_GUIDE]\n- [CONTRIBUTING]\n\n## Code of Conduct\n\nWe follow the [Contributor Covenant Code of Conduct][contributor-covenant].\n\n## Responsible Disclosure\n\nIf you have any security issue to report, please contact the project maintainers privately. You can reach us at [dev.act.kyle@gmail.com](mailto:dev.act.kyle@gmail.com).\n\n## License\n\n[LICENSE]\n\n[changelog]: ./docs/CHANGELOG.md\n[code_tag_summary]: ./docs/CODE_TAG_SUMMARY.md\n[contributing]: ./docs/CONTRIBUTING.md\n[contributor-covenant]: https://www.contributor-covenant.org\n[developer_guide]: ./docs/DEVELOPER_GUIDE.md\n[license]: https://github.com/DesignPatternsAdventure/pattern_feedback_tool/LICENSE\n[scripts]: https://github.com/DesignPatternsAdventure/pattern_feedback_tool/scripts\n[style_guide]: ./docs/STYLE_GUIDE.md\n[tests]: https://github.com/DesignPatternsAdventure/pattern_feedback_tool/tests\n',
    'author': 'Kyle King',
    'author_email': 'dev.act.kyle@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/DesignPatternsAdventure/pattern_feedback_tool',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.5,<4.0.0',
}


setup(**setup_kwargs)
