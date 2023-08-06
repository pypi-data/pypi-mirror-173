# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_byo_react', 'django_byo_react.templatetags']

package_data = \
{'': ['*'], 'django_byo_react': ['templates/django_byo_react/includes/*']}

install_requires = \
['Django>=3.2']

setup_kwargs = {
    'name': 'django-byo-react',
    'version': '0.2.3',
    'description': 'A template tag to create a div and json script tag for react to bind to',
    'long_description': '# Django BYO React\n\nA minimal template tag which creates a div element for React to bind to and a Django `json_script` which can be used to pass values from Django into the root React element as props. This library remains unopinionated about the React code by design since there are so many ways to create and maintain React apps.\n\n## Usage\n\nInstall the app in `settings.py`\n\n```python\nINSTALLED_APPS = [\n    "django_byo_react",\n    ...\n]\n```\n\nIn the template that you want to install a react app load the tag and use it with the given `kwargs`. You can add extra props to the root react component by adding `kwargs` to the tag element. As long as is json serializable it can be included in the props.\n\n```django\n{% load byo_react %}\n\n"{% byo_react id=\'react-app-id\' className=\'w-100\' showActive=True %}"\n```\n\n### Javascript/Typescript Example\n\nThe JS/TS side is left to the user as there are many ways in which one can create a react app. This leaves the most flexibility to integrate existing react apps and frameworks into a django page. The one important point is that the `id` is the variable that ties the backend to the frontend so keep this in sync.\n\nHere is a typical example for a very basic app.\n\n```typescript\nimport React, { FC } from "react";\nimport ReactDOM from \'react-dom/client\';\n\n// Example root component for a react app\nconst App: FC = (props) => <div {...props}></div>\n\nconst elementId = "react-element-id"\n\nconst container = document.getElementById(elementId)\nif (!container) throw new Error(`Can\'t find element with id ${elementId}`);\n\n// Extract props from the django json_script tag\nconst jsonContent = document.getElementById(container.dataset?.scriptId)?.textContent;\nif (!jsonContent) throw new Error("No associated script found");\n\n// props will be a dictionary containing the tag kwargs\n// eg: The props constant will be an object with { showActive: true }\nconst props = JSON.parse(jsonContent);\n\nconst root = ReactDOM.createRoot(container)\nroot.render(<App {...props} />);\n```',
    'author': 'lukewiwa',
    'author_email': 'luke.wiwa@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lukewiwa/django-byo-react',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
