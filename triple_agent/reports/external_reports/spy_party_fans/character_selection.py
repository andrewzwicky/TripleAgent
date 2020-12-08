from collections import defaultdict
import os
import json

from triple_agent.classes.outcomes import WinType
from triple_agent.constants.paths import SPF_DATA_FOLDER
from triple_agent.classes.timeline import TimelineCategory


def spf_character_selection_report(all_replays):
    output_dictionary = {}

    for game in all_replays:
        output_dictionary[game.uuid] = defaultdict(list)
        output_dictionary[game.uuid]["Shot"] = [None]
        for event in game.timeline:
            if event.category & TimelineCategory.Cast:
                # assume there will only be one role in the cast portion
                # assume there will be a role in the Cast timeline events.
                output_dictionary[game.uuid][event.role[0].name].append(
                    event.cast_name[0].stringify()
                )

            if event.category & TimelineCategory.SniperShot:
                output_dictionary[game.uuid]["Shot"] = [event.cast_name[0].stringify()]

    with open(os.path.join(SPF_DATA_FOLDER, "character_data.json"), "w") as at_json_out:
        json.dump(output_dictionary, at_json_out, indent=4)
