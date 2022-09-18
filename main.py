"""A Python script that directly downloads Pandas documentation and create a twin directory by
replacing each group of text by a new group of text with a 1 between each element of the string."""

__author__ = "Yacine BOUKARI"
__email__ = "steeveboukari9@gmail.com"
__version__ = "0.1.0"

# Built-in imports
import urllib.request
from zipfile import ZipFile
import ssl
import os
import shutil
import pathlib
from typing import TypeVar, List, Tuple

# Other libraries imports
from bs4 import BeautifulSoup
from tqdm import tqdm

# Custom type for file's path
PathLike = TypeVar('PathLike', str, pathlib.Path)


def download_file() -> int:
    """This function downloads the zip file targeted by URL,
    and saves it in the current directory.

    Returns:
        int: The status of the download request.
            See https://www.w3.org/Protocols/HTTP/HTRESP.html for further information.
    """

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    with urllib.request.urlopen(URL, context=ssl_context) as response:
        with open(ZIP_FILE_PATH, "wb") as zip_file:
            print(f"\nDownloading '{ZIP_FILE_NAME}' ...")

            for element in tqdm(response):
                zip_file.write(element)

            print(f"'{ZIP_FILE_NAME}' downloaded !")

    return response.status


def unzip_file() -> int:
    """Unzip the zip file targeted by ZIP_FILE_PATH in the directory targeted by DIR_PATH

    Returns:
        int: The size of the unzipped directory in bytes.
    """

    print(f"\nUnzipping '{ZIP_FILE_NAME}' ...")

    with ZipFile(ZIP_FILE_PATH, "r") as zip_file:
        zip_file.extractall(DIR_PATH)

    print(f"'{ZIP_FILE_NAME} unzipped !")

    return os.stat(DIR_PATH).st_size


def get_files() -> List[Tuple[PathLike, PathLike]]:
    """The function explores the DIR_PATH and find every file in it (subdirectories included)

    It also creates a clone directory at TWIN_DIR_PATH.

    Returns:
        List[Tuple[PathLike, PathLike]]: A list of tuples of absolute path for
        each file in the directory targeted by DIR_PATH, with their corresponding in TWIN_DIR_PATH
    """

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
    """For each file in DIR_PATH:
        - modify it if it is an .html file
        - does nothing if not
    then copy it to TWIN_DIR_PATH.

    For the modification, each text content is replaced by inserting 1s between characters.

    Returns:
        int: The number of files successfully copied.
    """

    copied = 0

    print(f"\nProcessing files from '{DIR_ABSOLUTE_PATH}' to '{TWIN_DIR_ABSOLUTE_PATH}' ...")

    for file_path, new_file_path in tqdm(get_files()):

        if file_path[-5:] == ".html":

            with open(file_path, "r", encoding="utf-8") as file:
                with open(new_file_path, "w", encoding="utf-8") as new_file:
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
    URL = "https://pandas.pydata.org/docs/pandas.zip"
    ZIP_FILE_PATH = "./pandas.zip"
    ZIP_FILE_NAME = "pandas.zip"
    DIR_PATH = "./pandas/"
    TWIN_DIR_PATH = "./twin/"
    DIR_ABSOLUTE_PATH = os.path.abspath(DIR_PATH)
    TWIN_DIR_ABSOLUTE_PATH = os.path.abspath(TWIN_DIR_PATH)

    print()
    print(" HTML to H1T1M1L ".center(50, "="))
    print("\n\nPlease make sure you have at least 500Mb free space in the current directory.")
    input("\nPress 'Enter' to continue: ")
    print("Download status:", download_file())
    print("File size:", unzip_file())
    print(process_files(), "files copied")
    print("\nDone!\n")
    print(" BYE ".center(50, "="))
    print()
