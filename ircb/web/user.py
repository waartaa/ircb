# -*- coding: utf-8 -*-
import asyncio
import json

from aiohttp import web
from aiohttp_auth import auth

from ircb.storeclient import UserStore
from ircb.web.decorators import auth_required
from ircb.web.constants import STATUS_OK
from ircb.forms.user import UserForm


class SignupView(web.View):
    """
    .. http:post:: /api/v1/signup/

        :string username: **Required**. The username of the user.
        :string email: **Required**. The email of the user.
        :string password: **Required**. The password of the user.
        :string first_name: The first name of the user.
        :string last_name: The last name of the user.
    """

    async def post(self):
        username = await auth.get_auth(self.request)
        if username:
            raise web.HTTPForbidden()
        data = await self.request.post()
        form = UserForm(formdata=data)
        form.validate()
        await self._validate_username(form)
        await self._validate_email(form)
        if form.errors:
            return web.Response(body=json.dumps(form.errors).encode(),
                                status=400,
                                content_type='application/json')
        cleaned_data = form.data
        user = await UserStore.create(
            dict(
                username=cleaned_data['username'],
                email=cleaned_data['email'],
                password=cleaned_data.get('password', ''),
                first_name=cleaned_data.get('first_name', ''),
                last_name=cleaned_data.get('last_name', '')
            )
        )
        resp = {
            'status': STATUS_OK,
            'content_type': 'application/json',
            'charset': 'utf-8',
        }

        resp.update({'body': json.dumps({
            'username': user.username,
            'access_token': user.access_token,
        }).encode()})

        return web.Response(**resp)

    async def _validate_username(self, form):
        username = form.username.data
        users = await UserStore.get(
            dict(query=('username', username)))
        if users:
            error_msg = 'Username already in use.'
            form.username.errors.append(error_msg)

    async def _validate_email(self, form):
        email = form.email.data
        users = await UserStore.get(
            dict(query=('email', email)))
        if users:
            error_msg = 'Email already in use.'
            form.email.errors.append(error_msg)


class SigninView(web.View):
    """
    .. http:post:: /api/v1/signin/

        :string username: **Required**. The username of the user.
        :string password: **Required**. The password of the user.

        If the header contains the `access_token` then password is not
        required.
    """

    async def post(self):
        token = self.request.headers.get('Authorization')

        data = await self.request.post()
        username = data.get('username')
        password = data.get('password')

        if password is None and token is None:
            raise web.HTTPForbidden()

        if password is not None:
            user = await UserStore.get(
                dict(query=('auth',
                            (username, password))
                )
            )
        elif access_token is not None:
            user = await UserStore.get(
                dict(query=('auth',
                            (username, access_token))
                )
            )

        if user:
            await auth.remember(self.request, user.username)
            return web.Response(body=b'OK')
        raise web.HTTPForbidden()


class SignoutView(web.View):

    @auth_required
    @asyncio.coroutine
    def post(self):
        yield from auth.forget(self.request)
        return web.Response(body=b'OK')
