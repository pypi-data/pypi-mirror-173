# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ilias_course_watcher']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'pyxdg>=0.28,<0.29',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['icw = ilias_course_watcher:main']}

setup_kwargs = {
    'name': 'ilias-course-watcher',
    'version': '0.1.2',
    'description': 'Periodically check if courses are available',
    'long_description': '# Course Watcher for ILIAS\n\nThis is an unoffial Application. It is not associated with the ILIAS project.\n\nThis command line application let\'s you query your ILIAS instance in some specific ways described in the [task types section](#task-types).\n\n## Usage\n\nBecause I hate argparse, getopt and the likes and because a command might get pretty complicated otherwise, you only need to specify exactly one argument:\n\nThe path of the [config file]{#configuration}. Alternatively `-` can be specified to read the config file from stdin.\n\n```bash\n# Setup needed before!\n./icw config.json\n```\n\nThis programm does not (yet?) have any daemon capabilities. It conceived to be run regularly by another tool such as cron or systemd timers.\n\nExample configurations are provided in `ilias-course-watcher.service` + `ilias-course-watcher.timer` and `ilias-course-watcher.crontab`.\n\n## Setup\n\n### pypi.org (Recommended)\n\n```bash\npip install --user ilias-course-watcher\n```\n\n### Manual\n\n```bash\n# Install poetry using your package manager and then run:\npoetry install\npoetry build\npip install --user dist/*.tar.gz\n# This will install all needed dependencies in a virtual environment\n#\n### You could also install the dependencies specified in the\n### pyproject.toml yourself (maybe also in a virtual environment)\n### and run CourseWatcher.py directly. There\'s no need to use poetry.\n```\n\n### Systemd timer\n\n```bash\n./install-systemd-user-config.sh\n```\n\n## Configuration\n\nThe configuration is specified in JSON format.\nA template can be found in `template-config.json`.\n\nAlways specified need to be the fields:\n\n- "Domain": string\n- "Username": string\n- "Password": string\n- "Tasks": list of tasks\n\n```json\n{\n\t"Domain": "https://www.studon.fau.de",\n\t"Username": "my-username",\n\t"Password": "my-password",\n\t"Tasks": [\n\t\t... See Task Types ...\n\t]\n}\n```\n\n## Task Types\n\nThere are 3 different task types serving each a different function.\n\n### Search Entry (search_entry)\n\nA category search searches in a given Category page for entries containing\nthe given search string (case-insensitive).\n\n```json\n{\n\t"type": "search_entry",\n\t"search_object": "crs123456",\n\t"search_string": "WS 2023",\n\t"success_command": "notify-send"\n}\n```\n\nThe search_object can optionally include a `.html`-suffix.\n\nThe success_command is executed if the search_string was found in the title of one of the entries of the specified category, course or fold.\n\n\n### Search Update (search_update)\n\nAn update search remembers the contents of a category, course or fold page (if the search has been run before) and compares them to the current contents.\n\nA history of past contents is saved in the cached files.\n\nA cache directory can optionally be specified. By default the XDG Cache Directory is used (`~/.cache/ilias-course-watcher` by default).\n\n```json\n{\n\t"type": "search_update",\n\t"search_object": "fold123456.html",\n\t"cache_dir": "~/.ilias-course-watcher",\n\t"success_command": "command ls -1 -c ~/.ilias-course-watcher/fold123456.icw* | head -n 2 | tac | xargs diff"\n}\n```\n\nThe success_command is executed if an update has been detected.\nThe command pipeline in the example above prints the name of the files containing the up-to-date contents and the previous contents respectively. This output is then piped to xargs, which in turn then runs diff providing these two files as parameters. Other possible may include sending emails for example.\n\n### Queue Availability (queue)\n\nThe queue task is not yet implemented. It should in the future monitor a queue to a course, running the success command if the course is open for sign-up and maybe even try to sign up by itself.',
    'author': 'Merlin Sievers',
    'author_email': 'merlin@sievers.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/dann-merlin/ilias-course-watcher',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
