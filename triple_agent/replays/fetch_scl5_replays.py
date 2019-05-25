import os
import random
import re
import zipfile
from shutil import copyfile, rmtree
from time import sleep
from urllib.parse import quote
from urllib.request import urlretrieve

import requests
from bs4 import BeautifulSoup

from triple_agent.utilities.paths import (
    LONG_FILE_HEADER,
    ALL_EVENTS_FOLDER,
    SCL5_REPLAYS_FOLDER,
    TEMP_EXTRACT_FOLDER,
    ZIP_EXTRACT_FOLDER,
)

SCL5_REPLAYS_URL = r"https://s3-us-west-2.amazonaws.com/scl-replays-season5/"


# These are files I suspect were uploaded by both players, or misclassified by SCL Manager
BAD_FILES = {
    "SCL Season 4 - Week 08 - Gold - falconhit vs sharper.zip",
    "SCL Season 4 - Week 10 - Platinum - pires vs cameraman.zip",
    "SCL Season 4 - Week 09 - Platinum - drawnonward vs varanas.zip",
    "SCL Season 5 - Week 06 - Diamond - warningtrack vs cleetose.zip",
    "SCL Season 5 - Week 07 - Platinum - slappydavis vs yerand.zip",
}

SCL_REPLAY_ZIP_RE = re.compile(
    r"^SCL Season . - Week (?P<week>\d+) - (?P<division>\w+) - .*?"
)


def fetch_scl5_replays():
    soup = BeautifulSoup(requests.get(SCL5_REPLAYS_URL).text, "xml")

    existing_zip_files = os.listdir(ZIP_EXTRACT_FOLDER)

    new_zip_file_matches = []

    for key in soup.ListBucketResult.find_all("Key"):
        if key.text not in BAD_FILES:
            if key.text not in existing_zip_files:
                filename_match = SCL_REPLAY_ZIP_RE.match(key.text)
                if filename_match is None:
                    print(key.text)
                    raise ValueError

                new_zip_file_matches.append(filename_match)

    for zip_file_match in new_zip_file_matches:
        zip_file_dest = os.path.join(ZIP_EXTRACT_FOLDER, zip_file_match.string)

        extract_folder = os.path.join(
            SCL5_REPLAYS_FOLDER,
            zip_file_match.group("division"),
            zip_file_match.group("week").lstrip("0"),
        )

        print(
            zip_file_match.string,
            zip_file_match.group("division"),
            zip_file_match.group("week"),
        )
        sleep(random.randint(2, 4))
        urlretrieve(SCL5_REPLAYS_URL + quote(zip_file_match.string), zip_file_dest)

        os.makedirs(extract_folder, exist_ok=True)
        try:
            rmtree(TEMP_EXTRACT_FOLDER)
        except FileNotFoundError:
            pass
        os.makedirs(TEMP_EXTRACT_FOLDER, exist_ok=True)

        try:
            zip_ref = zipfile.ZipFile(zip_file_dest, "r")
        except zipfile.BadZipFile as this_exep:
            print(zip_file_dest)
            raise this_exep

        zip_ref.extractall(TEMP_EXTRACT_FOLDER)

        for root, _, files in os.walk(TEMP_EXTRACT_FOLDER):
            for file in files:
                if file.endswith(".replay"):
                    copyfile(
                        LONG_FILE_HEADER + os.path.join(root, file),
                        LONG_FILE_HEADER + os.path.join(extract_folder, file),
                    )

        zip_ref.close()
        rmtree(TEMP_EXTRACT_FOLDER)


def check_for_duplicate_files():
    found_dict = dict()

    for root, _, files in os.walk(ALL_EVENTS_FOLDER):
        if root != ALL_EVENTS_FOLDER:
            for file in files:
                if file.endswith(".replay"):
                    if file not in found_dict.keys():
                        found_dict[file] = root
                    else:
                        print(
                            "XXX",
                            file,
                            os.path.relpath(ALL_EVENTS_FOLDER, root),
                            os.path.relpath(ALL_EVENTS_FOLDER, found_dict[file]),
                        )


if __name__ == "__main__":
    fetch_scl5_replays()
    check_for_duplicate_files()
