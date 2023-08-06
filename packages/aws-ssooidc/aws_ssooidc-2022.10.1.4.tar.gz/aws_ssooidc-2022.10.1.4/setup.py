# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_ssooidc']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.78,<2.0.0']

setup_kwargs = {
    'name': 'aws-ssooidc',
    'version': '2022.10.1.4',
    'description': 'Create temporary credentials for AWS SSO-OIDC.',
    'long_description': "===============\n**aws_ssooidc**\n===============\n\nOverview\n--------\n\nCreate temporary credentials with AWS SSO-OIDC access tokens.\n\nPrerequisites\n-------------\n\n- *Python >= 3.6*\n- *boto3 (https://pypi.org/project/boto3/) >= 1.17.78*\n\nRequired (Positional) Arguments\n-------------------------------\n\n- Position 1: sso_url (the start URL for your AWS SSO login)\n\nOptional (Keyword) Arguments\n----------------------------\n\n- client_name\n    - Description: Arbitrary name of the SSO client to create.\n    - Type: String\n    - Default: 'ssoclient'\n- region\n    - Description: Your AWS region.\n    - Type: String\n    - Default: 'us-east-1'\n- timeout\n    - Description: Number of tries before giving up.\n    - Type: Integer\n    - Default: 30\n\nUsage\n-----\n\nInstallation:\n\n.. code-block:: BASH\n\n   pip3 install aws-ssooidc\n   # or\n   python3 -m pip install aws-ssooidc\n\nIn Python3:\n\n.. code-block:: PYTHON\n\n   import aws_ssooidc as sso\n\n   response = sso.gettoken('<sso_url>')\n   access_token = response['accessToken']\n\nIn BASH:\n\n.. code-block:: BASH\n\n   python [/path/to/]aws_ssooidc \\\n   -u <sso_url>\n",
    'author': 'Ahmad Ferdaus Abd Razak',
    'author_email': 'ahmad.ferdaus.abd.razak@ni.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fer1035/pypi-ssooidc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
