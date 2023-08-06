# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['doT']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dot-js-py',
    'version': '0.0.1',
    'description': 'A python implementation of the famous js template engine. doT.js.',
    'long_description': 'doT.py\n======\n\nA python implementation of the famous js template engine. doT.js. http://olado.github.io/doT/index.html.\nIt do excetly the same thing as doT.js except written in python. Thus, it can be used in python web framework.\n\ndoT.py compile the template to a pure javascript function in server side; therefore client side can evaluate the template later without any dependency. Which means it saves the time for client to load template engine and to load template file. In short, doT.py allows using client side template tech without include a template engine in client side.\n\n## Installation\n\n`pip install doT.py`\n\n### Here is an example:\n\n#### Use client side template\n\n```html\n<html>\n<!-- load template engine -->\n<script type="text/javascript" src="doT.js"></script>\n<div id="container">\n<script type="text/javascript">\n     // Compile template function\n     var tempFn = doT.template("<h1>Here is a sample template {{=it.foo}}</h1>");\n     var resultText = tempFn({foo: \'with doT\'});\n     document.getElementById(\'container\').innerHtml = resultText;\n</script>\n</html>\n```\n\n#### Use doT.py, you write:\n```html\n<html>\n<!-- without loading template engine -->\n<div id="container">\n<script type="text/javascript">\n     // Compile template function\n     var tempFn = {{ js_template(\'<h1>Here is a sample template {{=it.foo}}</h1>\') }};\n     var resultText = tempFn({foo: \'with doT\'});\n     document.getElementById(\'container\').innerHtml = resultText;\n</script>\n</html>\n```\n\n#### it will automatically compiled to\n```html\n<html>\n<!-- without loading template engine -->\n<div id="container">\n<script type="text/javascript">\n     // Compile template function\n     var tempFn = function anonymous(it) { var out=\'"<h1>Here is a sample template \'+(it.foo)+\'</h1>"\';return out; };\n     var resultText = tempFn({foo: \'with doT\'});\n     document.getElementById(\'container\').innerHtml = resultText;\n</script>\n</html>\n```\n\nDjango Support:\n\nJinja2 Support:\n\nCommandline Support:\n',
    'author': 'lucemia',
    'author_email': 'lucemia@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7',
}


setup(**setup_kwargs)
