# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ngsildclient',
 'ngsildclient.api',
 'ngsildclient.api.asyn',
 'ngsildclient.api.helper',
 'ngsildclient.model',
 'ngsildclient.model.attr',
 'ngsildclient.model.helper',
 'ngsildclient.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.8.0,<0.9.0',
 'geojson>=2.5.0,<3.0.0',
 'httpx>=0.23.0,<0.24.0',
 'isodate>=0.6.1,<0.7.0',
 'networkx>=2.8.7,<3.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.26.0,<3.0.0',
 'rich>=12.4.1,<13.0.0',
 'scalpl>=0.4.2,<0.5.0']

setup_kwargs = {
    'name': 'ngsildclient',
    'version': '0.5.0',
    'description': 'A Python library that helps building NGSI-LD entities and interacting with a NGSI-LD Context Broker',
    'long_description': '# The ngsildclient library\n\n[![NGSI-LD badge](https://img.shields.io/badge/NGSI-LD-red.svg)](https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.02.01_60/gs_CIM009v010201p.pdf)\n[![SOF support badge](https://nexus.lab.fiware.org/repository/raw/public/badges/stackoverflow/fiware.svg)](http://stackoverflow.com/questions/tagged/fiware)\n<br>\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![Read the Docs](https://img.shields.io/readthedocs/ngsildclient)](https://ngsildclient.readthedocs.io/en/latest/index.html)\n<br>\n[![deploy status](https://github.com/Orange-OpenSource/python-ngsild-client/workflows/CI/badge.svg)](https://github.com/Orange-OpenSource/python-ngsild-client/actions)\n[![PyPI](https://img.shields.io/pypi/v/ngsildclient.svg)](https://pypi.org/project/ngsildclient/)\n[![Python version](https://img.shields.io/pypi/pyversions/ngsildclient)](https://pypi.org/project/ngsildclient/)\n\n\n## Overview\n\n **ngsildclient** is a Python library dedicated to NGSI-LD.\n \n It combines :\n\n - a toolbox to create and modify NGSI-LD entities effortlessly\n - a NGSI-LD API client to interact with a Context Broker\n\n### Build entities\n\nFour primitives are provided `prop()`, `gprop()`, `tprop()`, `rel()` to build respectively a Property, GeoProperty, TemporalProperty and Relationship.\n\nAn Entity is backed by a Python dictionary that stores the JSON-LD payload.\nThe library operates the mapping between the Entity\'s attributes and the JSON-LD counterpart, allowing to easily manipulate NGSI-LD properties and always work with Python types.\n\n### Interact with the broker\n\nTwo clients are provided,  `Client` and `AsyncClient` respectively for synchronous and asynchronous modes.\n\nPrefer the synchronous one when working in interactive mode, for example to explore and visualize context data in a Jupyter notebook.\nPrefer the async one if you\'re looking for performance, for example to develop a "real-time" NGSI-LD Agent with a high data-acquisition frequency rate.\n\n\n ## Features\n\n### Build NGSI-LD entities\n- primitives to build properties and relationships (chainable)\n- benefit from uri naming convention, omit scheme and entity\'s type, e.g. `parking = Entity("OffStreetParking", "Downtown1")`\n- support dot-notation facility, e.g. `reliability = parking["availableSpotNumber.reliability"]`\n- easily manipulate a property\'s value, e.g. `reliability.value = 0.8`\n- easily manipulate a property\'s metadata, e.g. `reliability.datasetid = "dataset1"`\n- support nesting\n- support multi-attribute\n- load/save to file\n- load from HTTP\n- load well-known sample entities, e.g.  `parking = Entity.load(SmartDataModels.SmartCities.Parking.OffStreetParking)`\n- provide helpers to ease building some structures, e.g. PostalAddress\n- pretty-print entity and properties\n\n### Wrap the NGSI-LD API\n - synchronous and asynchronous clients\n - support batch operations\n - support pagination : transparently handle pagination (sending as many requests as needed under the hood)\n - support auto-batch : transparently divide into many batch requests if needed\n - support queries and alternate (POST) queries\n - support temporal queries\n - support pandas dataframe as a temporal query result\n - support subscriptions\n - find subscription conflicts\n - SubscriptionBuilder to help build subscriptions\n - auto-detect broker vendor and version\n - support follow relationships (chainable), e.g. `camera = parking.follow("availableSpotNumber.providedBy")`\n\n## Where to get it\n\nThe source code is currently hosted on GitHub at :\nhttps://github.com/Orange-OpenSource/python-ngsild-client\n\nBinary installer for the latest released version is available at the [Python\npackage index](https://pypi.org/project/ngsildclient).\n\n## Installation\n\n**ngsildclient** requires Python 3.9+.\n\n```sh\npip install ngsildclient\n```\n\n## Getting started\n\n### Create our first parking Entity\n\nThe following code snippet builds the `OffstreetParking` sample entity from the ETSI documentation.\n\n```python\nfrom datetime import datetime\nfrom ngsildclient import Entity\n\nPARKING_CONTEXT = "https://raw.githubusercontent.com/smart-data-models/dataModel.Parking/master/context.jsonld"\n\ne = Entity("OffStreetParking", "Downtown1")\ne.ctx.append(PARKING_CONTEXT)\ne.prop("name", "Downtown One")\ne.prop("availableSpotNumber", 121, observedat=datetime(2022, 10, 25, 8)).anchor()\ne.prop("reliability", 0.7).rel("providedBy", "Camera:C1").unanchor()\ne.prop("totalSpotNumber", 200).loc(41.2, -8.5)\n```\n\nLet\'s print the JSON-LD payload.\n\n```python\ne.pprint()\n```\n\n```json\n{\n    "@context": [\n        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",\n        "https://raw.githubusercontent.com/smart-data-models/dataModel.Parking/master/context.jsonld"\n    ],\n    "id": "urn:ngsi-ld:OffStreetParking:Downtown1",\n    "type": "OffStreetParking",\n    "name": {\n        "type": "Property",\n        "value": "Downtown One"\n    },\n    "availableSpotNumber": {\n        "type": "Property",\n        "value": 121,\n        "observedAt": "2022-10-25T08:00:00Z",\n        "reliability": {\n            "type": "Property",\n            "value": 0.7\n        },\n        "providedBy": {\n            "type": "Relationship",\n            "object": "urn:ngsi-ld:Camera:C1"\n        }\n    },\n    "totalSpotNumber": {\n        "type": "Property",\n        "value": 200\n    },\n    "location": {\n        "type": "GeoProperty",\n        "value": {\n            "type": "Point",\n            "coordinates": [\n                -8.5,\n                41.2\n            ]\n        }\n    }\n}\n```\n\n### Persist our parking in the Context Broker\n\nThe following example assumes that an Orion-LD context broker *(w/ TRoE enabled)* is running on localhost.\n\nA docker-compose config [file](https://raw.githubusercontent.com/Orange-OpenSource/python-ngsild-client/master/brokers/orionld/docker-compose-troe.yml) file is provided for that purpose.\n\n```python\nfrom ngsildclient import Client\n\nclient = Client(port=8026, port_temporal=8027)\nclient.create(e)\n```\n\n### Increase our parking occupancy as the day goes on\n\nEach hour five more parkings spots are occupied, until 8 p.m.\n\n```python\nfrom datetime import timedelta\n\nprop = e["availableSpotNumber"]\nfor _ in range(12):\n    prop.observedat += timedelta(hours=1)\n    prop.value -= 10\n    client.update(e)\n```\n\n### Retrieve our parking\n\nGet back our parking from the broker and display it.\n\nOnly one available parking spot remains at 8 p.m.\n\n```python\nparking = client.get("OffStreetParking:Downtown1", ctx=PARKING_CONTEXT)\nparking.pprint()\n```\n\n### Request the Temporal Representation of our parking\n\nFor convenience we retrieve it as a pandas dataframe.\n\n*If you don\'t have pandas installed, just omit the `as_dataframe` argument and get JSON instead.*\n\n```python\ndf = client.temporal.get(e, ctx=PARKING_CONTEXT, as_dataframe=True)\n```\n\nLet\'s close the client and display the last rows.\n\n```python\nclient.close()\ndf.tail()\n```\n\n|    | OffStreetParking   | observed                  |   availableSpotNumber |\n|---:|:-------------------|:--------------------------|----------------------:|\n|  8 | Downtown1          | 2022-10-25 16:00:00+00:00 |                    41 |\n|  9 | Downtown1          | 2022-10-25 17:00:00+00:00 |                    31 |\n| 10 | Downtown1          | 2022-10-25 18:00:00+00:00 |                    21 |\n| 11 | Downtown1          | 2022-10-25 19:00:00+00:00 |                    11 |\n| 12 | Downtown1          | 2022-10-25 20:00:00+00:00 |                     1 |\n\n\n## Documentation\n\nUser guide is available on [Read the Docs](https://ngsildclient.readthedocs.io/en/latest/index.html).\n\nRefer to the [Cookbook](https://ngsildclient.readthedocs.io/en/latest/cookbook.html) chapter that provides many HOWTOs to :\n\n- develop various NGSI-LD Agents collecting data from heterogeneous datasources\n- forge NGSI-LD sample entities from the Smart Data Models initiative\n\n## License\n\n[Apache 2.0](LICENSE)\n',
    'author': 'fbattello',
    'author_email': 'fabien.battello@orange.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Orange-OpenSource/python-ngsild-client',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
