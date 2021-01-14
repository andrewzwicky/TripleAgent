import os
import json
import logging

from triple_agent.constants.paths import OVERALL_REPORT_FOLDER

logger = logging.getLogger("triple_agent")


def create_game_manifest(all_replays):
    logger.info("updating game manifest")
    output_dictionary = dict()

    for game in all_replays:
        if game.event not in output_dictionary.keys():
            output_dictionary[game.event] = dict()

        if game.division not in output_dictionary[game.event].keys():
            output_dictionary[game.event][game.division] = dict()

        if game.week not in output_dictionary[game.event][game.division].keys():
            # Use list instead of set, because set throws a JSON encoding error
            # This is fast enough that it's easier to just do this then make
            # some custom encoder.
            output_dictionary[game.event][game.division][game.week] = list()

        names = tuple(sorted([game.spy, game.sniper]))

        if names not in output_dictionary[game.event][game.division][game.week]:
            output_dictionary[game.event][game.division][game.week].append(names)
            output_dictionary[game.event][game.division][game.week].sort()

    with open(
        os.path.join(OVERALL_REPORT_FOLDER, "all_games_manifest.json"), "w"
    ) as manifest_out:
        json.dump(output_dictionary, manifest_out, indent=4)
