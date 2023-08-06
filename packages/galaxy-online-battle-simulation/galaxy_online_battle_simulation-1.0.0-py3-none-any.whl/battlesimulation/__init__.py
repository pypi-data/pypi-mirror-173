__version__ = "1.0.0"

from battlesimulation.components.config import _GlobalGameParameters

_GGP: _GlobalGameParameters = None
_debug_printing = False
_debug_limit_variables = True

from battlesimulation.components.config import load_global_game_parameters

load_global_game_parameters()

def debug_print(text):
    global _debug_printing
    if _debug_printing:
        print(text)

from battlesimulation.components.basic_game_entity import _BasicGameEntity, _BasicGameEntityArray
from battlesimulation.components.damage import Damage, DamageArray
from battlesimulation.components.rocket import Rocket, RocketArray
from battlesimulation.components.building import Building, BuildingArray
from battlesimulation.components.module_and_bonuses import ModuleAndBonuses
from battlesimulation.components.spaceship import Spaceship, Hercules, Loki, Raptor, Hornet, Javelin, Excalibur, Valkyrie, Titan, Abaddon
from battlesimulation.components.planet import Planet
from battlesimulation.components.spacefleet import SpaceFleet
from battlesimulation.context import Context
from battlesimulation.battle_simulation import BattleSimulation

_root_battle_simulation = BattleSimulation()