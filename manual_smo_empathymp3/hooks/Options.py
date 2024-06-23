# Object classes from AP that represent different types of options that you can create
from Options import FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, NamedRange

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value



####################################################################
# NOTE: At the time that options are created, Manual has no concept of the multiworld or its own world.
#       Options are defined before the world is even created.
#
# Example of creating your own option:
#
#   class MakeThePlayerOP(Toggle):
#       """Should the player be overpowered? Probably not, but you can choose for this to do... something!"""
#       display_name = "Make me OP"
#
#   options["make_op"] = MakeThePlayerOP
#
#
# Then, to see if the option is set, you can call is_option_enabled or get_option_value.
#####################################################################


# To add an option, use the before_options_defined hook below and something like this:
#   options["total_characters_to_win_with"] = TotalCharactersToWinWith
#
class IncludePostPeaceMoons(DefaultOnToggle):
    """Turning this off will remove all moons that cannot be obtained before completing the given kingdom's story. Short kingdoms where the story is required (such as Cascade) are unaffected."""
    display_name = "Include Post-Peace Moons"

class Capturesanity(Toggle):
    """Shuffle all captures into the pool. Captures found in Cap or Cascade on the first visit are considered to be given for free and will not grant checks."""
    display_name = "Capturesanity"

class CoinShops(Toggle):
    """Shuffles all clothing that can be purchased with regular coins. Shop Moons are always shuffled."""
    display_name = "Coin Shops"

class RegionalShops(Toggle):
    """Shuffles all clothing, souvenirs, and stickers that can be purchased with regional coins."""
    display_name = "Regional Shops"

class ActionRando(Toggle):
    """Shuffle all Basic Actions (as listed in the Action Guide) into the pool. You start with the "Capture" and "Enter Pipe" actions. There are 2 locations for getting on Jaxi and the Motor scooter."""
    display_name = "Action Rando"

# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict) -> dict:
    options["include_post_peace_moons"] = IncludePostPeaceMoons
    options["capturesanity"] = Capturesanity
    options["coin_shops"] = CoinShops
    options["regional_shops"] = RegionalShops
    options["action_rando"] = ActionRando
    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: dict) -> dict:
    return options