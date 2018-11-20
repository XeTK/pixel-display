from pathlib import Path

from urllib.request import urlretrieve

CACHE_FOLDER = './image_cache'


def setup():
    cache_folder = Path(CACHE_FOLDER)
    if not cache_folder.is_dir():
        cache_folder.mkdir(parents=True)


def get_filename_from_url(url):
    return url.rsplit('/', 1)[-1]


def file_path(filename):
    return CACHE_FOLDER + '/' + filename


def check_file_exists(filename):
    file = Path(file_path(filename))
    return file.is_file()


def download_image(url):
    filename = get_filename_from_url(url)

    print("Downloading: " + filename)

    urlretrieve(url, file_path(filename))


def get_image(url):
    setup()

    filename = get_filename_from_url(url)

    if not check_file_exists(filename):
        download_image(url)

    return file_path(filename)
