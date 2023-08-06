from __future__ import annotations
from typing import Union
import battlesimulation
from battlesimulation import Building, BuildingArray, Damage, DamageArray, Rocket, RocketArray

##############################################

class Planet():
    """Planet class representing Game Planet with Buildings, Rockets and possible (but only one) blockade SpaceFleet."""

    def get_turrets_lvl(self) -> int:
        if self._simple_turrets_lvl:
            return self._turrets_lvl
        else:
            return self.buildings.total_turrets_level

    def set_turrets_lvl(self, value: int) -> None:
        if isinstance(value, int) and value >= 0:
            self._turrets_lvl = value

    @property
    def passive_damage(self) -> DamageArray:
        """Returns DamageArray of Turret's "passive" damage."""

        damage_array = DamageArray()
        damage_value = self.turrets_lvl * self.turret_damage * self.planetary_coef
        damage_array.set_item_of_array(Damage(self.turret_damage_type_id, damage_value))
        return damage_array

    @property
    def rockets_original(self) -> dict:
        """Returns a dict of Rockets quantities before they were used."""

        if isinstance(self.rockets, RocketArray):
            return self.rockets.rockets_original

    @property
    def rockets_left(self) -> dict:
        """Returns a dict of Rockets quantities left."""

        if isinstance(self.rockets, RocketArray):
            return self.rockets.rockets_left
    
    @property
    def rockets_used(self) -> dict:
        """Returns a dict of Rockets quantities that were already used."""

        if isinstance(self.rockets, RocketArray):
            return self.rockets.rockets_used

    turrets_lvl = property(get_turrets_lvl, set_turrets_lvl)

    def __init__(self) -> None:
        self._turrets_lvl = 0
        self._simple_turrets_lvl = False
        self.blockade = None
        self.rockets = RocketArray()
        self.buildings = BuildingArray()
        self._reinit()

    def _reinit(self) -> None:
        self.planet_type = 1
        self.planet_size = 0
        self.x = 0
        self.y = 0
        self.set_turrets_lvl(0)
        self.turret_damage = battlesimulation._GGP.globals["turret_damage"]
        self.turret_damage_type_id = battlesimulation._GGP.globals["turret_damage_type_id"]
        self.shield_damage_type_id = battlesimulation._GGP.globals["shield_damage_type_id"]
        self.planetary_coef = 0.80
        self.blockade = None
        if isinstance(self.rockets, RocketArray):
            self.rockets._reinit()
        else:
            self.rockets = RocketArray()
        if isinstance(self.buildings, BuildingArray):
            self.buildings._reinit()
        else:
            self.buildings = BuildingArray()

    def set_planet_params(self, planet: dict) -> None:
        """Sets Planet params or you can use individual functions to set specific params.

            Accepts input as dict. Structure:
            {"planet_type":id, "planet_size":id, "turrets_lvl":int, "blockade":Union[SpaceFleet,None],
            "rockets":Union[list,tuple,dict], "buildings":Union[list,tuple]}
            rockets and buildings accept list or tuple of pairs of list or tuple ((id1,value1),(id1,value2))
            rockets also accept dict of id:value keypair {id1:value1,id2:value2}.
            blockade is an enemy's SpaceFleet if present or None.
            Unnecessary params are x and y coordinates: positive ints.
            If you specify planet buildings, you should omit turrets_lvl,
            and if you omit buildings but still need turrets_lvl -> specify it as a sum of all levels of all turrets.
            All or any data value may be omitted in which case a defaults will be used:
            Planet T1 M3 with nobuildings, turrets or rockets and no blockade.
        """

        self._reinit()
        if isinstance(planet, dict):
            planet_type = planet.get("planet_type")
            planet_size = planet.get("planet_size")
            turrets_lvl = planet.get("turrets_lvl")
            rockets = planet.get("rockets")
            buildings = planet.get("buildings")
            blockade = planet.get("blockade")
            x = planet.get("x")
            y = planet.get("y")
            self.set_coordinates(x,y)
            self.set_planet_type_and_size(planet_type, planet_size)
            self.set_rockets(rockets)
            self.set_buildings(buildings)
            result = self._check_buildings_for_reinit()
            if result and turrets_lvl is None:
                self.set_simple_turrets_lvl(False)
            else:
                self.set_simple_turrets_lvl(turrets_lvl)
            self.blockade = blockade
    
    def set_coordinates(self, x: int, y: int) -> None:
        """Set Planet Game coordinates."""

        if isinstance(x, int) and x > 0:
            self.x = x
        if isinstance(y, int) and y > 0:
            self.y = y

    def set_simple_turrets_lvl(self, turrets_lvl: int) -> None:
        """Forcefully sets total Turrets level (used for Turrets "passive" damage).

            If you specify planet buildings, you should not use this;
            and if you omit buildings but still need turrets_lvl -> set it here as a sum of all levels of all turrets.
            You can also revert to using buildings by setting them and calling this set_simple_turrets_lvl with turrets_lvl as False.
        """

        if not isinstance(turrets_lvl, bool) and isinstance(turrets_lvl, int) and turrets_lvl >= 0:
            self._simple_turrets_lvl = True
            self.set_turrets_lvl(turrets_lvl)
        elif turrets_lvl == False:
            self._simple_turrets_lvl = False

    def set_planet_type_and_size(self, planet_type: int, planet_size: int) -> None:
        """Sets planet type and size (used for planetary coef -> used for base Turrets "passive" damage).

            Planet type: ordinary planets 1,2,3,4,5,6,7, Space Stations 9,12,15(? maybe for Trade SS ?).
            Planet size: 0,1,2 -> number of Mines on the Planet -> 0 - 3 Mines, 1 - 4 Mines, 2 - 5 Mines.
        """

        if planet_type in battlesimulation._GGP.types_planet_type:
            self.planet_type = planet_type
        if planet_size in battlesimulation._GGP.types_planet_size:
            self.planet_size = planet_size
        type_size_str = f"{self.planet_type}{self.planet_size}"
        planetary_coef = battlesimulation._GGP.planetary_coefs.get(type_size_str)
        if isinstance(planetary_coef, float):
            self.planetary_coef = planetary_coef

    def set_buildings(self, buildings: Union[list,tuple,dict]) -> None:
        """Sets buildings. Accepts list or tuple of pairs of list or tuple ((id1,value1),(id1,value2))
            or dict of id:value keypair {id1:value1,id2:value2}.
            Ids should be valid and unique, otherwise the last id will overwrite previous.
            Also certain buildings have a maximum buildable number on a Planet.

            Default ids: 1 - Command Center, 2 - Mine, 3 - Warehouse, 4 - Trade Office, 5 - Cosmodrome,
            6 - Spacecraft Plant, 7 - Power Plant, 8 - Detection Station, 9 - Missile Turret, 10 - Shield Generator.
        """

        self.buildings.set_whole_array(buildings)

    def set_rockets(self, rockets: Union[list,tuple,dict]) -> None:
        """First resets Rockets Array (on the Planet) and then sets it to given data.

            Accepts list or tuple of pairs of list or tuple ((id1,value1),(id1,value2))
            or dict of id:value keypair {id1:value1,id2:value2}.
            Ids should be valid and unique, otherwise the last id will overwrite previous.

            Default ids: 1 - Sticks-XL, 2 - Cobra-M1, 3 - Aurora, 4 - X-Ray.
        """

        self.rockets._reinit()
        if isinstance(rockets, list) or isinstance(rockets, tuple):
            for pair in rockets:
                if (isinstance(pair, list) or isinstance(pair, tuple)) and len(pair) == 2:
                    # index 0 is id, 1 is quantity
                    self.rockets.add_rocket(Rocket(*pair))
                elif isinstance(pair, Rocket):
                    self.rockets.add_rocket(pair)
        elif isinstance(rockets, dict):
            # key is id, value is quantity
            for id in rockets:
                if isinstance(rockets[id], int):
                    self.rockets.add_rocket(Rocket(id, rockets[id]))
                elif isinstance(rockets[id], Rocket):
                    self.rockets.add_rocket(rockets[id])
        self.rockets.reset_original_values()

    def make_a_copy_of_self(self) -> Planet:
        """Returns a new Planet instance with the same attributes."""

        new_planet = Planet()
        new_planet.buildings = self.buildings.make_a_copy_of_self()
        new_planet.rockets = self.rockets.make_a_copy_of_self()
        new_planet.blockade = self.blockade
        if self._turrets_lvl > 0 and self._simple_turrets_lvl:
            new_planet._simple_turrets_lvl = True
            new_planet._turrets_lvl = self._turrets_lvl
        else:
            new_planet._simple_turrets_lvl = False
        new_planet.set_planet_type_and_size(self.planet_type, self.planet_size)
        new_planet.set_coordinates(self.x, self.y)
        return new_planet

    def _check_buildings_for_reinit(self) -> bool:
        """When set_planet_params is called, checks if BuildingArray has any Buildings set."""

        result = False
        if isinstance(self.buildings, BuildingArray):
            for building in self.buildings:
                if isinstance(building, Building):
                    result = True
                    break
        return result

    @property
    def filtered_str_full(self) -> str:
        """Full string of self attributes."""

        text = f"Planet: T{self.planet_type} M{self.planet_size+3}, coords {self.x} {self.y}, planetary coef is {self.planetary_coef}, "
        text += f"passive turret damage: {self.passive_damage.filtered_str},\n"
        text += f"{self.buildings_string},\n{self.rockets_string}"
        return text

    @property
    def filtered_str_full_original(self) -> str:
        """Full string of self attributes."""

        text = f"Planet: T{self.planet_type} M{self.planet_size+3}, coords {self.x} {self.y}, planetary coef is {self.planetary_coef}, "
        text += f"passive turret damage: {self.passive_damage.filtered_str},\n"
        text += f"{self.buildings_string_original},\n{self.rockets_string_original}"
        return text

    @property
    def buildings_string(self) -> str:
        """Pretty BuildingsArray string."""

        return self.buildings.filtered_pretty_str

    @property
    def buildings_string_original(self) -> str:
        """Pretty BuildingsArray original string."""

        return self.buildings.filtered_pretty_str_original

    @property
    def rockets_string(self) -> str:
        """RocketsArray string of its attributes."""

        return self.rockets.filtered_str

    @property
    def rockets_string_original(self) -> str:
        """RocketsArray string of its original attributes."""

        return self.rockets.filtered_str_original

    def __repr__(self) -> str:
        """Short string of self attributes."""

        return f"Planet: T{self.planet_type} M{self.planet_size+3}, passive turret damage: {str(self.passive_damage.filtered_str)}, planetary coef is {self.planetary_coef}"

##############################################