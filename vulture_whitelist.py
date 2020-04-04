import pytesseract

from triple_agent.classes.game import GameHandler
from triple_agent.classes.outcomes import WinType
from triple_agent.constants.colors import (
    PlotColorsWong,
    PlotColorsTolBright,
    PlotColorsTolMuted,
    PlotColorsSCL,
)
from triple_agent.constants.events import (
    SCL5_DIVISIONS,
    SCL5_PICK_MODES,
    SCL6_VENUE_MODES,
    select_sc19,
    select_scl5,
    select_scl5_regular_season,
    select_scl5_with_drops,
    select_scl6,
    select_scl6_regular_season,
    select_scl6_placements
)
from triple_agent.reports.specific.action_tests import (
    action_test_percentages,
    diff_action_test_percentages,
)
from triple_agent.reports.specific.banana_breads import (
    all_banana_bread_percentages,
    first_banana_bread_percentages,
    banana_split,
)
from triple_agent.reports.specific.conversation import cumulative_conversation_times
from triple_agent.reports.specific.bug import bug_attempt_timings, bug_success_rate
from triple_agent.reports.specific.character_selection import (
    spy_selection,
    amba_selection,
    double_agent_selection,
    st_selection,
)
from triple_agent.reports.specific.fingerprints import (
    attempted_fingerprint_sources,
    successful_fingerprint_sources,
)
from triple_agent.reports.specific.game_durations import game_durations
from triple_agent.reports.specific.game_outcomes import game_outcomes
from triple_agent.reports.specific.microfilm import at_or_direct_mf
from triple_agent.reports.specific.mission_choices import mission_choices
from triple_agent.reports.specific.mission_completes import (
    mission_completion,
    mission_completion_query,
    final_mission_completion_query
)
from triple_agent.reports.specific.scl_set_scores import (
    game_differential,
    scl_set_scores_categorize,
)
from triple_agent.reports.specific.seduce import first_flirt_timing
from triple_agent.reports.specific.stop_talks import stop_talk_in_game_percentage
from triple_agent.reports.specific.time_adds import (
    time_add_times,
    time_add_times_per_game,
)
from triple_agent.reports.specific.lights import amba_lights, spy_lights
from triple_agent.reports.external_reports.misc_reports.curator_requests import (
    cough_clank_crash,
    curated_many_green_ats,
)
from triple_agent.organization.extract_spectation_replays import (
    extract_spectate_replays,
)


# library internals
pytesseract.pytesseract.tesseract_cmd
extract_spectate_replays

# jsonpickle methods
GameHandler
GameHandler.flatten
GameHandler.restore

# colors
PlotColorsWong
PlotColorsTolBright
PlotColorsTolMuted
PlotColorsSCL

# notebook usage
WinType.SniperWin
SCL5_PICK_MODES
SCL5_DIVISIONS
SCL6_VENUE_MODES
select_scl5
select_scl5_regular_season
select_sc19
action_test_percentages
diff_action_test_percentages
all_banana_bread_percentages
first_banana_bread_percentages
banana_split
bug_attempt_timings
bug_success_rate
spy_selection
st_selection
amba_selection
double_agent_selection
attempted_fingerprint_sources
successful_fingerprint_sources
game_durations
game_outcomes
at_or_direct_mf
mission_choices
mission_completion_query
mission_completion
scl_set_scores_categorize
game_differential
first_flirt_timing
stop_talk_in_game_percentage
time_add_times_per_game
time_add_times
spy_lights
amba_lights
select_scl5_with_drops
select_scl6
select_scl6_regular_season
select_scl6_placements
cumulative_conversation_times
final_mission_completion_query

# archive, but unused
cough_clank_crash
curated_many_green_ats
