import asyncio
import json

from aiohttp import web
from aiohttp_auth import auth

from ircb.storeclient import UserStore
from ircb.web.decorators import auth_required
from ircb.forms.user import UserForm


class SignupView(web.View):

    @asyncio.coroutine
    def post(self):
        username = yield from auth.get_auth(self.request)
        if username:
            raise web.HTTPForbidden()
        data = yield from self.request.post()
        form = UserForm(formdata=data)
        form.validate()
        yield from self._validate_username(form)
        yield from self._validate_email(form)
        if form.errors:
            return web.Response(body=json.dumps(form.errors).encode(),
                                status=400,
                                content_type='application/json')
        cleaned_data = form.data
        yield from UserStore.create(
            dict(
                username=cleaned_data['username'],
                email=cleaned_data['email'],
                password=cleaned_data['password'],
                first_name=cleaned_data.get('first_name', ''),
                last_name=cleaned_data.get('last_name', '')
            )
        )
        return web.Response(body=b'OK')

    def _validate_username(self, form):
        username = form.username.data
        users = yield from UserStore.get(
            dict(query=('username', username)))
        if users:
            error_msg = 'Username already in use.'
            form.username.errors.append(error_msg)

    def _validate_email(self, form):
        email = form.email.data
        users = yield from UserStore.get(
            dict(query=('email', email)))
        if users:
            error_msg = 'Email already in use.'
            form.email.errors.append(error_msg)


class SigninView(web.View):

    @asyncio.coroutine
    def post(self):
        data = yield from self.request.post()
        user = yield from UserStore.get(
            dict(query=('auth', (data.get('username'), data.get('password'))))
        )
        if user:
            yield from auth.remember(self.request, user.username)
            return web.Response(body=b'OK')
        raise web.HTTPForbidden()


class SignoutView(web.View):

    @auth_required
    @asyncio.coroutine
    def post(self):
        yield from auth.forget(self.request)
        return web.Response(body=b'OK')
