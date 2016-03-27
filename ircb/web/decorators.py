from functools import wraps
from aiohttp import web
from aiohttp_auth.auth import get_auth


def auth_required(func):
    """
    Fix to make auth_required func with class based views.

    Utility decorator that checks if a user has been authenticated for this
    request.

    Allows views to be decorated like:

        @auth_required
        def view_func(request):
            pass

    providing a simple means to ensure that whoever is calling the function has
    the correct authentication details.

    Args:
        func: Function object being decorated and raises HTTPForbidden if not

    Returns:
        A function object that will raise web.HTTPForbidden() if the passed
        request does not have the correct permissions to access the view.
    """
    @wraps(func)
    async def wrapper(*args):
        if isinstance(args[0], web.View):
            request = args[0].request
        else:
            request = args[-1]
        if (await get_auth(request)) is None:
            raise web.HTTPForbidden()

        return await func(*args)

    return wrapper

