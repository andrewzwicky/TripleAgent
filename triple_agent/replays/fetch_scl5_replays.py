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
)

ZIPS_FOLDER = "ZIPS"
TEMP_FOLDER = "TEMP"

SCL5_REPLAYS_URL = r"https://s3-us-west-2.amazonaws.com/scl-replays-season5/"


# These are files I suspect were uploaded by both players, or misclassified by SCL Manager
BAD_FILES = {
    "SCL Season 4 - Week 08 - Gold - falconhit vs sharper.zip",
    "SCL Season 4 - Week 10 - Platinum - pires vs cameraman.zip",
    "SCL Season 4 - Week 09 - Platinum - drawnonward vs varanas.zip",
    "SCL Season 5 - Week 06 - Diamond - warningtrack vs cleetose.zip",
    "SCL Season 5 - Week 07 - Platinum - slappydavis vs yerand.zip",
}


def fetch_scl5_replays():
    scl_replay_zip_re = re.compile(
        r"^SCL Season . - Week (?P<week>\d+) - (?P<division>\w+) - .*?"
    )
    req = requests.get(SCL5_REPLAYS_URL)

    soup = BeautifulSoup(req.text, "xml")

    temp_extract_folder = os.path.join(SCL5_REPLAYS_FOLDER, TEMP_FOLDER)

    for key in soup.ListBucketResult.find_all("Key"):

        file = key.text

        m = scl_replay_zip_re.match(file)
        if m is None:
            print(file)
            raise ValueError

        if file not in BAD_FILES:

            zip_file_dest = os.path.join(SCL5_REPLAYS_FOLDER, ZIPS_FOLDER, file)

            extract_folder = os.path.join(
                SCL5_REPLAYS_FOLDER, m.group("division"), m.group("week").lstrip("0")
            )

            # assume if zip is present, it's been extracted
            if not os.path.exists(zip_file_dest):
                print(file, m.group("division"), m.group("week"))
                sleep(random.randint(2, 4))
                urlretrieve(SCL5_REPLAYS_URL + quote(file), zip_file_dest)

                os.makedirs(extract_folder, exist_ok=True)
                try:
                    rmtree(temp_extract_folder)
                except FileNotFoundError:
                    pass
                os.makedirs(temp_extract_folder, exist_ok=True)

                try:
                    zip_ref = zipfile.ZipFile(zip_file_dest, "r")
                except zipfile.BadZipFile as this_exep:
                    print(zip_file_dest)
                    raise this_exep

                zip_ref.extractall(temp_extract_folder)

                for root, dirs, files in os.walk(temp_extract_folder):
                    for file in files:
                        if file.endswith(".replay"):
                            copyfile(
                                LONG_FILE_HEADER + os.path.join(root, file),
                                LONG_FILE_HEADER + os.path.join(extract_folder, file),
                            )

                zip_ref.close()
                rmtree(temp_extract_folder)


def check_for_duplicate_files():
    found_dict = dict()

    for root, dirs, files in os.walk(ALL_EVENTS_FOLDER):
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
