# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src',
 'generated': 'generated/generated',
 'generated.openapi_client': 'generated/generated/openapi_client',
 'generated.openapi_client.api': 'generated/generated/openapi_client/api',
 'generated.openapi_client.apis': 'generated/generated/openapi_client/apis',
 'generated.openapi_client.model': 'generated/generated/openapi_client/model',
 'generated.openapi_client.models': 'generated/generated/openapi_client/models',
 'generated.test': 'generated/generated/test'}

packages = \
['generated',
 'generated.openapi_client',
 'generated.openapi_client.api',
 'generated.openapi_client.apis',
 'generated.openapi_client.model',
 'generated.openapi_client.models',
 'generated.test',
 'groundlight']

package_data = \
{'': ['*'], 'generated': ['.openapi-generator/*', 'docs/*']}

install_requires = \
['certifi>=2021.10.8,<2022.0.0',
 'frozendict>=2.3.2,<3.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'urllib3>=1.26.9,<2.0.0']

setup_kwargs = {
    'name': 'groundlight',
    'version': '0.5.3',
    'description': 'Build computer vision systems from natural language with Groundlight',
    'long_description': '# Groundlight Python SDK\n\nGroundlight makes it simple to understand images.  You can easily create computer vision detectors just by describing what you want to know using natural language.\n\n**How does it work?**  Your images are first analyzed by machine learning (ML) models which are automatically trained on your data.  If those models have high enough confidence, that\'s your answer.  But if the models are unsure, then the images are progressively escalated to more resource-intensive analysis methods up to real-time human review.  So what you get is a computer vision system that starts working right away without even needing to first gather and label a dataset.  At first it will operate with high latency, because people need to review the image queries.  But over time, the ML systems will learn and improve so queries come back faster with higher confidence.\n\n*Note: The SDK is currently in "beta" phase.  Interfaces are subject to change in future versions.*\n\n\n## Simple Example\n\nHow to build a computer vision system in 5 lines of python code:\n\n```Python\nfrom groundlight import Groundlight\ngl = Groundlight()\nd = gl.create_detector("door", query="Is the door open?")  # define with natural language\nimage_query = gl.submit_image_query(detector=d, image="path/filename.jpeg")  # send an image\nprint(f"The answer is {image_query.result}")  # get the result\n```\n\n\n## Getting Started\n\n1. Install the `groundlight` SDK.  Requires python version 3.7 or higher.  See [prerequisites](#Prerequisites).\n\n    ```Bash\n    $ pip3 install groundlight\n    ```\n\n1. To access the API, you need an API token. You can create one on the\n   [groundlight web app](https://app.groundlight.ai/reef/my-account/api-tokens).\n\nThe API token should be stored securely.  You can use it directly in your code to initialize the SDK like:\n\n```python\ngl = Groundlight(api_token="<YOUR_API_TOKEN>")\n```\n\nwhich is an easy way to get started, but is NOT a best practice.  Please do not commit your API Token to version control!  Instead we recommend setting the `GROUNDLIGHT_API_TOKEN` environment variable outside your code so that the SDK can find it automatically.\n\n```bash\n$ export GROUNDLIGHT_API_TOKEN=api_2GdXMflhJi6L_example\n$ python3 glapp.py\n```\n\n\n## Prerequisites\n\n### Using Groundlight SDK on Ubuntu 18.04\n\nUbuntu 18.04 still uses python 3.6 by default, which is end-of-life.  We recommend setting up python 3.8 as follows:\n\n```\n# Prepare Ubuntu to install things\nsudo apt-get update\n# Install the basics\nsudo apt-get install -y python3.8 python3.8-distutils curl\n# Configure `python3` to run python3.8 by default\nsudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 10\n# Download and install pip3.8\ncurl https://bootstrap.pypa.io/get-pip.py > /tmp/get-pip.py\nsudo python3.8 /tmp/get-pip.py\n# Configure `pip3` to run pip3.8\nsudo update-alternatives --install /usr/bin/pip3 pip3 $(which pip3.8) 10\n# Now we can install Groundlight!\npip3 install groundlight\n```\n\n## Using Groundlight on the edge\n\nStarting your model evaluations at the edge reduces latency, cost, network bandwidth, and energy. Once you have downloaded and installed your Groundlight edge models, you can configure the Groundlight SDK to use your edge environment by configuring the \'endpoint\' to point at your local environment as such:\n\n```Python\nfrom groundlight import Groundlight\ngl = Groundlight(endpoint="http://localhost:6717")\n```\n\n(Edge model download is not yet generally available.)\n\n## Advanced\n\n### Retrieve an existing detector\n\n```Python\ndetector = gl.get_detector(id="YOUR_DETECTOR_ID")\n```\n\n### List your detectors\n\n```Python\n# Defaults to 10 results per page\ndetectors = gl.list_detectors()\n\n# Pagination: 3rd page of 25 results per page\ndetectors = gl.list_detectors(page=3, page_size=25)\n```\n\n### Retrieve an image query\n\nIn practice, you may want to check for a new result on your query. For example, after a cloud reviewer labels your query. For example, you can use the `image_query.id` after the above `submit_image_query()` call.\n\n```Python\nimage_query = gl.get_image_query(id="YOUR_IMAGE_QUERY_ID")\n```\n\n### List your previous image queries\n\n```Python\n# Defaults to 10 results per page\nimage_queries = gl.list_image_queries()\n\n# Pagination: 3rd page of 25 results per page\nimage_queries = gl.list_image_queries(page=3, page_size=25)\n```\n\n### Handling HTTP errors\n\nIf there is an HTTP error during an API call, it will raise an `ApiException`. You can access different metadata from that exception:\n\n```Python\nfrom groundlight import ApiException, Groundlight\n\ngl = Groundlight()\ntry:\n    detectors = gl.list_detectors()\nexcept ApiException as e:\n    print(e)\n    print(e.args)\n    print(e.body)\n    print(e.headers)\n    print(e.reason)\n    print(e.status)\n```\n\n',
    'author': 'Groundlight AI',
    'author_email': 'support@groundlight.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://groundlight.ai',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0',
}


setup(**setup_kwargs)
