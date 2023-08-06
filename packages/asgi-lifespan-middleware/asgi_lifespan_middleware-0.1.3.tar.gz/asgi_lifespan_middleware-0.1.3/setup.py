# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asgi_lifespan_middleware']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'asgi-lifespan-middleware',
    'version': '0.1.3',
    'description': 'Middleware to handle ASGI lifespans',
    'long_description': '# asgi-lifespan-middleware\n\nASGI middlewate to support ASGI lifespans using a simple async context manager interface.\n\nThis middleware accepts an ASGI application to wrap and an async context manager lifespan.\nIt will run both the lifespan it was handed directly and that of the ASGI app (if the wrapped ASGI app supports lifespans).\n\n## Example (Starlette)\n\nStarlette apps already support lifespans so we\'ll just be using the TestClient against a plain ASGI app that does nothing.\n\n```python\nfrom contextlib import asynccontextmanager\nfrom typing import AsyncIterator\n\nfrom starlette.testclient import TestClient\nfrom starlette.types import ASGIApp, Scope, Send, Receive\n\nfrom asgi_lifespan_middleware import LifespanMiddleware\n\n@asynccontextmanager\nasync def lifespan(\n    # you\'ll get the wrapped app injected\n    app: ASGIApp,\n) -> AsyncIterator[None]:\n    print("setup")\n    yield\n    print("teardown")\n\n\nasync def app(scope: Scope, receive: Receive, send: Send) -> None:\n    ...  # do nothing\n\n\nwrapped_app = LifespanMiddleware(\n    app,\n    lifespan=lifespan,\n)\n\nwith TestClient(wrapped_app):\n    pass\n```\n',
    'author': 'Adrian Garcia Badaracco',
    'author_email': 'adrian@adriangb.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/adriangb/asgi-lifespan-middleware',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
