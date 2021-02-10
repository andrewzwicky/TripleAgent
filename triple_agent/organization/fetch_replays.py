from pathlib import Path
import os
import random
import re
import zipfile
from shutil import copyfile, rmtree
from time import sleep
from urllib.parse import quote
from urllib.request import urlretrieve
from typing import Dict

import requests
from bs4 import BeautifulSoup
from triple_agent.constants.paths import (
    LONG_FILE_HEADER,
    ALL_EVENTS_FOLDER,
    SCL6_REPLAYS_FOLDER,
    SCL6_TEMP_EXTRACT_FOLDER,
    SCL6_ZIP_EXTRACT_FOLDER,
)

SCL6_REPLAYS_URL = r"https://s3-us-west-2.amazonaws.com/scl-replays-season6/"


# These are files I suspect were uploaded by both players, or misclassified by SCL Manager
BAD_FILES = {
    "SCL Season 4 - Week 08 - Gold - falconhit vs sharper.zip",
    "SCL Season 4 - Week 10 - Platinum - pires vs cameraman.zip",
    "SCL Season 4 - Week 09 - Platinum - drawnonward vs varanas.zip",
    "SCL Season 5 - Week 06 - Diamond - warningtrack vs cleetose.zip",
    "SCL Season 6 - Week 03 - Oak - smashblade vs phillammon.zip",
    "SCL Season 6 - Week 03 - Oak - maxstermind vs tonewyork.zip",
    "SCL Season 6 - Week 02 - Oak - cptbasch vs testierjamaj.zip",
    "SCL Season 6 - Week 02 - Oak - armageddon vs tonewyork.zip",
    "SCL Season 6 - Week 03 - Oak - cptbasch vs atia.zip",
    "SCL Season 6 - Week 02 - Oak - atia vs phillammon.zip",
    "SCL Season 6 - Week 02 - Oak - cptbasch vs tonewyork.zip",
    "SCL Season 6 - Week 02 - Oak - smashblade vs maxstermind.zip",
    "SCL Season 6 - Week 03 - Oak - cptbasch vs ibutra.zip",
    "SCL Season 6 - Week 03 - Oak - maxstermind vs phillammon.zip",
    "SCL Season 6 - Week 04 - Oak - cptbasch vs armageddon.zip",
    "SCL Season 6 - Week 04 - Oak - smashblade vs phillammon.zip",
    "SCL Season 6 - Week 06 - Oak - cptbasch vs testierjamaj.zip",
    "SCL Season 6 - Week 08 - Oak - armageddon vs tonewyork.zip",
    "SCL Season 6 - Week 08 - Oak - cptbasch vs atia.zip",
    "SCL Season 6 - Week 09 - Oak - smashblade vs atia.zip",
}

SCL_REPLAY_ZIP_RE = re.compile(
    r"^SCL Season . - Week (?P<week>\d+) - (?P<division>\w+) - .*?"
)


def fetch_replays(url: str):
    soup = BeautifulSoup(requests.get(url).text, "xml")

    os.makedirs(SCL6_ZIP_EXTRACT_FOLDER, exist_ok=True)
    existing_zip_files = os.listdir(SCL6_ZIP_EXTRACT_FOLDER)

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
        zip_file_dest = SCL6_ZIP_EXTRACT_FOLDER.joinpath(zip_file_match.string)

        extract_folder = SCL6_REPLAYS_FOLDER.joinpath(
            zip_file_match.group("division"),
            zip_file_match.group("week").lstrip("0"),
        )

        print(
            zip_file_match.string,
            zip_file_match.group("division"),
            zip_file_match.group("week"),
        )
        sleep(random.randint(2, 4))
        urlretrieve(url + quote(zip_file_match.string), zip_file_dest)

        os.makedirs(extract_folder, exist_ok=True)
        try:
            rmtree(SCL6_TEMP_EXTRACT_FOLDER)
        except FileNotFoundError:
            pass
        os.makedirs(SCL6_TEMP_EXTRACT_FOLDER, exist_ok=True)

        try:
            zip_ref = zipfile.ZipFile(zip_file_dest, "r")
        except zipfile.BadZipFile as this_exep:
            print(zip_file_dest)
            raise this_exep

        zip_ref.extractall(SCL6_TEMP_EXTRACT_FOLDER)

        for file in SCL6_TEMP_EXTRACT_FOLDER.glob("**/*,replay"):
            copyfile(
                LONG_FILE_HEADER / file,
                LONG_FILE_HEADER / extract_folder.joinpath(file.name),
            )

        zip_ref.close()
        rmtree(SCL6_TEMP_EXTRACT_FOLDER)


def check_for_duplicate_files(events_folder: Path):
    found_dict: Dict[str, str] = dict()

    for root, _, files in os.walk(events_folder):
        if root != events_folder:
            for file in files:
                if file.endswith(".replay"):
                    if file not in found_dict.keys():
                        found_dict[file] = root
                    else:
                        print(
                            "XXX",
                            file,
                            os.path.relpath(root, events_folder),
                            os.path.relpath(found_dict[file], events_folder),
                        )


if __name__ == "__main__":
    fetch_replays(SCL6_REPLAYS_URL)
    check_for_duplicate_files(ALL_EVENTS_FOLDER)
