import os
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
from triple_agent.constants.events import select_scl5_with_drops
from triple_agent.reports.external_reports.spy_party_fans.character_selection import (
    spf_character_selection_report,
)
from triple_agent.reports.external_reports.spy_party_fans.action_tests import (
    spf_action_test_report,
)
from triple_agent.reports.external_reports.spy_party_fans.sniper_lights import (
    spf_lights_report,
)

EVENT_REPORT_SOURCE = Path(__file__).parents[0].joinpath("event_reports")
OVERALL_REPORT_SOURCE = Path(__file__).parents[0].joinpath("overall_reports")


def delete_stale_json_files():
    json_uuid_set = set(
        [f.stem for f in JSON_GAMES_FOLDER.iterdir() if f.suffix == ".json"]
    )
    pkl_uuid_set = set([f.stem for f in REPLAY_PICKLE_FOLDER.iterdir()])

    # these are games that were generated, but deleted, so the json files
    # should be removed as well
    removed_games = json_uuid_set - pkl_uuid_set

    for uuid in removed_games:
        JSON_GAMES_FOLDER.joinpath(f"{uuid}.json").unlink()


def create_index_file(target_dir: Path):
    soup = BeautifulSoup("<!doctype html><html></html>", "lxml")
    head = soup.new_tag("head")
    body = soup.new_tag("body")
    soup.html.append(head)
    soup.html.append(body)

    title_string = target_dir.joinpath("title.txt").open().read()

    title = soup.new_tag("title")
    title.string = f"Triple Agent - {title_string}"

    # only want to have one style.css file, so all html files
    # should just point to the same one.
    depth = len(target_dir.relative_to(DOCS_FOLDER).parts)
    css_rel_path = "../" * depth + "style.css"

    link = soup.new_tag("link", rel="stylesheet", href=f"{css_rel_path}")
    soup.head.append(title)
    soup.head.append(link)

    h1 = soup.new_tag("h1")
    h1.string = f"{title_string}"

    soup.body.append(h1)

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
                a = soup.new_tag("a", href=f"{rel_path}/index.html")
                a.string = path.joinpath("title.txt").open().read()
            else:
                a = soup.new_tag("a", href=f"{rel_path}")
                a.string = str(rel_path)

            div.append(a)

            soup.body.append(div)

    with target_dir.joinpath("index.html").open("w", encoding="utf8") as file:
        file.write(str(soup.prettify()))


def refresh_html_files():
    for root, dirs, files in os.walk(DOCS_FOLDER):
        create_index_file(Path(root))


def refresh_example_notebooks():
    os.chdir(EXAMPLES_FOLDER)
    for potential_notebook in os.listdir(EXAMPLES_FOLDER):
        if potential_notebook.endswith(".ipynb"):
            execute_single_notebook(potential_notebook)


def refresh_event_reports():
    for potential_notebook in os.listdir(EVENT_REPORT_SOURCE):
        if potential_notebook.endswith(".ipynb"):
            potential_path = os.path.join(EVENT_REPORT_SOURCE, potential_notebook)
            execute_single_notebook(potential_path)
            os.system(
                f'jupyter nbconvert --to html "{potential_path}" --output-dir="{EVENT_REPORT_FOLDER}"'
            )


def refresh_overall_reports():
    for potential_notebook in os.listdir(OVERALL_REPORT_SOURCE):
        if potential_notebook.endswith(".ipynb"):
            potential_path = os.path.join(OVERALL_REPORT_SOURCE, potential_notebook)
            execute_single_notebook(potential_path)
            os.system(
                f'jupyter nbconvert --to html "{potential_path}" --output-dir="{OVERALL_REPORT_FOLDER}"'
            )


def refresh_all_reports():
    delete_stale_json_files()
    refresh_html_files()

    all_replays = get_parsed_replays(lambda x: True)
    scl5_replays = get_parsed_replays(select_scl5_with_drops)

    refresh_overall_reports()
    refresh_event_reports()
    player_at_reports(all_replays, scl5_replays)
    player_spy_selection_report(all_replays, scl5_replays)
    player_game_count_reports(all_replays, scl5_replays)
    refresh_example_notebooks()
    spf_lights_report(all_replays)
    spf_action_test_report(all_replays)
    spf_character_selection_report(all_replays)


if __name__ == "__main__":
    refresh_all_reports()
