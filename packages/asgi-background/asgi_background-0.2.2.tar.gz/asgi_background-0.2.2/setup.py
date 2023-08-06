# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asgi_background']

package_data = \
{'': ['*']}

install_requires = \
['anyio>=3.6.1', 'asgi-lifespan-middleware>=0.1.3']

extras_require = \
{':python_version < "3.10"': ['typing-extensions>=4.2.0']}

setup_kwargs = {
    'name': 'asgi-background',
    'version': '0.2.2',
    'description': 'Background tasks for any ASGI web framework',
    'long_description': '# asgi-background\n\nBackground tasks for any ASGI framework.\n\n## Example (Starlette)\n\n```python\nfrom asgi_background import BackgroundTaskMiddleware, BackgroundTasks\nfrom starlette.applications import Starlette\nfrom starlette.middleware import Middleware\nfrom starlette.requests import Request\nfrom starlette.responses import Response\nfrom starlette.routing import Route\n\n\nasync def task(num: int) -> None:\n    await anyio.sleep(1)\n    print(num)\n\n\nasync def endpoint(request: Request) -> Response:\n    tasks = BackgroundTasks(request.scope)\n    await tasks.add_task(task, 1)\n    return Response()\n\n\napp = Starlette(\n    routes=[Route("/", endpoint)],\n    middleware=[Middleware(BackgroundTaskMiddleware)]\n)\n```\n\n## Execution\n\nUnlike Starlette, we do not execute background tasks within the ASGI request/response cycle.\nInstead we schedule them in a `TaskGroup` that is bound to the application\'s lifespan.\nThe only guarantee we make is that background tasks will not block (in the async sense, not the GIL sense) sending the response and that we will (try) to wait for them to finish when the application shuts down.\nJust like with Starlette\'s background tasks, you should only use these for short lived tasks, they are not a durable queuing mechanisms like Redis, Celery, etc.\nFor context, the default application shutdown grace period in Kubernetes is 30 seconds, so 30 seconds is probably about as long as you should allow your tasks to run.\n',
    'author': 'Adrian Garcia Badaracco',
    'author_email': 'adrian@adriangb.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/adriangb/asgi-background',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
