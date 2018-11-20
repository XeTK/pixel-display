from json import loads

from requests import request

from process_image import open_image
from spotify_auth import SpotifyAuth
from download import get_image
from web_server import setup_rest_endpoint

SPOTIFY_NOW_PLAYING_URL = "https://api.spotify.com/v1/me/player/currently-playing"


def get_current_playing(auth_token):
    headers = {
        'Authorization': "Bearer " + auth_token,
        'cache-control': "no-cache"
    }

    response = request("GET", SPOTIFY_NOW_PLAYING_URL, headers=headers)

    return loads(response.text)


def get_album_art_url(users_currently_playing):
    array_of_album_art = users_currently_playing['item']['album']['images']
    index_of_smallest = len(array_of_album_art) -1
    album_art_64 = array_of_album_art[index_of_smallest]
    album_art_64_url = album_art_64['url']

    return album_art_64_url


def main_after_auth(auth_token):
    users_currently_playing = get_current_playing(auth_token)

    if users_currently_playing is not None:
        art_url = get_album_art_url(users_currently_playing)
        local_path = get_image(art_url)
        print(local_path)

        return open_image(local_path)

    return "BROKEN"


def setup_rest_resource(auth_token):
    setup_rest_endpoint(main_after_auth, auth_token)


def main():
    spotify_auth = SpotifyAuth(setup_rest_resource)
    spotify_auth.main()


main()
