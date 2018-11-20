from pathlib import Path

from base64 import b64encode
from json import loads
from yaml import load

from requests import request

from callback_web_server import setup_return_endpoint

CONFIG_FILE = "config.yaml"
REFRESH_TOKEN_FILE = "refresh_token.txt"

AUTHORIZATION_CODE_REQUEST = "authorization_code"
REFRESH_TOKEN_REQUEST = "refresh_token"


ACCESS_TOKEN_URL = "https://accounts.spotify.com/api/token"


config_file = open(CONFIG_FILE, 'r')
config = load(config_file)


CLIENT_ID = config['CLIENT_ID']
CLIENT_SECRET = config['CLIENT_SECRET']
CALLBACK_URL = config['CALLBACK_URL']
PORT = config['PORT']
DEBUG = config['DEBUG'] == "True"


ACCOUNT_URL = "https://accounts.spotify.com/authorize?client_id=" + CLIENT_ID + "&response_type=code&redirect_uri=" + CALLBACK_URL + "&scope=user-read-currently-playing"


def basic_auth_gen(user, password):
    pre_string = user + ':' + password
    bytes_string = pre_string.encode()
    encode_bytes = b64encode(bytes_string)
    return encode_bytes.decode("utf-8")


def get_tokens(request_type, user, password, auth_code=None, refresh_token=None):
    basic_auth_string = basic_auth_gen(user, password)

    payload = "grant_type=" + request_type + "&redirect_uri=" + CALLBACK_URL

    if auth_code is not None:
        payload += "&code=" + auth_code

    if refresh_token is not None:
        payload += "&refresh_token=" + refresh_token

    headers = {
        'Authorization': "Basic " + basic_auth_string,
        'Content-Type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache"
    }

    response = request('POST', ACCESS_TOKEN_URL, data=payload, headers=headers)

    return loads(response.text)


def get_access_token(auth_code):
    json_struct = get_tokens(
        AUTHORIZATION_CODE_REQUEST,
        CLIENT_ID,
        CLIENT_SECRET,
        auth_code=auth_code
    )

    refresh_token = json_struct['refresh_token']

    write_refresh_token(refresh_token)

    return json_struct['access_token']


def get_access_token_on_refresh():
    refresh_token = read_refresh_token()

    json_struct = get_tokens(
        REFRESH_TOKEN_REQUEST,
        CLIENT_ID,
        CLIENT_SECRET,
        refresh_token=refresh_token
    )

    return json_struct['access_token']


def read_refresh_token():
    refresh_token_file = open(REFRESH_TOKEN_FILE, 'r')
    refresh_token = refresh_token_file.read()
    refresh_token_file.close()
    return refresh_token


def write_refresh_token(auth_token):
    refresh_token_file = open(REFRESH_TOKEN_FILE, 'w')
    refresh_token_file.write(auth_token)
    refresh_token_file.close()


class SpotifyAuth:
    def __init__(self, main_after_auth):
        self.main_after_auth = main_after_auth

    def continue_after_external_auth(self, auth_code):
        auth_token = get_access_token(auth_code)
        self.main_after_auth(auth_token)

    def main(self):
        refresh_token_file = Path(REFRESH_TOKEN_FILE)
        if refresh_token_file.is_file():
            auth_token = get_access_token_on_refresh()

            self.main_after_auth(auth_token)
        else:
            print(ACCOUNT_URL)
            setup_return_endpoint(PORT, DEBUG, self.continue_after_external_auth)
