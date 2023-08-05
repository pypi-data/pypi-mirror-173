# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['zkvvm']
install_requires = \
['appdirs>=1.4.4,<2.0.0', 'tqdm>=4.64.1,<5.0.0', 'vvm>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['zkvvm = zkvvm:main']}

setup_kwargs = {
    'name': 'zkvvm',
    'version': '0.1.0',
    'description': 'zkVyper version manager',
    'long_description': 'zkvvm\n=====\n\nA completely experimental and untested zkVyper version manager.\n\nUsage\n-----\n\n#. Install with pip.\n\n    .. code-block:: shell\n\n        $ pip install git+https://github.com/skellet0r/zkvvm@master#egg=zkvvm\n\n#. Use the built-in CLI\n\n    .. code-block:: shell\n\n        $ zkvvm --help\n        usage: zkvvm [-h] [--cache-dir CACHE_DIR] [--log-file LOG_FILE] [-v] {ls,ls-remote,install,uninstall} ...\n\n        zkVyper Version Manager\n\n        optional arguments:\n        -h, --help            show this help message and exit\n        --cache-dir CACHE_DIR\n                                Default: /home/user/.cache/zkvvm\n        --log-file LOG_FILE   Default: /home/user/.cache/zkvvm/log/zkvvm.log\n        -v\n\n        commands:\n        {ls,ls-remote,install,uninstall}\n            ls                  List available local versions\n            ls-remote           List available remote versions\n            install             Install a remote version\n            uninstall           Uninstall a local version\n\n#. Use in a script\n\n    .. code-block:: python\n\n        import zkvvm\n\n        output = zkvvm.compile(["tmp/Foo.vy"])\n\n        src = """# @version 0.3.3\n\n        @view\n        @external\n        def foo(_a: uint256) -> uint256:\n            return _a\n        """\n        output = zkvvm.compile_source(src, zk_version="1.1.1", vyper_version="0.3.3")\n',
    'author': 'Edward Amor',
    'author_email': 'edward.amor3@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
