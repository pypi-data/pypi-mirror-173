Galaxy Online Battle Simulation
========
# Introduction
This module was made for simulation of different battles in the online space strategy game Galaxy Online.

You can use this module to analize your possibilities, casualties, costs, etc; you can find possible good counters to incoming attacks on you.

There is a GUI version of Game Calculator: https://github.com/fadedness/Galaxy-Online-Battle-Calculator
and you would probably prefer it over text command line.

But as of 2022/10/25 it uses built in methods of calculations and I'm gonna change that to use this new module instead.

# install and usage
```
python -m pip install galaxy-online-battle-simulation
```

To use it either run python -m battlesimulation for interactive mode with menu
or import it in your script and use Context class:
```
python -m battlesimulation
```
```
from battlesimulation import Context
context = Context()
# hints what to do
context.help()
# lists of Game objects with ids and params
context.help_game_parameters()
```

# Detailed usage and description
Fleet 1 is considered always attacking the Fleet 2, which is defending Planet's surface. Fleet 3 is blockading or supporting Planet.
If you want a Space Battle just use default (empty) Planet and Fleet 1 and 2.

Every Fleet can have different Modules; Planet can have different Buildings on it and Rockets in its Turrets that will fire at attacking Spaceships.

Accuracy of Spaceships in Game is random (from 80% to 100%),
but you can calculate min and max amounts of Spaceships that could be destroyed in actual Game.

Let's see what game situations this module can handle.

First of all you need to import and instantiate Context class:
```
from battlesimulation import Context
context = Context()
```

### 1. You have an incoming attack and you what to know how you could counter that.
```
# add those attacker's spaceships to Fleet 2
context.add_%spaceshipname_to_fleet_2(quantity)
# add module for attacker if it has any
context.set_fleet_2_module_by_id_and_level(id, level)
# add module for your Fleet if you plan to use it
context.set_fleet_1_module_by_id_and_level(id, level)
# and run simulation
context.simulate()
```
You will get results sorted and printed in casualties' cost and build time ascending order.
It only suggests single spaceship Fleet, five battle spaceships - five results.
Actually ten results. 5 for minimum you need to counter and five for lowering your casualties' with game's Superiority mechanic
(the more spaceships you send, the less will be destoyed).

Because in this situation you are going to counter-attack, you don't need to change Fleet's default attacking flag.
But if you want to defend passively, you would need to call:
```
context.set_fleet_1_attacking(False)
context.set_fleet_2_attacking(True)
```
What does that do? Game uses Priorities to calculate which Spaceships will receive more damage.
And When you're defending certain Spaceships (Valkyrie) have lower priority and thus recieve less damage.

### 2. You have a battle log that looks unrealistic to you (the Game is in Beta, so errors can occur). You can simulate it with module and get possible min and max results. And compare log with these ranges.
```
# add all spaceships to corresponding Fleets
context.add_%spaceshipname_to_fleet_1(quantity)
context.add_%spaceshipname_to_fleet_2(quantity)

# set Modules (if any) and right priorities
context.set_fleet_1_module_by_id_and_level(id, level)
context.set_fleet_2_module_by_id_and_level(id, level)
context.set_fleet_1_attacking(False)
context.set_fleet_2_attacking(True)

# set planet if it was involved with Turrets passive or active (Rockets) damage,
# if not, skip it
# sizes: 0 - 3 Mines, 1 - 4 Mines, 2 - 5 Mines
# type and size define Turrets passive damage
context.set_planet(type in [1,2,3,4,5,6,7], size in [0,1,2], sum_of_all_turrets_levels)

# for example the Planet in Game is:
# Chromium with 4 Mines, Turret buildings: 20, 20, 19, 19
context.set_planet(4, 1, 78)

# add Rockets (if any were involved)
context.add_rocket(id, quantity)

# set Fleets' accuracy type to range_max or range_min (doesn't matter)
context.set_fleet_1_acc_type("range_max")
context.set_fleet_2_acc_type("range_max")

# and run simulation
context.simulate()
# the results will be printed
```

You can directly access objects for results:
```
context._fleet_1
context._fleet_2
context._fleet_3
context._planet
context._planet.rockets
context._planet.buildings
# for example
context._fleet_1.fleet_alive #(property, returns dict, {spaceship_id_1: quantity_1, ...}
# and for range_max or range_min
# a new Context is created inside main one for additional simulation
context.context_branch
# and it's the same in terms of access
context.context_branch._fleet_1
```
All Game objects can be printed:
```
print(context._fleet_1)
# or can even have filtered string (for non-zero quantity, for example)
print(context._fleet_1.filtered_alive_str)
print(context._planet.filtered_str_full)
```
### 3. You can set Planet with Buildings (Shield Generator is the main defense) and get the number of Valkyries needed to destroy them and the number of Valkyries that will be destroyed by defenses.

Although this Bombardment mechanic is going to be changed with newer one, it is still here.

### 4. You can simulate two consecutive battles with Fleets, when Fleet 3 is stationary around the Planet.
For both just simulations or finding a possible good counter to both Fleets (2 and 3) at once.

Fleet 3 could be a third player's blockade around the Planet or Planet owner's ally's Support.

## Game Objects
### Spaceships:
id - name
1. Hercules
2. Loki
3. Raptor
4. Hornet
5. Javelin
6. Excalibur
7. Valkyrie
8. Titan
9. Abaddon

### Rockets:
id - name
1. Sticks-XL
2. Cobra-M1
3. Aurora
4. X-Ray

### Buildings:
id - name
1. Command Center
2. Mine
3. Warehouse
4. Trade Office
5. Cosmodrome
6. Spacecraft Plant
7. Power Plant
8. Detection Station
9. Missile Turret
10. Shield Generator

### Modules:
id - name
1. Disintegrator
2. Afterburner
3. Shield Booster
4. Complex Bastion
5. Complex Luch
6. Complex Halo
7. Complex Guardian
8. Satellite Solarium
9. Satellite Energy
10. Complex Boarding

Once again:
```
# lists of Game objects with ids and params
context.help_game_parameters()
```
Or use Game guides on website.

# Game data
There is a file data.json in this repo. It is not used by module, it is left for reference and for advanced usage.

All data is hardcoded in components/config.py.

But instead of editing config.py, one can edit that data.json, load it via json and pass to:
```
import json
with open("/path/to/data.json", "r") as f:
	loaded_data = json.load(f)
battlesimulation.load_global_game_parameters(loaded_data)
```
If the data is valid it will be loaded and used in this module.

# Conclusion
There are many things you can set and do, but I'm not going to document it here, sorry.
Mainly because I have a GUI version.

Almost all functions have doc strings with some explanations.

# licence
MIT License

# contact
You can contact me via telegram https://t.me/fadedness
