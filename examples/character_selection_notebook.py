from triple_agent.parsing.replay.get_parsed_replays import get_parsed_replays
from triple_agent.constants.events import select_scl5_regular_season
from triple_agent.reports.specific.character_selection import determine_character_in_role
from triple_agent.reports.specific.game_outcomes import game_outcomes
from triple_agent.classes.roles import Roles
from triple_agent.reports.generation.plot_specs import AxisProperties, DataQueryProperties

scl5_replays = get_parsed_replays(select_scl5_regular_season)

_=game_outcomes(
    scl5_replays,
    axis_properties = AxisProperties(
        title="SCL5 Game Outcomes by Spy Character",
        x_axis_portrait=True,
        y_axis_label="Game Count",
        x_axis_label="Spy Character",
        savefig='example_pictures/scl5_spy_selection.png'
    ),
    data_query = DataQueryProperties(
        groupby=lambda g: determine_character_in_role(g, Roles.Spy),
        secondary_order=sum,
    )
)
