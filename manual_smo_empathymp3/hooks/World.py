# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from worlds.AutoWorld import World
from BaseClasses import MultiWorld, CollectionState

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem
from ..Locations import ManualLocation

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value

# calling logging.info("message") anywhere below in this file will output the message to both console and log file
import logging

########################################################################################
## Order of method calls when the world generates:
##    1. create_regions - Creates regions and locations
##    2. create_items - Creates the item pool
##    3. set_rules - Creates rules for accessing regions and locations
##    4. generate_basic - Runs any post item pool options, like place item/category
##    5. pre_fill - Creates the victory location
##
## The create_item method is used by plando and start_inventory settings to create an item from an item name.
## The fill_slot_data method will be used to send data to the Manual client for later use, like deathlink.
########################################################################################



# Called before regions and locations are created. Not clear why you'd want this, but it's here. Victory location is included, but Victory event is not placed yet.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after regions and locations are created, in case you want to see or modify that information. Victory location is included.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    include_post_peace_moons = get_option_value(multiworld, player, "include_post_peace_moons") or True
    capturesanity = get_option_value(multiworld, player, "capturesanity") or False
    coin_shops = get_option_value(multiworld, player, "coin_shops") or False
    regional_shops = get_option_value(multiworld, player, "regional_shops") or False

    locations_to_remove = []

    for location in world.location_table:
        if location["name"] == "Moon: Defeat Bowser": continue
        if "Capture" in location.get("category", []) and not capturesanity:
            locations_to_remove.append(location["name"])
        elif "Coin" in location.get("category", []) and coin_shops:
            locations_to_remove.append(location["name"])
        elif "Regional" in location.get("category", []) and regional_shops:
            locations_to_remove.append(location["name"])
        elif not include_post_peace_moons:
            if not set(["Sand Peace", "Lake Peace", "Wooded Peace", "Metro Peace", "Snow Peace", "Seaside Peace", "Snow/Seaside Peace", "Luncheon Peace", "Bowser's Peace"]).isdisjoint(location.get("category", [])):
                locations_to_remove.append(location["name"])
    
    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in locations_to_remove:
                    region.locations.remove(location)

# The item pool before starting items are processed, in case you want to see the raw item pool at that stage
def before_create_items_starting(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# The item pool after starting items are processed but before filler is added, in case you want to see the raw item pool at that stage
def before_create_items_filler(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    # Use this hook to remove items from the item pool
    itemNamesToRemove = [] # List of item names

    # Add your code here to calculate which items to remove.
    #
    # Because multiple copies of an item can exist, you need to add an item name
    # to the list multiple times if you want to remove multiple copies of it.

    for itemName in itemNamesToRemove:
        item = next(i for i in item_pool if i.name == itemName)
        item_pool.remove(item)

    return item_pool

    # Some other useful hook options:

    ## Place an item at a specific location
    # location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Location Name")
    # item_to_place = next(i for i in item_pool if i.name == "Item Name")
    # location.place_locked_item(item_to_place)
    # item_pool.remove(item_to_place)

# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it
def after_create_items(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    capturesanity = get_option_value(multiworld, player, "capturesanity") or False
    coin_shops = get_option_value(multiworld, player, "coin_shops") or False
    regional_shops = get_option_value(multiworld, player, "regional_shops") or False
    action_rando = get_option_value(multiworld, player, "action_rando") or False

    def addReq(loc, req):
        if loc["requires"] == []:
            loc["requires"] = req
        else:
            loc["requires"] = "(" + loc["requires"] + ") and (" + req + ")"

    if action_rando and capturesanity:
        # ensuring you can do lake kingdom stuff before you go to wooded kingdom or vice versa
        addReq(region_table["Lake Kingdom"], "|Uproot| or ( ( ( |Ground Pound Jump| and |Ground Pound| ) or |Backwards Somersault| or |Side Somersault| or ( |Wall Jump| and |Dive| ) or |Triple Jump| ) and ( |Long Jump| or |Triple Jump| or |Backwards Somersault| or |Side Somersault| ) and |Cap Jump| and |Dive| )")
        addReq(region_table["Wooded Kingdom"], "((|Triple Jump| or (|Ground Pound| and |Ground Pound Jump|) or |Backwards Somersault| or |Side Somersault|) and |Wall Jump| and |Cap Jump| and (|Dive| or |Goomba|)) or (|Zipper| and |Swim|)")
        # requirements to leave lost kingdom
        addReq(region_table["Metro Kingdom"], "|Wall Jump| or |Tropical Wiggler|")

    elif action_rando and not capturesanity:
        # ensuring you can enter the lake in lake kingdom before you go to wooded kingdom
        addReq(region_table["Wooded Kingdom"], "((|Triple Jump| or (|Ground Pound| and |Ground Pound Jump|) or |Backwards Somersault| or |Side Somersault|) and |Wall Jump| and |Cap Jump|) or |Swim|")

    if action_rando:
        # ensuring you don't get stuck without Cappy in Lost Kingdom
        addReq(region_table["Lost Kingdom"], "|Ground Pound|")

    if capturesanity:
        addReq(region_table["Snow Kingdom"], "|Sherm|")
        addReq(region_table["Seaside Kingdom"], "|Sherm|")
        addReq(region_table["Moon Kingdom"], "|Pokio|")

    for location in world.location_table:
        if location["name"] == "Sand: Sand Kingdom Timer Challenge 3":
            if action_rando:
                addReq(location, "|Jaxi| or (|Long Jump| and |Roll|)")
            continue
        elif location["name"] == "Wooded: Nut Planted in the Tower":
            if action_rando and capturesanity:
                addReq(location, "|Uproot| or (|Ground Pound| and |Ground Pound Jump|) or |Backwards Somersault| or |Side Somersault| or |Wall Jump|")
            continue
        elif location["name"] == "Wooded: Flooding Pipeway Ceiling Secret":
            if action_rando:
                addReq(location, "|Swim| and |Wall Jump| and ((|Ground Pound| and |Ground Pound Jump|) or |Backwards Somersault| or |Side Somersault| or (|Dive| and |Cap Jump|))")
            continue
        elif location["name"] == "Lost: On a Tree in a Swamp":
            if action_rando and capturesanity:
                addReq(location, "|Tropical Wiggler| or (|Cap Jump| and |Dive|) or (|Wall Jump| and |Glydon|)")
            continue
        elif location["name"] == "Lost: Peeking Out from Under the Bridge":
            if action_rando and capturesanity:
                addReq(location, "|Tropical Wiggler| or |Dive|")
            continue
        if action_rando and capturesanity:
            for category in location.get("category", []):
                if "Kingdom" in category:
                    continue
                elif category == "Bullet Bill Skip":
                    addReq(location, "|Bullet Bill| or (|Dive| and |Cap Jump| and |Long Jump|)")
                elif category == "Bullet Bill Small Skip":
                    addReq(location, "|Bullet Bill| or (|Dive| and |Cap Jump|)")
                elif category == "Bullet Bill Maze":
                    addReq(location, "|Bullet Bill| or (|Dive| and (|Wall Jump| or |Triple Jump|))")
                elif category == "Into the Lake":
                    addReq(location, "((|Triple Jump| or (|Ground Pound| and |Ground Pound Jump|) or |Backwards Somersault| or |Side Somersault|) and |Wall Jump| and |Cap Jump| and (|Dive| or |Goomba|)) or (|Zipper| and |Swim|)")
                elif category == "Swim or Cheep Cheep":
                    addReq(location, "|Swim| or |Cheep Cheep|")
                elif category == "Cheep Cheep or Ground Pound":
                    addReq(location, "|Ground Pound| or |Cheep Cheep|")
                elif category == "Maze Skip":
                    addReq(location, "|Uproot| or ( ( ( |Ground Pound Jump| and |Ground Pound| ) or |Backwards Somersault| or |Side Somersault| or ( |Wall Jump| and |Dive| ) or |Triple Jump| ) and ( |Long Jump| or |Triple Jump| or |Backwards Somersault| or |Side Somersault| ) and |Cap Jump| and |Dive| )")
        elif action_rando and not capturesanity:
            for category in location.get("category", []):
                if "Kingdom" in category:
                    continue
                elif category == "Into the Lake":
                    addReq(location, "(|Triple Jump| or (|Ground Pound| and |Ground Pound Jump|) or |Backwards Somersault| or |Side Somersault|) and |Wall Jump|) or |Swim|")
        if action_rando:
            for category in location.get("category", []):
                if "Kingdom" in category:
                    continue
                elif category in ["Sombrero", "Swimwear", "Explorer", "Builder", "Boxers", "Snowsuit", "Resort", "Chef", "Samurai", "Lake Peace", "Night Metro", "Pokino", "Bowser's Peace", "Capture", "Shop", "Coin"]:
                    continue
                elif category == "Scale a Wall":
                    addReq(location, "|Triple Jump| or (|Wall Jump| and |Dive|) or (|Ground Pound| and |Ground Pound Jump|) or |Backwards Somersault| or |Side Somersault|")
                elif category == "Scale a Wall (No Triple Jump)":
                    addReq(location, "(|Wall Jump| and |Dive|) or (|Ground Pound| and |Ground Pound Jump|) or |Backwards Somersault| or |Side Somersault|")
                elif category in ["Long Jump", "Roll", "Ground Pound", "Dive", "Ground Pound Jump", "Backward Somersault", "Side Somersault", "Triple Jump", "Wall Jump", "Hold/Throw", "Swim", "Jaxi", "Motor scooter"]:
                    addReq(location, "|" + category + "|")
                
        if capturesanity:
            if location["region"] == "Metro Kingdom" and "Night Metro" not in location.get("category", []):
                addReq(location, "|Sherm|")
            elif location["region"] == "Bowser's Kingdom" and "Pokino" not in location.get("category", []):
                addReq(location, "|Pokio|")
            for category in location.get("category", []):
                if "Kingdom" in category:
                    continue
                elif category == "Sand Peace":
                    addReq(location, "|Bullet Bill| and |Knucklotec's Fist|")
                elif category == "Wooded Peace":
                    addReq(location, "|Sherm| and |Uproot|")
                elif category == "Metro Peace":
                    addReq(location, "|Manhole|")
                elif category == "Snow Peace":
                    addReq(location, "|Ty-foo| and |Shiverian Racer|")
                elif category == "Seaside Peace":
                    addReq(location, "|Gushen|")
                elif category == "Snow/Seaside Peace":
                    addReq(location, "((|Ty-foo| and |Shiverian Racer| and (|Seaside Kingdom Power Moon:10| OR (|Seaside Kingdom Multi-Moon| AND |Seaside Kingdom Power Moon:7|))) or (|Gushen| and (|Snow Kingdom Power Moon:10| OR (|Snow Kingdom Multi-Moon| AND |Snow Kingdom Power Moon:7|))))")
                elif category == "Luncheon Peace":
                    addReq(location, "|Hammer Bro| and |Meat| and |Lava Bubble|")
                elif category == "Regional":
                    if location["region"] == "Cap Kingdom":
                        addReq(location, "|Paragoomba|")
                    elif location["region"] == "Sand Kingdom":
                        addReq(location, "|Bullet Bill| and |Knucklotec's Fist| and |Jaxi| and |Mini Rocket| and |Goomba|")
                    elif location["region"] == "Lake Kingdom":
                        addReq(location, "|Zipper|")
                    elif location["region"] == "Wooded Kingdom":
                        addReq(location, "|Sherm| and |Uproot| and |Boulder|")
                    elif location["region"] == "Lost Kingdom":
                        addReq(location, "|Glydon| and |Tropical Wiggler|")
                    elif location["region"] == "Metro Kingdom":
                        addReq(location, "|Manhole| and |Mini Rocket|")
                    elif location["region"] == "Snow Kingdom":
                        addReq(location, "|Ty-foo| and |Goomba|")
                    elif location["region"] == "Seaside Kingdom":
                        addReq(location, "|Gushen| and |Cheep Cheep|")
                    elif location["region"] == "Luncheon Kingdom":
                        addReq(location, "|Hammer Bro| and |Volbonan| and |Meat| and |Lava Bubble|")
                    elif location["region"] == "Bowser's Kingdom":
                        addReq(location, "|Lakitu|")
                    elif location["region"] == "Moon Kingdom":
                        addReq(location, "|Parabones| and |Tropical Wiggler| and |Banzai Bill|")
                elif category == "Meat":
                    addReq(location, "|Hammer Bro| and |Meat|")
                elif category == "Uproot or Fire Bro":
                    addReq(location, "|Uproot| or |Fire Bro|")
                elif category == "Lighthouse":
                    addReq(location, "(|Gushen| or |Cheep Cheep|)")
                elif category in ["Paragoomba", "Bullet Bill", "Cactus", "Goomba", "Knucklotec's Fist", "Mini Rocket", "Glydon", "Lakitu", "Zipper", "Cheep Cheep", "Puzzle Part", "Uproot", "Fire Bro", "Sherm", "Coin Coffer", "Tree", "Boulder", "Picture Match Part", "Tropical Wiggler", "Manhole", "Taxi", "RC Car", "Ty-foo", "Shiverian Racer", "Gushen", "Lava Bubble", "Volbonan", "Hammer Bro", "Meat", "Pokio", "Jizo", "Bowser Statue", "Parabones", "Banzai Bill", "Bowser"]:
                    addReq(location, "|" + category + "|")
        if regional_shops:
            if "Sombrero" in location.get("category", []):
                addReq(location, "|Sombrero| and |Poncho|")
            if "Explorer" in location.get("category", []):
                addReq(location, "|Explorer Hat| and |Explorer Outfit|")
            if "Builder" in location.get("category", []):
                addReq(location, "|Builder Helmet| and |Builder Outfit|")
            if "Snowsuit" in location.get("category", []):
                addReq(location, "|Snow Hood| and |Snow Suit|")
            if "Resort" in location.get("category", []):
                addReq(location, "|Resort Hat| and |Resort Outfit|")
            if "Chef" in location.get("category", []):
                addReq(location, "|Chef Hat| and |Chef Suit|")
            if "Samurai" in location.get("category", []):
                addReq(location, "|Samurai Helmet| and |Samurai Armor|")
        if coin_shops:
            if "Boxers" in location.get("category", []):
                addReq(location, "|Boxer Shorts|")
        if "Swimwear" in location.get("category", []) and regional_shops and coin_shops:
            addReq(location, "((|Swim Goggles| and |Swimwear|) or |Boxer Shorts|)")

    def Example_Rule(state: CollectionState) -> bool:
        # Calculated rules take a CollectionState object and return a boolean
        # True if the player can access the location
        # CollectionState is defined in BaseClasses
        return True

    ## Common functions:
    # location = world.get_location(location_name, player)
    # location.access_rule = Example_Rule

    ## Combine rules:
    # old_rule = location.access_rule
    # location.access_rule = lambda state: old_rule(state) and Example_Rule(state)
    # OR
    # location.access_rule = lambda state: old_rule(state) or Example_Rule(state)

# The item name to create is provided before the item is created, in case you want to make changes to it
def before_create_item(item_name: str, world: World, multiworld: MultiWorld, player: int) -> str:
    return item_name

# The item that was created is provided after creation, in case you want to modify the item
def after_create_item(item: ManualItem, world: World, multiworld: MultiWorld, player: int) -> ManualItem:
    return item

# This method is run towards the end of pre-generation, before the place_item options have been handled and before AP generation occurs
def before_generate_basic(world: World, multiworld: MultiWorld, player: int) -> list:
    pass

# This method is run at the very end of pre-generation, once the place_item options have been handled and before AP generation occurs
def after_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This is called before slot data is set and provides an empty dict ({}), in case you want to modify it before Manual does
def before_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called after slot data is set and provides the slot data at the time, in case you want to check and modify it after Manual is done with it
def after_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called right at the end, in case you want to write stuff to the spoiler log
def before_write_spoiler(world: World, multiworld: MultiWorld, spoiler_handle) -> None:
    pass
