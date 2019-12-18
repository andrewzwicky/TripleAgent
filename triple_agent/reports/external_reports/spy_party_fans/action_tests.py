import os
import json

from triple_agent.classes.missions import Missions
from triple_agent.constants.paths import SPF_DATA_FOLDER
from triple_agent.classes.timeline import TimelineCategory


def spf_action_test_report(all_replays):
    output_dictionary = {}

    for game in all_replays:
        output_dictionary[game.uuid] = []
        for event in game.timeline:
            if event.category & TimelineCategory.ActionTest:
                to_add = {
                    "action": event.mission.name,
                    "elapsed_time": event.elapsed_time,
                    "spy_time": event.time,
                    "action_test": event.action_test.name,
                    "difficult": False,
                }
                if event.category & TimelineCategory.TimeAdd:
                    to_add["action"] = "TimeAdd"

                if event.mission == Missions.Fingerprint:
                    to_add["difficult"] = True

                output_dictionary[game.uuid].append(to_add)

    with open(os.path.join(SPF_DATA_FOLDER, "action_test.json"), "w") as at_json_out:
        json.dump(output_dictionary, at_json_out, indent=4)
