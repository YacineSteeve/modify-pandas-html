import urllib.request
import zipfile
from bs4 import BeautifulSoup
import ssl
import os
import shutil
import pathlib
from tqdm import tqdm
from typing import TypeVar, List, Tuple

URL = "https://pandas.pydata.org/docs/pandas.zip"
ZIP_FILE_PATH = "./pandas.zip"
ZIP_FILE_NAME = "pandas.zip"
DIR_PATH = "./pandas/"
TWIN_DIR_PATH = "./twin/"
DIR_ABSOLUTE_PATH = os.path.abspath(DIR_PATH)
TWIN_DIR_ABSOLUTE_PATH = os.path.abspath(TWIN_DIR_PATH)
TPathLike = TypeVar('TPathLike', str, pathlib.Path)


def download_file() -> int:
    global URL, ZIP_FILE_PATH, ZIP_FILE_NAME

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    with urllib.request.urlopen(URL, context=ssl_context) as response:
        with open(ZIP_FILE_PATH, "wb") as zip_file:
            print(f"\nDownloading '{ZIP_FILE_NAME}' ...")

            for element in response:
                zip_file.write(element)

            print(f"'{ZIP_FILE_NAME}' downloaded !")

    return response.status


def unzip_file() -> int:
    global ZIP_FILE_PATH, ZIP_FILE_NAME, DIR_PATH

    print(f"\nUnzipping '{ZIP_FILE_NAME}' ...")

    zip_file = zipfile.ZipFile(ZIP_FILE_PATH)
    zip_file.extractall(DIR_PATH)

    print(f"'{ZIP_FILE_NAME} unzipped !")

    return os.stat(DIR_PATH).st_size


def get_files() -> List[Tuple[TPathLike, TPathLike]]:
    global DIR_PATH, TWIN_DIR_PATH

    files = []

    for current_dir_path, _, filenames in os.walk(DIR_PATH):
        new_dir_path = os.path.join(TWIN_DIR_PATH, current_dir_path[len(DIR_PATH):])

        try:
            os.mkdir(new_dir_path)
        except FileExistsError:
            print(f"\nError: '{new_dir_path}' already exists !"
                  f"\nPlease delete the existing directory first and try again.")
            break

        for filename in filenames:
            files.append((
                os.path.join(current_dir_path, filename),
                os.path.join(new_dir_path, filename)
            ))

    return files


def process_files() -> int:
    global DIR_ABSOLUTE_PATH, TWIN_DIR_ABSOLUTE_PATH

    copied = 0

    print(f"\nModifying and copying files from '{DIR_ABSOLUTE_PATH}' to '{TWIN_DIR_ABSOLUTE_PATH}' ...")

    for file_path, new_file_path in tqdm(get_files()):

        if file_path[-5:] == ".html":

            with open(file_path, "r") as file:
                with open(new_file_path, "w") as new_file:
                    soup = BeautifulSoup(file.read(), 'html.parser')
                    tags = soup.find_all(recursive=True, text=True)

                    for tag in tags:
                        if tag.string is not None:
                            tag.string.replace_with("1".join(list(tag.string)))

                    new_file.write(soup.prettify(formatter='html'))

        else:
            shutil.copyfile(file_path, new_file_path)

        copied += 1

    print("Copy finished !")

    return copied


if __name__ == "__main__":
    print(" HTML to H1T1M1L ".center(50, "="))
    print("\n\nPlease make sure you have at least 500Mb free space in the current directory.")
    input("\nPress 'Enter' to continue: ")
    print("Download status:", download_file())
    print("File size:", unzip_file())
    print(process_files(), "files copied")
    print("\nDone!\n")
    print(" BYE ".center(62, "="))
