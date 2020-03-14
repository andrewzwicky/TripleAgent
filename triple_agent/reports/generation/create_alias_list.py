import jsonpickle
from triple_agent.constants.paths import PLAYER_REPORT_FOLDER

jsonpickle.set_encoder_options("simplejson", sort_keys=True, indent=4)
jsonpickle.set_preferred_backend("simplejson")


def create_alias_list(all_games):
    """
    This function should create the alias list.  The alias
    list is a JSON file containing keys for *_username
    fields, either a s76.../steam name or a spyparty username.

    This function should go through all the games parsed, sort by
    date, and take the last displayname for each person and put
    that into the alias list.  This is a first pass attempt at
    not having duplicate names, which fragments stats in reports.
    :return:
    """

    date_sorted_replays = sorted(all_games, key=lambda game: game.start_time)

    alias_dict = dict()

    for this_game in date_sorted_replays:
        # always overwrite name with the latest name
        alias_dict[this_game.spy_username] = this_game.spy
        alias_dict[this_game.sniper_username] = this_game.sniper

    alias_json = jsonpickle.encode(alias_dict)

    with open(PLAYER_REPORT_FOLDER.joinpath("alias_list.json"), "w") as json_out:
        json_out.write(alias_json)
