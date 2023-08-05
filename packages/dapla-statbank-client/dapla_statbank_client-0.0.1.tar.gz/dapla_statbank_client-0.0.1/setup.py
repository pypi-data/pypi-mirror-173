# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['statbank']

package_data = \
{'': ['*']}

install_requires = \
['build>=0.8.0,<0.9.0',
 'dapla-toolbelt>=1.3.3,<2.0.0',
 'ipywidgets>=8.0.2,<9.0.0',
 'pandas>=1.5.0,<2.0.0',
 'pyjstat>=2.3.0,<3.0.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'dapla-statbank-client',
    'version': '0.0.1',
    'description': 'Handles data transfer Statbank <-> Dapla for Statistics Norway',
    'long_description': '# dapla-statbank-client\nUsed internally by SSB (Statistics Norway).\nValidates and transfers data from Dapla to Statbank.\nGets data from public and internal statbank.\n\n\n### Usage Transferring\n```python\nfrom statbank import StatbankClient\nstat_client = StatbankClient(loaduser = "LASTEBRUKER")\n# Fill out password\nstat_client.transfer(df_06399, tabellid="06339")\n```\nThe simplest form of usage, is directly-transferring using the transfer-method under the client-class. If the statbanktable expects multiple "deltabeller", dataframes must be passed in a list, in the correct order.\n\nValidation will happen by default on user-side, in Python, using the "UttrekksBeskrivelse" (filbeskrivelse). Validation can be disabled using the "validation"-parameter on the client.\nValidation happens on the number of tables, number of columns, code usage in categorical columns, code usage in "suppression-columns" (prikkkolonner), and on timeformats (both length and characters used).\n\nYou can validate the data using the validate-method, without starting a transfer, like this:\n\n```python\nstat_client.validate(df_06339, tableid="06339")\n```\n\nYou can also look at the "filbeskrivelse" which is in its own local class: StatbankUttrekksBeskrivelse\n```python\ndescription_06339 = stat_client.get_description(tableid="06339")\nprint(description_06339)\n```\n\n\n### Usage get apidata\n\n```python\nclient.apidata_all("06339", include_id=True)\n```\n`apidata_all`, does not need a specified query, it will build its own query, trying to get *all the data* from the table. This might be too much, resulting in an error.\n\nThe `include_id`-parameter is a bit *magical*, it gets both codes and value-columns for categorical columns, and tries to merge these next to each other, it also makes a check if the content i the same, then it will not include the content twice.\n\nIf you want to specify a query, to limit the response, use the method `apidata` instead.\\\nHere we are requesting an "internal table" which only people at SSB have access to, with a specified URL and query.\n```python\nquery = {\'query\': [{\'code\': \'Region\', \'selection\': {\'filter\': \'vs:Landet\', \'values\': [\'0\']}}, {\'code\': \'Alder\', \'selection\': {\'filter\': \'vs:AldGrupp19\', \'values\': [\'000\', \'001\', \'002\', \'003\', \'004\', \'005\', \'006\', \'007\', \'008\', \'009\', \'010\', \'011\', \'012\', \'013\', \'014\', \'015\', \'016\', \'017\', \'018\', \'019\', \'020\', \'021\', \'022\', \'023\', \'024\', \'025\', \'026\', \'027\', \'028\', \'029\', \'030\', \'031\', \'032\', \'033\', \'034\', \'035\', \'036\', \'037\', \'038\', \'039\', \'040\', \'041\', \'042\', \'043\', \'044\', \'045\', \'046\', \'047\', \'048\', \'049\', \'050\', \'051\', \'052\', \'053\', \'054\', \'055\', \'056\', \'057\', \'058\', \'059\', \'060\', \'061\', \'062\', \'063\', \'064\', \'065\', \'066\', \'067\', \'068\', \'069\', \'070\', \'071\', \'072\', \'073\', \'074\', \'075\', \'076\', \'077\', \'078\', \'079\', \'080\', \'081\', \'082\', \'083\', \'084\', \'085\', \'086\', \'087\', \'088\', \'089\', \'090\', \'091\', \'092\', \'093\', \'094\', \'095\', \'096\', \'097\', \'098\', \'099\', \'100\', \'101\', \'102\', \'103\', \'104\', \'105\', \'106\', \'107\', \'108\', \'109\', \'110\', \'111\', \'112\', \'113\', \'114\', \'115\', \'116\', \'117\', \'118\', \'119+\']}}, {\'code\': \'Statsbrgskap\', \'selection\': {\'filter\': \'vs:Statsborgerskap\', \'values\': [\'000\']}}, {\'code\': \'Tid\', \'selection\': {\'filter\': \'item\', \'values\': [\'2022\']}}], \'response\': {\'format\': \'json-stat2\'}}\n\nclient.apidata("https://i.ssb.no/pxwebi/api/v0/no/prod_24v_intern/START/be/be01/folkemengde/Rd0002Aa",\n        query,\n        include_id = True\n       )\n```\n\n\n### Usage batches\nFor the transferring methods, there are "twin" batch-methods. \nAlternatively you can just run the methods above multiple times...\n\nTo transfer many tables at the same time.\n```python\ntransfers = stat_client.transfer_batch({"06339": df_06399,\n                                        "05300": df_05300})\nprint(transfers["05300"])\n```\n\nTo validate many tables at the same time.\n```python\nstat_client.validate_batch({"06339": df_06399,\n                            "05300": df_05300})\n```\n\nTo get many descriptions at once send a list.\n```python\ndescriptions = stat_client.validate_batch(["06339","05300"])\nprint(descriptions["06339"])\n```',
    'author': 'Statistics Norway',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
