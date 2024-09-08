# Super Mario Odyssey Manual Randomizer Guide

Heavily borrows code from [MarioManTAW's apworld in the Manual for Archipelago Server](https://discord.com/channels/1097532591650910289/1146498720792334336/1199903507772350465)

Welcome to the Manual Randomizer for Super Mario Odyssey!
The way it works is: you send out checks by collecting moons, and cannot leave a Kingdom until you have the required amount of moons/multimoons as items.
Every moon other than Post-Game moons are randomized, though you can turn off Post-World Peace moons. (but like, don't do that. it breaks everything.)

## Where is the settings page?

The .yaml file is included with the GitHub release.

## What are the other settings?

- You can randomize every capture, meaning you can't use it until you receive the item for it.
  - You start off with Frog, Wire, all 3 different Chain Chomps, and the T-Rex, so that you don't get immediately stuck in Cap/Cascade kingdom.
    - The aforementioned starting items do not have corresponding locations.
  - The locations are obtained by capturing the capture. If you don't have the item for it, immediately uncapture.
- You can add locations for every shop item that costs regional coins.
- You can add locations for every shop item that costs regular coins.
- You can randomize every basic action (as listed in the Action Guide).
  - You start with the "Capture", "Enter Pipe", and "Cap Throw and Hold" actions.
  - There are 2 locations for getting on Jaxi and the Motor scooter. Dismount immediately if you don't have the item!

## What is the goal of Super Mario Odyssey when randomized?

There are three goals to choose from:
- Complete the Festival (which involves doing world peace in metro kingdom)
- Defeat Bowser and Escape the Moon (which involves beating the game)
- World Peace (which involves doing world peace in every kingdom and then beating the game)

## Required Software

- Super Mario Odyssey
- Archipelago from the [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases)

## Installation Procedures

Make sure a copy of the Manual world is in the lib/world directory of your client-side installation.

## Joining a MultiWorld Game

1. Launch the launcher.
2. Click on Manual client on the right.
3. At the top enter your server's ip with the port provided (by default archipelago.gg:38281).
4. In Manual Game ID put "Manual_SMO_mp3" then press the Connect button on the top right.
5. In the command field at the bottom enter the name of your slot you chose in your Player.yaml then press enter

## Manual Client

In the "Tracker and Locations" tab you'll find buttons corresponding with all the available locations in the Randomizer. Since this is a manual game its built on trust™ you press the locations when you get to them, hopefully in the future only what you can access will be visible but at the moment you could press victory and it would accept it. Also, if you have death_link enabled, there's a button at the top right to trigger and receive death links.

## Playing the Game

Start from a new save file. 
Proceed through Cap Kingdom, and once you reach Cascade Kingdom you can start getting checks.
You'll need to receive 5 moons (or 2 moons and a multi-moon) to leave the kingdom.
Each kingdom requires the necessary amount of moon items to leave, listed below:

## How many moons do you need to leave each kingdom?

For generic moons:

- Cascade: 5
- Sand: 21
- Lake/Wooded: 45
  - In Generic Moons Mode specifically, you can visit either kingdom after leaving sand but can't leave to Cloud until you get 45.
- Lost: 55
- Metro: 75
- Snow/Seaside: 95 (same as lake/wooded)
- Luncheon: 113
- Ruined: 116
- Bowser's: 124

For specific moons:

Keep in mind that a Multi-Moon counts as 3!
- Cascade: 5
- Sand: 16
- Lake: 8
- Wooded: 16
- Lost: 10
- Metro: 20
- Snow: 10
- Seaside: 10
- Luncheon: 18
- Ruined: 3
- Bowser's: 8

## What actions are randomized (if enabled)

If you're playing with `action_rando` enabled, until you receive the items for these, you can't do these things.
Similar actions that other captures have are *not* randomized (like Bowser's Triple Jump)

- Long Jump
- Roll
- Ground Pound
- Dive
- Ground Pound Jump
- Upward Throw
- Downward Throw
- Spin Throw
- Cap Jump
- Homing Cap Throw
- Backward Somersault (aka backflip)
- Side Somersault (aka sideflip)
- Triple Jump
- Wall Jump
- Hold/Throw
- Swim (specifically referring to pressing B in the water to go up. gliding along the surface of the water is fine.)
- Quick Swim (just check the action guide for this one. it's actually needed to do one check in seaside kingdom.)
- Spin (not useful in the slightest, unless you don't have motion controls to do spin throw for some reason, or you're trying to do spin pounds. but those aren't in logic.)
- Dash (2D)
- Jaxi
- Motor scooter

# How do traps work?

If you're playing with generic moons, you'll probably have some filler items, and I recommend replacing them with traps!
Here's the list:

- Return Trap: When you receive it, warp back to the Odyssey and walk back to where you were manually.
- Upside Down Trap: Until you collect a moon, play with your controller upside down.
- Cappyless Trap: Until you collect a moon, play without using cappy.