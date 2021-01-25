import os
import json
import logging
from collections import Counter

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
            output_dictionary[game.event][game.division][game.week] = dict()

        names = ",".join(tuple(sorted([game.spy, game.sniper])))

        if names not in output_dictionary[game.event][game.division][game.week]:
            output_dictionary[game.event][game.division][game.week][names] = list()
        output_dictionary[game.event][game.division][game.week][names].append(game.uuid)

    for k1, v1 in output_dictionary.items():
        for k2, v2 in v1.items():
            for k3, _ in v2.items():
                output_dictionary[k1][k2][k3] = {
                    k: output_dictionary[k1][k2][k3][k]
                    for k in sorted(
                        output_dictionary[k1][k2][k3].keys(), key=str.casefold
                    )
                }

    with open(
        os.path.join(OVERALL_REPORT_FOLDER, "all_games_manifest.json"), "w"
    ) as manifest_out:
        json.dump(output_dictionary, manifest_out, indent=4)
