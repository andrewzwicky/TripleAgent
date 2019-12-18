import os
import json

from triple_agent.constants.paths import SPF_DATA_FOLDER
from triple_agent.classes.timeline import TimelineCategory


def spf_lights_report(all_replays):
    output_dictionary = {}

    for game in all_replays:
        output_dictionary[game.uuid] = []
        for event in game.timeline:
            if event.category & TimelineCategory.SniperLights:
                to_add = {
                    "action": event.event,
                    "elapsed_time": event.elapsed_time,
                    "spy_time": event.time,
                    "character": event.cast_name[0].name,
                    "role": event.role[0].name,
                }

                output_dictionary[game.uuid].append(to_add)

    with open(os.path.join(SPF_DATA_FOLDER, "sniper_lights.json"), "w") as at_json_out:
        json.dump(output_dictionary, at_json_out, indent=4)
