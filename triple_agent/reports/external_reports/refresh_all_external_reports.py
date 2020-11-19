import os
from zipfile import ZipFile
from time import strftime

from pathlib import Path
from bs4 import BeautifulSoup

from triple_agent.reports.external_reports.player_reports.action_tests import (
    player_at_reports,
)
from triple_agent.reports.external_reports.player_reports.spy_selection import (
    player_spy_selection_report,
)
from triple_agent.reports.external_reports.player_reports.game_counts import (
    player_game_count_reports,
)
from triple_agent.reports.generation.ipython_notebook import execute_single_notebook
from triple_agent.constants.paths import (
    EXAMPLES_FOLDER,
    EVENT_REPORT_FOLDER,
    OVERALL_REPORT_FOLDER,
    JSON_GAMES_FOLDER,
    REPLAY_PICKLE_FOLDER,
    DOCS_FOLDER,
)
from triple_agent.parsing.replay.get_parsed_replays import get_parsed_replays
from triple_agent.constants.events import select_scl6_with_drops
from triple_agent.reports.external_reports.spy_party_fans.character_selection import (
    spf_character_selection_report,
)
from triple_agent.reports.external_reports.spy_party_fans.action_tests import (
    spf_action_test_report,
)
from triple_agent.reports.external_reports.spy_party_fans.sniper_lights import (
    spf_lights_report,
)
from triple_agent.reports.external_reports.overall_reports.games_manifest import (
    create_game_manifest,
)
from triple_agent.reports.generation.create_alias_list import create_alias_list

EVENT_REPORT_SOURCE = Path(__file__).parents[0].joinpath("event_reports")
OVERALL_REPORT_SOURCE = Path(__file__).parents[0].joinpath("overall_reports")

ZIP_CHUNK_SIZE = 2000


def delete_stale_json_files():
    json_uuid_set = {f.stem for f in JSON_GAMES_FOLDER.iterdir() if f.suffix == ".json"}
    pkl_uuid_set = {f.stem for f in REPLAY_PICKLE_FOLDER.iterdir()}

    # these are games that were generated, but deleted, so the json files
    # should be removed as well
    removed_games = json_uuid_set - pkl_uuid_set

    for uuid in removed_games:
        JSON_GAMES_FOLDER.joinpath(f"{uuid}.json").unlink()


def create_zip_start_end_indices(num_files: int, chunk_size: int):
    assert num_files > 0
    assert chunk_size > 0

    count = 1
    start = 0
    end = min(chunk_size, num_files - 1)

    while True:
        yield count, start, end

        count += 1
        start += chunk_size
        end = min(end + chunk_size, num_files - 1)

        if start >= num_files:
            break


def zip_all_json_files():
    json_files = sorted([f for f in JSON_GAMES_FOLDER.iterdir() if f.suffix == ".json"])

    for zip_num, start, end in create_zip_start_end_indices(
        len(json_files), ZIP_CHUNK_SIZE
    ):
        with ZipFile(
            os.path.join(JSON_GAMES_FOLDER, f"json_games_{zip_num}.zip"), "w"
        ) as json_zip:
            for file in json_files[start:end]:
                json_zip.write(file, arcname=file.name)


def create_index_file(target_dir: Path):
    soup = BeautifulSoup("<!doctype html><html></html>", "lxml")

    soup.html.append(soup.new_tag("head"))
    soup.html.append(soup.new_tag("body"))

    title_string = target_dir.joinpath("title.txt").open().read()

    title = soup.new_tag("title")
    title.string = f"Triple Agent - {title_string}"

    # only want to have one style.css file, so all html files
    # should just point to the same one.
    depth = len(target_dir.relative_to(DOCS_FOLDER).parts)
    css_rel_path = "../" * depth + "style.css"

    soup.head.append(title)
    soup.head.append(soup.new_tag("link", rel="stylesheet", href=f"{css_rel_path}"))

    h1_tag = soup.new_tag("h1")
    h1_tag.string = f"{title_string}"

    last_update_tag = soup.new_tag("div", style="font-size: x-small")
    last_update_tag.string = f"Last Updated: {strftime('%Y-%m-%d')}"

    soup.body.append(h1_tag)

    soup.body.h1.string.insert_after(last_update_tag)

    tar_path = Path(target_dir)

    extensions_to_link = {".json", ".html", ".zip"}

    # sort this list to ensure that any zip files are first, followed by alphabetical order.
    for path in sorted(tar_path.iterdir(), key=lambda p: (p.suffix != ".zip", p.name)):
        if path.is_dir() or (
            path.name != "index.html" and path.suffix in extensions_to_link
        ):
            rel_path = path.relative_to(tar_path)
            div = soup.new_tag("div")

            if path.is_dir():
                a_tag = soup.new_tag("a", href=f"{rel_path}/index.html")
                a_tag.string = path.joinpath("title.txt").open().read()
            else:
                a_tag = soup.new_tag("a", href=f"{rel_path}")
                a_tag.string = str(rel_path)

            div.append(a_tag)

            soup.body.append(div)

    with target_dir.joinpath("index.html").open("w", encoding="utf8") as file:
        file.write(str(soup.prettify()))


def refresh_html_files():
    for root, _, _ in os.walk(DOCS_FOLDER):
        create_index_file(Path(root))


def refresh_example_notebooks():
    os.chdir(EXAMPLES_FOLDER)
    for potential_notebook in os.listdir(EXAMPLES_FOLDER):
        if potential_notebook.endswith(".ipynb"):
            print(f"executing {potential_notebook}")
            execute_single_notebook(potential_notebook)


def refresh_event_reports():
    for potential_notebook in os.listdir(EVENT_REPORT_SOURCE):
        if potential_notebook.endswith(".ipynb"):
            potential_path = os.path.join(EVENT_REPORT_SOURCE, potential_notebook)
            print(f"executing {potential_path}")
            execute_single_notebook(potential_path)
            os.system(
                f'jupyter nbconvert --to html "{potential_path}" --output-dir="{EVENT_REPORT_FOLDER}"'
            )


def refresh_overall_reports():
    for potential_notebook in os.listdir(OVERALL_REPORT_SOURCE):
        if potential_notebook.endswith(".ipynb"):
            potential_path = os.path.join(OVERALL_REPORT_SOURCE, potential_notebook)
            print(f"executing {potential_path}")
            execute_single_notebook(potential_path)
            os.system(
                f'jupyter nbconvert --to html "{potential_path}" --output-dir="{OVERALL_REPORT_FOLDER}"'
            )


def refresh_all_reports():
    all_replays = get_parsed_replays(lambda x: True, use_alias_list=False)
    create_alias_list(all_replays)

    delete_stale_json_files()
    zip_all_json_files()
    refresh_html_files()

    # SCL5 is concluded, not need to create report again
    all_replays = get_parsed_replays(lambda x: True)
    scl6_replays = list(filter(select_scl6_with_drops, all_replays))

    refresh_overall_reports()
    refresh_event_reports()

    player_at_reports(all_replays, "action_test_all")
    player_at_reports(scl6_replays, "action_test_scl6")

    player_spy_selection_report(all_replays, "spy_selection_all")
    player_spy_selection_report(scl6_replays, "spy_selection_scl6")

    player_game_count_reports(all_replays, "spy_game_count_all")
    player_game_count_reports(scl6_replays, "spy_game_count_scl6")

    refresh_example_notebooks()

    create_game_manifest(all_replays)
    spf_lights_report(all_replays)
    spf_action_test_report(all_replays)
    spf_character_selection_report(all_replays)


if __name__ == "__main__":
    refresh_all_reports()
