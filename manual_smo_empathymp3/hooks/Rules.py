from typing import Optional
from worlds.AutoWorld import World
from ..Helpers import clamp, get_items_with_value, is_option_enabled
from BaseClasses import MultiWorld, CollectionState

import re

# Sometimes you have a requirement that is just too messy or repetitive to write out with boolean logic.
# Define a function here, and you can use it in a requires string with {function_name()}.
def overfishedAnywhere(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Has the player collected all fish from any fishing log?"""
    for cat, items in world.item_name_groups:
        if cat.endswith("Fishing Log") and state.has_all(items, player):
            return True
    return False

# You can also pass an argument to your function, like {function_name(15)}
# Note that all arguments are strings, so you'll need to convert them to ints if you want to do math.
def anyClassLevel(world: World, multiworld: MultiWorld, state: CollectionState, player: int, level: str):
    """Has the player reached the given level in any class?"""
    for item in ["Figher Level", "Black Belt Level", "Thief Level", "Red Mage Level", "White Mage Level", "Black Mage Level"]:
        if state.count(item, player) >= int(level):
            return True
    return False

def YamlEnabled(world: World, multiworld: MultiWorld, state: CollectionState, player: int, param: str) -> bool:
    """Is a yaml option enabled?"""
    return is_option_enabled(multiworld, player, param)

def YamlDisabled(world: World, multiworld: MultiWorld, state: CollectionState, player: int, param: str) -> bool:
    """Is a yaml option disabled?"""
    return not is_option_enabled(multiworld, player, param)

def BulletBillSkip(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player do certain jumps without a bullet bill (or with a bullet bill)"""
    return "{YamlDisabled(action_rando)} or {YamlDisabled(capturesanity)} or |Bullet Bill| or (|Dive| and |Cap Jump| and |Long Jump|)"

def BulletBillSmallSkip(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player do certain small jumps without a bullet bill (or with a bullet bill)"""
    return "{YamlDisabled(action_rando)} or {YamlDisabled(capturesanity)} or |Bullet Bill| or (|Dive| and |Cap Jump|)"

def BulletBillSmallSkip(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player do the bullet bill maze without a bullet bill (or with a bullet bill)"""
    return "{YamlDisabled(action_rando)} or {YamlDisabled(capturesanity)} or |Bullet Bill| or (|Dive| and (|Wall Jump| or |Triple Jump|))"

def SandPeace(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player do sand peace"""
    return "|Bullet Bill| and |Knucklotec's Fist|"

def IntoTheLake(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player enter the lake kingdom lake"""
    return "{YamlDisabled(action_rando)} or ({YamlDisabled(capturesanity)} and (((|Triple Jump| or (|Ground Pound| and |Ground Pound Jump|) or |Backward Somersault| or |Side Somersault|) and |Wall Jump| and |Cap Jump| and (|Dive| or |Goomba|)) or (|Zipper| and |Swim|))) or (((|Triple Jump| or (|Ground Pound| and |Ground Pound Jump|) or |Backward Somersault| or |Side Somersault|) and |Wall Jump|) or |Swim|)"

def LakePeace(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player do lake peace"""
    return "{IntoTheLake()} and {SwimOrCheepCheep()}"

def SwimOrCheepCheep(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """swim or cheep cheep"""
    return "{YamlDisabled(action_rando)} or {YamlDisabled(capturesanity)} or |Swim| or |Cheep Cheep|"

def SwimOrCapJump(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """swim or cap jump"""
    return "{YamlDisabled(action_rando)} or |Cap Jump|"

def CheepCheepOrGroundPound(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """cheep cheep or ground pound"""
    return "{YamlDisabled(action_rando)} or {YamlDisabled(capturesanity)} or |Ground Pound| or |Cheep Cheep|"

def MazeSkip(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player get past the maze in wooded kingdom"""
    return "{YamlDisabled(action_rando)} or {YamlDisabled(capturesanity)} or |Uproot| or ( ( ( |Ground Pound Jump| and |Ground Pound| ) or |Backward Somersault| or |Side Somersault| or ( |Wall Jump| and |Dive| ) or |Triple Jump| ) and ( |Long Jump| or |Triple Jump| or |Backward Somersault| or |Side Somersault| ) and |Cap Jump| and |Dive| )"

def ShermOrLongJump(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player do sherm or long jump"""
    return "{YamlDisabled(action_rando)} or {YamlDisabled(capturesanity)} or |Sherm| or |Long Jump|"

def PostNightMetro(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player get post-night metro moons"""
    return "{YamlDisabled(capturesanity)} or |Sherm|"

def PostTrumpeter(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player get the trumpeter in metro kingdom"""
    return "{PostNightMetro()} and ({YamlDisabled(action_rando)} or {YamlDisabled(capturesanity)} or |Long Jump| or |Pole| or |Roll| or |Ground Pound Jump| or |Dive| or |Triple Jump|)"

def MetroPeace(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player get metro peace"""
    return "({YamlDisabled(capturesanity)} or |Sherm|) and {PostTrumpeter()}"

def FromTheTopOfTheTower(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player jump frm the top of metro tower"""
    return "{YamlDisabled(action_rando)} or (|Long Jump| or (|Pole| and |Motor scooter|) or |Roll| or |Ground Pound Jump| or |Dive| or |Triple Jump|) or ({YamlDisabled(capturesanity)} and (|Long Jump| or |Motor scooter| or |Roll| or |Ground Pound Jump| or |Dive| or |Triple Jump|))"

def WallJumpOrPole(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player do wall jump or pole"""
    return "{YamlDisabled(action_rando)} or {YamlDisabled(capturesanity)} or |Wall Jump| or |Pole|"

def TyfooOrScaleATallWall(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player do tyfoo or scale a tall wall"""
    return "{YamlDisabled(action_rando)} or {YamlDisabled(capturesanity)} or |Ty-foo| or ((|Triple Jump| or (|Ground Pound| and |Ground Pound Jump|) or |Backward Somersault| or |Side Somersault|) and |Wall Jump| and |Cap Jump| and |Dive|)"

def SnowPeace(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player get snow peace"""
    return "{YamlDisabled(capturesanity)} or (|Ty-foo| and |Shiverian Racer|)"

def SeasidePeace(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player do seaside Peace"""
    return "({YamlDisabled(action_rando)} or |Ground Pound|) and ({YamlDisabled(capturesanity)} or |Gushen|)"

def SnowSeasidePeace(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player do snow or seaside Peace"""
    return "(({SnowPeace()} and (|Seaside Kingdom Power Moon:10| OR (|Seaside Kingdom Multi-Moon| AND |Seaside Kingdom Power Moon:7|))) or ({SeasidePeace()} and (|Snow Kingdom Power Moon:10| OR (|Snow Kingdom Multi-Moon| AND |Snow Kingdom Power Moon:7|))))"

def PostEarlyLuncheon(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player get more moons in luncheon than the very first ones"""
    return "{YamlDisabled(action_rando)} or {YamlDisabled(capturesanity)} or |Lava Bubble| or (|Dive| and |Cap Jump|)"

def ClimbToTheMeat(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player climb to the meat"""
    return "{YamlDisabled(action_rando)} or {YamlDisabled(capturesanity)} or |Volbonan| or (|Dive| and |Wall Jump| and (|Triple Jump| or |Ground Pound Jump| or |Backward Somersault| or |Side Somersault|))"

def LuncheonPeace(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player get snow peace"""
    return "{ClimbToTheMeat()} and ({YamlDisabled(capturesanity)} or (|Hammer Bro| and |Meat| and |Lava Bubble|))"

def JumpHigh(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player jump high"""
    return "{YamlDisabled(action_rando)} or ((|Ground Pound Jump| and |Ground Pound|) or |Backward Somersault| or |Side Somersault| or |Triple Jump|)"

def ScaleAWall(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player scale a wall"""
    return "{YamlDisabled(action_rando)} or (|Triple Jump| or (|Wall Jump| and |Dive|) or (|Ground Pound| and |Ground Pound Jump|) or |Backward Somersault| or |Side Somersault|)"

def ScaleAWallNoTripleJump(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player scale a wall without triple jump"""
    return "{YamlDisabled(action_rando)} or ((|Wall Jump| and |Dive|) or (|Ground Pound| and |Ground Pound Jump|) or |Backward Somersault| or |Side Somersault|)"

def NiceFrame(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player knock down the nice frame (and get the other nearby moon)"""
    return "{YamlDisabled(action_rando)} or {YamlDisabled(capturesanity)} or |Lakitu| or |Long Jump| or |Roll|"

def ParabonesSkip(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player skip the parabones (or use it)"""
    return "{YamlDisabled(action_rando)} or {YamlDisabled(capturesanity)} or |Parabones| or (|Long Jump| and |Cap Jump| and |Dive|)"

def BowserPeace(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player get bowser peace"""
    return "{YamlDisabled(capturesanity)} or (|Pokio|)"

def RegionalCap(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player get regional coins in cap"""
    return "{YamlDisabled(capturesanity)} or |Paragoomba|"

def RegionalCascade(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player get regional coins in cascade"""
    return "|Cascade Kingdom Power Moon:5| OR ( |Cascade Kingdom Multi-Moon| AND |Cascade Kingdom Power Moon:2| )"

def RegionalSand(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player get regional coins in sand"""
    return "({YamlDisabled(action_rando)} or |Jaxi|) and ({YamlDisabled(capturesanity)} or (|Bullet Bill| and |Knucklotec's Fist| and |Mini Rocket| and |Goomba|))"

def RegionalLake(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player get regional coins in lake"""
    return "({YamlDisabled(action_rando)} or |Swim|) and {IntoTheLake()} and ({YamlDisabled(capturesanity)} or |Zipper|) and {CheepCheepOrSwim()}"

def RegionalWooded(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player get regional coins in wooded"""
    return "({YamlDisabled(action_rando)} or |Hold/Throw|) and ({YamlDisabled(capturesanity)} and |Sherm| and |Uproot| and |Boulder|) and {MazeSkip()}"

def RegionalLost(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player get regional coins in lost"""
    return "({YamlDisabled(action_rando)} or |Wall Jump|) and ({YamlDisabled(capturesanity)} or (|Glydon| and |Tropical Wiggler|))"

def RegionalMetro(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player get regional coins in metro"""
    return "({YamlDisabled(action_rando)} or (|Long Jump| and |Dive| and |Cap Jump|) or (({YamlDisabled(capturesanity)} or |Pole|) and |Wall Jump|)) and {PostTrumpeter()} and ({YamlDisabled(capturesanity)} or (|Manhole| and |Mini Rocket|))"

def RegionalSnow(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player get regional coins in snow"""
    return "{YamlDisabled(capturesanity)} or (|Ty-foo| and |Goomba|)"

def RegionalLuncheon(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player get regional coins in luncheon"""
    return "{LuncheonPeace()} and {YamlDisabled(capturesanity)} or (|Hammer Bro| and |Volbonan| and |Meat| and |Lava Bubble|)"

def RegionalBowser(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player get regional coins in bowser"""
    return "{YamlDisabled(capturesanity)} or (|Pokio| and {NiceFrame()})"

def RegionalMoon(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player get regional coins in bowser"""
    return "{YamlDisabled(capturesanity)} or (|Parabones| and |Tropical Wiggler| and |Banzai Bill| and |Sherm|)"

def Meat(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player get meat moon"""
    return "({YamlDisabled(capturesanity)} or (|Hammer Bro| and |Meat|)) and {ClimbToTheMeat()}"

def UprootOrFireBro(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """uproot or fire bro"""
    return "{YamlDisabled(capturesanity)} or |Uproot| or |Fire Bro|"

def Lighthouse(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """can the player get to the lighthouse"""
    return "{YamlDisabled(capturesanity)} or (|Gushen| or |Cheep Cheep|)"

def Sombero(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """clothes"""
    return "{YamlDisabled(regionalshops)} or (|Sombrero| and |Poncho|)"

def Explorer(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """clothes"""
    return "{YamlDisabled(regionalshops)} or (|Explorer Hat| and |Explorer Outfit|)"

def Builder(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """clothes"""
    return "{YamlDisabled(regionalshops)} or (|Builder Helmet| and |Builder Outfit|)"

def Snowsuit(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """clothes"""
    return "{YamlDisabled(regionalshops)} or (|Snow Hood| and |Snow Suit|)"

def Resort(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """clothes"""
    return "{YamlDisabled(regionalshops)} or (|Resort Hat| and |Resort Outfit|)"

def Chef(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """clothes"""
    return "{YamlDisabled(regionalshops)} or (|Chef Hat| and |Chef Suit|)"

def Samurai(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """clothes"""
    return "{YamlDisabled(regionalshops)} or (|Samurai Helmet| and |Samurai Armor|)"

def Boxers(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """clothes"""
    return "{YamlDisabled(coin_shops)} or |Boxer Shorts|"

def Swimwear(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """clothes"""
    return "{YamlDisabled(regionalshops)} or {YamlDisabled(coin_shops)} or ((|Swim Goggles| and |Swimwear|) or |Boxer Shorts|)"

# You can also return a string from your function, and it will be evaluated as a requires string.
def requiresMelee(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Returns a requires string that checks if the player has unlocked the tank."""
    return "|Figher Level:15| or |Black Belt Level:15| or |Thief Level:15|"

def ItemValue(world: World, multiworld: MultiWorld, state: CollectionState, player: int, args: str):
    """When passed a string with this format: 'valueName:int',
    this function will check if the player has collect at least 'int' valueName worth of items\n
    eg. {ItemValue(Coins:12)} will check if the player has collect at least 12 coins worth of items
    """

    args_list = args.split(":")
    if not len(args_list) == 2 or not args_list[1].isnumeric():
        raise Exception(f"ItemValue needs a number after : so it looks something like 'ItemValue({args_list[0]}:12)'")
    args_list[0] = args_list[0].lower().strip()
    args_list[1] = int(args_list[1].strip())

    if not hasattr(world, 'item_values_cache'): #Cache made for optimization purposes
        world.item_values_cache = {}

    if not world.item_values_cache.get(player, {}):
        world.item_values_cache[player] = {
            'state': {},
            'count': {},
            }

    if (args_list[0] not in world.item_values_cache[player].get('count', {}).keys()
            or world.item_values_cache[player].get('state') != dict(state.prog_items[player])):
        #Run First Time or if state changed since last check
        existing_item_values = get_items_with_value(world, multiworld, args_list[0])
        total_Count = 0
        for name, value in existing_item_values.items():
            count = state.count(name, player)
            if count > 0:
                total_Count += count * value
        world.item_values_cache[player]['count'][args_list[0]] = total_Count
        world.item_values_cache[player]['state'] = dict(state.prog_items[player]) #save the current gotten items to check later if its the same
    return world.item_values_cache[player]['count'][args_list[0]] >= args_list[1]


# Two useful functions to make require work if an item is disabled instead of making it inaccessible
def OptOne(world: World, multiworld: MultiWorld, state: CollectionState, player: int, item: str, items_counts: Optional[dict] = None):
    """Check if the passed item (with or without ||) is enabled, then this returns |item:count|
    where count is clamped to the maximum number of said item in the itempool.\n
    Eg. requires: "{OptOne(|DisabledItem|)} and |other items|" become "|DisabledItem:0| and |other items|" if the item is disabled.
    """
    if item == "":
        return "" #Skip this function if item is left blank
    if not items_counts:
        items_counts = world.get_item_counts()

    require_type = 'item'

    if '@' in item[:2]:
        require_type = 'category'

    item = item.lstrip('|@$').rstrip('|')

    item_parts = item.split(":")
    item_name = item
    item_count = '1'

    if len(item_parts) > 1:
        item_name = item_parts[0]
        item_count = item_parts[1]

    if require_type == 'category':
        if item_count.isnumeric():
            #Only loop if we can use the result to clamp
            category_items = [item for item in world.item_name_to_item.values() if "category" in item and item_name in item["category"]]
            category_items_counts = sum([items_counts.get(category_item["name"], 0) for category_item in category_items])
            item_count = clamp(int(item_count), 0, category_items_counts)
        return f"|@{item_name}:{item_count}|"
    elif require_type == 'item':
        if item_count.isnumeric():
            item_current_count = items_counts.get(item_name, 0)
            item_count = clamp(int(item_count), 0, item_current_count)
        return f"|{item_name}:{item_count}|"

# OptAll check the passed require string and loop every item to check if they're enabled,
def OptAll(world: World, multiworld: MultiWorld, state: CollectionState, player: int, requires: str):
    """Check the passed require string and loop every item to check if they're enabled,
    then returns the require string with items counts adjusted using OptOne\n
    eg. requires: "{OptAll(|DisabledItem| and |@CategoryWithModifedCount:10|)} and |other items|"
    become "|DisabledItem:0| and |@CategoryWithModifedCount:2| and |other items|" """
    requires_list = requires

    items_counts = world.get_item_counts()

    functions = {}
    if requires_list == "":
        return True
    for item in re.findall(r'\{(\w+)\(([^)]*)\)\}', requires_list):
        #so this function doesn't try to get item from other functions, in theory.
        func_name = item[0]
        functions[func_name] = item[1]
        requires_list = requires_list.replace("{" + func_name + "(" + item[1] + ")}", "{" + func_name + "(temp)}")
    # parse user written statement into list of each item
    for item in re.findall(r'\|[^|]+\|', requires):
        itemScanned = OptOne(world, multiworld, state, player, item, items_counts)
        requires_list = requires_list.replace(item, itemScanned)

    for function in functions:
        requires_list = requires_list.replace("{" + function + "(temp)}", "{" + func_name + "(" + functions[func_name] + ")}")
    return requires_list
