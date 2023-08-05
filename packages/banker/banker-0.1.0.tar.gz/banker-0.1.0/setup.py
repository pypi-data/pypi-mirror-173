# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['banker']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'banker',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Banker\n\n\nBanker is a wrapper around [nordigen](www.nordigen.com) APIs in order to obtain banking transactions. To use\nBanker, it is necessary to create an account at nordigen and obtain individual secret keys, more on that below.\n\n## Installation\n```sh\npip3 install banker\n```\n\n## Usage\n### 1. First time setup\nTo use Banker, it is first required to sign up at [nordigen](www.nordigen.com) and thereafter create secret keys at the\n[following link](https://ob.nordigen.com/user-secrets/). Afterwards, a **auth.yaml** file can be generated\nusing the following, together with the generated *secret_id* and *secret_key* from nordigen.\n```python\n>>> import banker \n\n>>> secret_id = "SECRET_ID_FROM_NORDIGEN"\n>>> secret_key = "SECRET_KEY_FROM_NORDIGEN"\n\n>>> client = banker.Client()\n>>> client.add_keys(secret_id, secret_key)\n```\nAfter running the above, an **auth.yaml** file will be created in the same folder. It is no longer necessary to use the *secret_id* and *secret_key* since everything will be stored in\nthe **auth.yaml** file. <br> <br> \n### 2. Create and sign agreement with a bank.\nNext, we would like to create a connection with a single bank. In order to do this, a unique id for an\ninstitution is needed. In this example, we are interested in connecting all accounts from **Swedbank** (if you\nhave any), which can be done in the following way.\n```python\n>>> client = banker.Client()\n# We need to find the unique institution_id for swedbank.\n>>> client.search_institution("swedbank")\n[{\'id\': \'SWEDBANK_SWEDSESS\',\n  \'name\': \'Swedbank\',\n  \'bic\': \'SWEDSESS\',\n  \'transaction_total_days\': \'730\',\n  \'countries\': [\'SE\'],\n  \'logo\': \'https://cdn.nordigen.com/ais/SWEDBANK_LONG_SWEDSESS.png\',\n  \'payments\': False}]\n\n# With the \'id\' above we can submit a requisition and sign an agreement. Open the following link and proceed to sign the agreement. \n>>> client.submit_requisition("SWEDBANK_SWEDSESS")\n\'https://ob.nordigen.com/psd2/start/..../SWEDBANK_SWEDSESS\'\n```\n<br>\n\n### 3. List available accounts and get transactions, balances, etc.\nNow it is possible to list all accounts that are available from the banks that you have signed an agreement\nwith.\n```python\n>>> client.accounts()\n{\'SWEDBANK_SWEDSESS\': [\'YOUR_SWEDBANK_ACCOUNT_ID_1\', \'YOUR_SWEDBANK_ACCOUNT_ID_2\'], \'NORWEGIAN_SE_NORWNOK1\': [\'YOUR_NORWEGIAN_ACCOUNT_ID_1\']}\n\n# With one account_id above, get all transactions from the last 90 days.\n>>> client.transactions("YOUR_ACCOUNT_ID")\nA lot of output, which varies between different banks.\n\n# It is also possible to obtain account balance.\n>>> client.account_balance("YOUR_ACCOUNT_ID")\n{\'balances\': [{\'balanceAmount\': {\'amount\': \'AMOUNT_HERE\', \'currency\': \'SEK\'}, \'balanceType\': \'interimAvailable\'}, {\'balanceAmount\': {\'amount\': \'AMOUNT_HERE\', \'currency\': \'SEK\'}, \'balanceType\': \'interimBooked\'}]}\n```',
    'author': 'Anton Normelius',
    'author_email': 'a.normelius@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
