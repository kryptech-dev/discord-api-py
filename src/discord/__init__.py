import urllib
import json
import base64

import requests

from models.guild import Guild

class Discord():

    def __init__(self, client_id=None, secret=None, token=None, version=9):
        self.client_id = client_id
        self.secret = secret
        self.token = token
        self.version = version

    @property
    def base_url(self):
        return f"https://discord.com/api/v{self.version}"

    def _get_headers(self):
        return  {
            "Authorization": f"Bot {self.token}"
        }

    def get(self, url, params=None, headers=None, **kwargs):
        headers = headers if headers is not None else {}
        headers.update(self._get_headers())

        return requests.get(self.base_url + url, params=params, headers=headers, **kwargs)

    def post(self, url, data=None, json=None, headers=None, **kwargs):
        headers = headers if headers is not None else {}
        headers.update(self._get_headers())

        return requests.post(self.base_url + url, data=data, json=json, headers=headers, **kwargs)

    def put(self, url, data=None, json=None, headers=None, **kwargs):
        headers = headers if headers is not None else {}
        headers.update(self._get_headers())

        return requests.put(self.base_url + url, data=data, json=json, headers=headers, **kwargs)

    def delete(self, url, data=None, json=None, headers=None, **kwargs):
        headers = headers if headers is not None else {}
        headers.update(self._get_headers())

        return requests.delete(self.base_url + url, data=data, json=json, headers=headers, **kwargs)

    def get_oauth2(self, scopes, redirect_url):
        return OAuth2(self, scopes, redirect_url)

    def get_guild(self, guild_id):
        return Guild.get(self, guild_id)

class OAuth2():

    def __init__(self, discord, scopes, redirect_url):
        self.discord = discord
        self.scopes = scopes
        self.redirect_url = redirect_url

    @property
    def base_url(self):
        return "https://discord.com/api/oauth2"

    def get_authorize_url(self, state=None):
        state = state if state is not None else {}

        state_data = json.dumps(state)
        state_enc = state_data.encode("utf-8")
        state_string = base64.b64encode(state_enc)

        params = {
            "response_type": "code",
            "client_id": self.discord.client_id,
            "scope": self.scopes,
            "redirect_uri": self.redirect_url,
            "state": state_string
        }
        params_string = urllib.parse.urlencode(params)
        return f"{self.base_url}/authorize?{params_string}"

    def exchange_code(self, code, state=None):
        data = {
            "client_id": self.discord.client_id,
            "client_secret": self.discord.secret,
            "grant_type": "authorization_code",
            "code": code,
            "scope": self.scopes,
            "redirect_uri": self.redirect_uri
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.posts(self.base_url + "/token", data=data, headers=headers)

        if state is not None:
            state_enc = base64.b64decode(state)
            state_data = state_enc.decode("utf-8")
            state = json.loads(state_data)

        return response.json(), state