# Banker


Banker is a wrapper around [nordigen](www.nordigen.com) APIs in order to obtain banking transactions. To use
Banker, it is necessary to create an account at nordigen and obtain individual secret keys, more on that below.

## Installation
```sh
pip3 install banker
```

## Usage
### 1. First time setup
To use Banker, it is first required to sign up at [nordigen](www.nordigen.com) and thereafter create secret keys at the
[following link](https://ob.nordigen.com/user-secrets/). Afterwards, a **auth.yaml** file can be generated
using the following, together with the generated *secret_id* and *secret_key* from nordigen.
```python
>>> import banker 

>>> secret_id = "SECRET_ID_FROM_NORDIGEN"
>>> secret_key = "SECRET_KEY_FROM_NORDIGEN"

>>> client = banker.Client()
>>> client.add_keys(secret_id, secret_key)
```
After running the above, an **auth.yaml** file will be created in the same folder. It is no longer necessary to use the *secret_id* and *secret_key* since everything will be stored in
the **auth.yaml** file. <br> <br> 
### 2. Create and sign agreement with a bank.
Next, we would like to create a connection with a single bank. In order to do this, a unique id for an
institution is needed. In this example, we are interested in connecting all accounts from **Swedbank** (if you
have any), which can be done in the following way.
```python
>>> client = banker.Client()
# We need to find the unique institution_id for swedbank.
>>> client.search_institution("swedbank")
[{'id': 'SWEDBANK_SWEDSESS',
  'name': 'Swedbank',
  'bic': 'SWEDSESS',
  'transaction_total_days': '730',
  'countries': ['SE'],
  'logo': 'https://cdn.nordigen.com/ais/SWEDBANK_LONG_SWEDSESS.png',
  'payments': False}]

# With the 'id' above we can submit a requisition and sign an agreement. Open the following link and proceed to sign the agreement. 
>>> client.submit_requisition("SWEDBANK_SWEDSESS")
'https://ob.nordigen.com/psd2/start/..../SWEDBANK_SWEDSESS'
```
<br>

### 3. List available accounts and get transactions, balances, etc.
Now it is possible to list all accounts that are available from the banks that you have signed an agreement
with.
```python
>>> client.accounts()
{'SWEDBANK_SWEDSESS': ['YOUR_SWEDBANK_ACCOUNT_ID_1', 'YOUR_SWEDBANK_ACCOUNT_ID_2'], 'NORWEGIAN_SE_NORWNOK1': ['YOUR_NORWEGIAN_ACCOUNT_ID_1']}

# With one account_id above, get all transactions from the last 90 days.
>>> client.transactions("YOUR_ACCOUNT_ID")
A lot of output, which varies between different banks.

# It is also possible to obtain account balance.
>>> client.account_balance("YOUR_ACCOUNT_ID")
{'balances': [{'balanceAmount': {'amount': 'AMOUNT_HERE', 'currency': 'SEK'}, 'balanceType': 'interimAvailable'}, {'balanceAmount': {'amount': 'AMOUNT_HERE', 'currency': 'SEK'}, 'balanceType': 'interimBooked'}]}
```