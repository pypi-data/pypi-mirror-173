from __future__ import annotations
from typing import Union
import math
import battlesimulation
from battlesimulation import debug_print, _BasicGameEntityArray, Damage, DamageArray, Spaceship, ModuleAndBonuses, Planet, Rocket
from battlesimulation.components.utility import _my_truncate, _my_round_threshold_up

##############################################

class SpaceFleet(_BasicGameEntityArray):
    """SpaceFleet (Array) with fixed order and the same types of items (Spaceship)."""

    def get_acc_type(self) -> str:
        return self._acc_type
    
    def set_acc_type(self, acc_type: str) -> None:
        if acc_type in ("min","max","random","range_min","range_max") or (isinstance(acc_type, int) and 0 < acc_type <= 100):
            self._acc_type = acc_type

    acc_type = property(get_acc_type, set_acc_type)

    def __init__(self) -> None:
        """New instance of SpaceFleet class."""

        super().__init__(battlesimulation._GGP.types_spaceship, Spaceship, SpaceFleet)

        self.custom_name = "SpaceFleet"
        self.attacking = True # or defending = False | only for deciding which priorities to use
        self.attack_planet = True # direct attack of the Planet or False - make a blockade
        self._acc_type = "min"
        # this is for storing temporary incoming damage_array       DamageArray()
        self._temp_incoming_damage_array: DamageArray = None
        # this is for storing enemy's fleet damage to us            DamageArray()
        self.incoming_damage_array: DamageArray = None
        # this is for storing turret passive damage to us           DamageArray()
        self.incoming_turrets_damage: DamageArray = None
        # this is for storing shield generator EMP burst damage     DamageArray()
        self.incoming_emp_shield_damage: DamageArray = None
        self._reinit()

    def _reinit(self) -> None:
        """Resets SpaceFleet's modules, stored incoming damage arrays and spaceships."""

        self._reinit_spaceships()
        self.custom_name = "SpaceFleet"
        self.attacking = True
        self.attack_planet = True
        self._reinit_stored_damage_arrays()
        self._reinit_modules()

    def _reinit_spaceships(self) -> None:
        """Resets SpaceFleets spaceships to defaults."""

        super()._reinit()

    def _reinit_stored_damage_arrays(self) -> None:
        """Resets SpaceFleet's stored incoming damage arrays."""

        self._temp_incoming_damage_array = DamageArray()
        self.incoming_damage_array = DamageArray()
        self.incoming_turrets_damage = DamageArray()
        self.incoming_emp_shield_damage = DamageArray()

    def _reinit_modules(self) -> None:
        """Resets self.modules to new default Modules."""

        self.modules = ModuleAndBonuses()

    def get_spaceship(self, id: int) -> Spaceship:
        """Returns reference to corresponding Spaceship instance contained in self."""

        return self._get_item_of_array_by_id(id)

    def set_module_params(self, attack: Union[int,float] = None, defense: Union[int,float] = None, speed: Union[int,float] = None) -> None:
        """Sets module bonuses for attack, defense and speed.

            Accepts int (percent (but times 100 for an option of 3725/10000 -> 37.25 bonus), 5000 -> 0.5 + 1 -> 1.5) or float (1.5).
            For the case of testing values can be a negative int (but not below -100*100 (not included) -> -9999) or 0 < float < 1.
            That is kinda antibonus.
            If value is omitted a default value of 1.0 will be used.
        """

        self.modules.set_module_params(attack, defense, speed)

    def set_module_by_id(self, id: int, level: int = 100) -> None:
        """Set module by id and level to existing named Game Module.

            1 - Disintegrator, 2 - Afterburner, 3 - Shield Booster, 4 - Complex Bastion,
            5 - Complex Luch, 6 - Complex Halo, 7 - Complex Guardian,
            no bonuses:
            8 - Satellite Solarium, 9 - Satellite Energy, 10 - Complex Boarding.
        """

        self.modules.set_module_by_id(id, level)

    def set_module_attack_damage_mods(self, data: Union[list,tuple,dict]):
        """Sets attack damage mods (for example for Commanders in the future or for tests).

            Accepts input data of list or tuple of pairs (also list or tuple): ((id1,value1),(id2,value2)) or dict {id1:value1,id2:value2}.
            Ids should be valid and unique, otherwise the last id will overwrite previous.
            Values should be int (percent but times 100, i.e. 5000 -> 1.5) or float (1.5).
            For the case of testing values can be a negative int (but not below -100*100 (not included) -> -9999) or 0 < float < 1.
            Ids may be omitted and default value of 1.0 will be used for them.
        """
        self.modules._set_damage_mods(data, "attack")

    def set_module_defense_damage_mods(self, data: Union[list,tuple,dict]):
        """Sets defense damage mods (for example for Commanders in the future or for tests).

            Accepts input data of list or tuple of pairs (also list or tuple): ((id1,value1),(id2,value2)) or dict {id1:value1,id2:value2}.
            Ids should be valid and unique, otherwise the last id will overwrite previous.
            Values should be int (percent but times 100, i.e. 5000 -> 1.5) or float (1.5).
            For the case of testing values can be a negative int (but not below -100*100 (not included) -> -9999) or 0 < float < 1.
            Ids may be omitted and default value of 1.0 will be used for them.
        """

        self.modules._set_damage_mods(data, "defense")

    def set_fleet_to_attack_or_blockade_planet(self, attack_planet: bool = True) -> None:
        """Sets flag whether SpaceFleet is going to attack or blockade Planet."""

        if attack_planet:
            self.attack_planet = True
        else:
            self.attack_planet = False

    def set_fleet(self, spaceships: Union[list,tuple,dict]) -> bool:
        """Sets fleet of spaceships.
        
            First, it resets all SpaceFleet's spaceships and then sets them to passed data.
            Accepts input data of list or tuple of pairs (also list or tuple): ((id1,value1),(id2,value2)) or dict {id1:value1,id2:value2}.
            Ids should be valid and unique, for list or tuple with duplicated ids, spaceships will be overwritten with the last ones.
            Values (quantity of spaceships) should be int (whole spaceship) or float (should not be used, left for testing).
            N.B. Spaceships quantity when battle is simulated will become float.
        """

        self._reinit_spaceships()
        return self.set_whole_array(spaceships)

    def set_spaceship_in_fleet(self, spaceship: Union[list,tuple,dict,Spaceship]) -> bool:
        """Add a new spaceship to the Fleet, overwriting previous same spaceship (if any).

            Accepts list or tuple with length of 2: [id,quantity] or (id,quantity) or dict: {id:quantity}
            or an already instantiated spaceship.

            Default ids: 1 - Hercules, 2 - Loki, 3 - Raptor, 4 - Hornet, 5 - Javelin,
            6 - Excalibur, 7 - Valkyrie, 8 - Titan, 9 - Abaddon.
        """

        return self.set_item_of_array(spaceship)

    def calc_incoming_raw_damage_per_ship(self, enemy_total_damage: DamageArray) -> dict:
        """Calculates damage distribution per spaceships based on Priorities game mechanic.

            Returns a dict where key is Spaceship id and value is DamageArray for that spaceship.
            Will set all damages to zero in the input array. But will keep original damages.
            Later, func sum_up_leftover_damage will transfer left over damage to target array.
        """

        result = {}
        if isinstance(enemy_total_damage, DamageArray):
            priorities = self.priorities_array
            for ss_id in priorities:
                semi_result = DamageArray()
                for damage in enemy_total_damage:
                    if isinstance(damage, Damage):
                        value = damage.damage * priorities[ss_id]
                        semi_result.add_damage(Damage(damage.damage_type_id,value))
                semi_result.reset_original_values()
                result.update({ss_id:semi_result})

        if len(result) == 0:
            result = {-1:enemy_total_damage}
        else:
            enemy_total_damage.set_to_zero()
        return result

    def sum_up_leftover_damage(self, incoming_damage_per_ship: dict, target_array: DamageArray = None) -> DamageArray:
        """Sums up leftover damage per spaceship to new or passed (target) DamageArray.

            Takes type of data that was returned by calc_incoming_raw_damage_per_ship and gathers it back to one DamageArray.
            If target array was specified, it is modified and None is returned.
            If no target array then a new instance of DamageArray will be used and returned by the function.
        """

        if isinstance(incoming_damage_per_ship, dict):
            if isinstance(target_array, DamageArray):
                result = target_array
            else:
                result = DamageArray()
            for ss_id in incoming_damage_per_ship:
                damage_array = incoming_damage_per_ship[ss_id]
                if isinstance(damage_array, DamageArray):
                    for damage in damage_array:
                        if isinstance(damage, Damage):
                            result.add_damage(damage)
            if isinstance(target_array, DamageArray):
                # ok
                return
            else:
                result.reset_original_values()
                return result

    def calc_incoming_rockets_number_per_ship(self, rockets_number: int, priorities: dict) -> dict:
        """Calculates rocket distribution per spaceship based on Priorities game mechanic.

            Because number of rockets is always an int, results of calculations are rounded down.
            Plus Loki spaceships cannot be targeted by rockets, so they are ignored here.
            Does safety check so the sum of rockets per spaceship doesn't become larger than initial.
        """

        result = {}
        if isinstance(rockets_number, int) and rockets_number > 0 and isinstance(priorities, dict):
            rockets_left = rockets_number
            # max_priority = (ss_id, priority)
            max_priority = [1,0]
            for ss_id in priorities:
                priority = priorities[ss_id]
                if priority > max_priority[1]:
                    max_priority[0] = ss_id
                    max_priority[1] = priority
                semi_result = int(rockets_number * priority)
                if rockets_left - semi_result < 0:
                    semi_result = rockets_left
                    result.update({ss_id:semi_result})
                    rockets_left = 0
                else:
                    rockets_left -= semi_result
                    result.update({ss_id:semi_result})
            # In a situation where priorities distribution spikes
            # preemptively adds left rockets to the spaceships with maximum priority rate
            # or else due to rounding down it could go to infinite loop.
            # probably, the upper limit could be a little bit lower
            if 0 < rockets_left and rockets_left <= 5:
                result[max_priority[0]] += rockets_left
        return result

    def finalize_battle_results(self):
        """Sets quantity of each spaceship to alive value.

            After battle spaceships need to be rounded to "alive" value.
            As far as I could investigate, float quantity of spaceships is rounded by math rule of 0.5.
            So 130.491235 would become 130 and 95.50 -> 96.
        """

        for ss in self:
            if isinstance(ss, Spaceship):
                ss.quantity = ss.alive

    def calc_possible_spaceship_from_remaining_time(self, remaining: int, x1: int = None, x2: int = None, \
            y1: int = None, y2: int = None, planet1: Planet = None, planet2: Planet = None) -> tuple:
        """Suggests possible spaceships that can travel given distance in the given time.

            This func takes in remaining time (from attack.get(\"remaining\")) and game coordinates or Planets with coordinates
            and returns a tuple of two sets:
            returns (set1,set2).
            Set1 is a set of all spaceships that could travel between given coordinates
            with time approximately equal to given remaining time with it's base speed (precision is within 5% difference).
            Set2 is the same except for speed being increased with the max bonus of Afterburner module of level 100,
            that is Set2 - possible spaceships with speed module.
        """

        possible_spaceships = set()
        possible_spaceships_with_max_speed_modules = set()
        if isinstance(remaining, int) and remaining > 0 and isinstance(battlesimulation._GGP.globals.get("max_speed_bonus"), float) and battlesimulation._GGP.globals.get("max_speed_bonus") > 1.0:
            if isinstance(planet1, Planet) and isinstance(planet2, Planet):
                x1 = planet1.x
                y1 = planet1.y
                x2 = planet2.x
                y2 = planet2.y
            if isinstance(x1, int) and x1 > 0 and isinstance(x2, int) and x2 > 0 and isinstance(y1, int) and y1 > 0 and isinstance(y2, int) and y2 > 0:
                for id in battlesimulation._GGP.spaceships:
                    ss = battlesimulation._GGP.spaceships[id]
                    if isinstance(ss, dict):
                        calc_speed = ss.get("calc_speed")
                        if isinstance(calc_speed, float) and calc_speed > 0:
                            distance = math.sqrt((x1-x2)**2 + (y1-y2)**2)
                            raw_time = distance / (calc_speed * 1.0)    # 1.0 no speed module
                            precision = abs(raw_time / remaining - 1)
                            if precision <= 0.05:
                                possible_spaceships.add(ss.id)
                            distance = math.sqrt((x1-x2)**2 + (y1-y2)**2)
                            raw_time = distance / (calc_speed * battlesimulation._GGP.globals.get("max_speed_bonus"))    # 2.0 max speed bonus (from Module Afterburner level 100)
                            precision = abs(raw_time / remaining - 1)
                            if precision <= 0.05:
                                possible_spaceships_with_max_speed_modules.add(ss.id)
        return (possible_spaceships, possible_spaceships_with_max_speed_modules)

    def get_priorities_array_for_rockets(self, rocket: Rocket) -> dict:
        """Calculates spaceships priorities based on the passed Rocket.

            Unlike normal priorities, it depends on type of attack (blockade or attack)
            and on valid targets of the Rocket.
        """

        # unlike priorities against DamageArray (@property self.priorities_array), 
        # I want to keep spaceships with quantity > 0 for displaying debug_print()
        # 
        # because rockets have valid_targets, some spaceships will have 0 priority
        priorities = {}
        if self.is_populated:
            if isinstance(rocket, Rocket):
                valid_targets = rocket.valid_targets
                result = {}
                for ss in self:
                    if isinstance(ss, Spaceship):
                        result.update({ss.id:0})
                        # because all items in self._array are always instantiated, skip spaceships with no quantity
                        if ss.quantity > 0:
                            priorities.update({ss.id:0})
                sum_of_priorities = 0
                for ss in self:
                    if isinstance(ss, Spaceship):
                        if ss.id in valid_targets:
                            if self.attacking:
                                value = ss.attack_priority * ss.quantity
                                sum_of_priorities += value
                                result[ss.id] = value
                            else:
                                value = ss.defense_priority * ss.quantity
                                sum_of_priorities += value
                                result[ss.id] = value
                if sum_of_priorities > 0:
                    for id in result:
                        if id in priorities:
                            priorities[id] = _my_round_threshold_up(result[id] / sum_of_priorities, 6, battlesimulation._GGP.threshold)
        return priorities

    def make_a_copy_of_self(self) -> SpaceFleet:
        """Returns a new SpaceFleet instance with the same attributes and nested attributes.

            Including Spaceships (ids and quantity), a new Module with the same params (mod bonuses are not finalized!),
            with the same acc_type and attacking bool, with the same damage_arrays."""

        result: SpaceFleet = super().make_a_copy_of_self()
        if isinstance(self.modules, ModuleAndBonuses):
            result.set_module_params(self.modules.attack, self.modules.defense, self.modules.speed)
            result.set_module_attack_damage_mods(self.modules.attack_damage_mods)
            result.set_module_defense_damage_mods(self.modules.defense_damage_mods)
        result.acc_type = self.acc_type
        result.attacking = self.attacking
        result.attack_planet = self.attack_planet
        if isinstance(self._temp_incoming_damage_array, DamageArray):
            result._temp_incoming_damage_array = self._temp_incoming_damage_array.make_a_copy_of_self()
        if isinstance(self.incoming_damage_array, DamageArray):
            result.incoming_damage_array = self.incoming_damage_array.make_a_copy_of_self()
        if isinstance(self.incoming_turrets_damage, DamageArray):
            result.incoming_turrets_damage = self.incoming_turrets_damage.make_a_copy_of_self()
        if isinstance(self.incoming_emp_shield_damage, DamageArray):
            result.incoming_emp_shield_damage = self.incoming_emp_shield_damage.make_a_copy_of_self()
        return result

    def total_hp_for_defense_type(self, defense_type: int) -> Union[int,float]:
        """Returns total HP for specified defense type counting current quantities."""

        total_hp = 0
        if defense_type in battlesimulation._GGP.types_damage:
            for ss in self:
                if isinstance(ss, Spaceship):
                    total_hp += ss.defenses[defense_type] * ss.quantity
        return total_hp

    @property
    def total_damage(self) -> DamageArray:
        """Returns DamageArray with total damage of Spaceships based on self.acc_type (accuracy).

            If acc_type was set to 0 < int <= 100, then it will be used.
            If acc_type is a valid string ("min","max","random","range_min","range_max") it is passed to each spaceship's func get_accuracy.
            If none of the above a 100% accuracy is used.
        """
        total_damage_array = DamageArray()
        for ss in self:
            if isinstance(ss, Spaceship):
                id = ss.damage_type_id
                if isinstance(self.acc_type, int) and 0 < self.acc_type and self.acc_type <= 100:
                    value = ss.quantity * ss.attack * self.acc_type / 100 * self.modules.final_attack_damage_mods[id]
                elif self.acc_type in ("min","max","random","range_min","range_max"):
                    value = ss.quantity * ss.attack * ss.get_accuracy(self.acc_type) / 100 * self.modules.final_attack_damage_mods[id]
                else:
                    value = ss.quantity * ss.attack * 100 / 100 * self.modules.final_attack_damage_mods[id]
                total_damage_array.add_damage(Damage(id,value))
        total_damage_array.reset_original_values()
        return total_damage_array

    @property
    def priorities_array(self) -> dict:
        """Calculates spaceships priorities, based on Priority game mechanic."""

        priorities = {}
        if self.is_populated:
            semi_result = {}
            for ss in self:
                if isinstance(ss, Spaceship):
                    semi_result.update({ss.id:0})
            sum_of_priorities = 0
            for ss in self:
                if isinstance(ss, Spaceship):
                    if self.attacking:
                        value = ss.attack_priority * ss.quantity
                        sum_of_priorities += value
                        semi_result[ss.id] = value
                    else:
                        value = ss.defense_priority * ss.quantity
                        sum_of_priorities += value
                        semi_result[ss.id] = value
            if sum_of_priorities > 0:
                for id in semi_result:
                    # skip result with zero value ( == zero quantity of particular spaceship)
                    if semi_result[id]:
                        priorities.update({id: _my_round_threshold_up(semi_result[id] / sum_of_priorities, 6, battlesimulation._GGP.threshold)})
        return priorities

    @property
    def total_defenses(self) -> int:
        "Total defense of current quantity of spaceships. Used by Superiority game mechanic."

        total_defenses = 0
        for ss in self:
            if isinstance(ss, Spaceship):
                total_defenses += ss.total_defense
        return total_defenses

    @property
    def fleet_original(self) -> dict:
        """Returns dict of original quantities of spaceships: {ss.id: original_quantity}."""

        result = {}
        for id in self._valid_ids:
            result.update({id:0})
        for ss in self:
            if isinstance(ss, Spaceship) and ss.id in result:
                result[ss.id] = ss.original_quantity
        return result

    @property
    def fleet_alive(self) -> dict:
        """Returns dict of quantities of alive spaceships: {ss.id: alive_quantity}."""

        result = {}
        for id in self._valid_ids:
            result.update({id:0})
        for ss in self:
            if isinstance(ss, Spaceship):
                id = ss.id
                alive = ss.alive
                if id in result:
                    result[id] = alive
        return result

    @property
    def fleet_dead(self) -> dict:
        """Returns dict of quantities of dead spaceships: {ss.id: dead_quantity}."""

        result = self.fleet_original
        for id in result:
            result[id] = int(result[id])
        alive = self.fleet_alive
        for id in alive:
            if id in result:
                result[id] -= alive[id]
        return result

    @property
    def fleet_current(self) -> dict:
        """Returns dict of quantities of current (may be float) spaceships: {ss.id: current_quantity}."""

        result = {}
        for id in self._valid_ids:
            result.update({id:0})
        for ss in self:
            if isinstance(ss, Spaceship):
                id = ss.id
                quantity = ss.quantity
                if isinstance(quantity, float):
                    quantity = _my_truncate(quantity, 6)
                if id in self._valid_ids:
                    result[id] = quantity
        return result

    @property
    def is_populated(self) -> bool:
        """Returns True if at least 0.000001 quantity of a Spaceship is present in SpaceFleet."""

        result = False
        for id in self.fleet_current:
            if self.fleet_current[id] > 0:
                result = True
                break
        return result

    @property
    def was_populated(self) -> bool:
        """Returns True if at least one original quantity of a Spaceship is not zero in SpaceFleet."""

        result = False
        for id in self.fleet_original:
            if self.fleet_original[id] > 0:
                result = True
                break
        return result

    @property
    def cost_of_original(self) -> int:
        """Cost in energy of all Spaceships before any Battles."""

        result = 0
        for ss in self:
            if isinstance(ss, Spaceship):
                result += ss.cost_of_original
        return result

    @property
    def cost_of_dead(self) -> int:
        """Cost in energy of all destroyed Spaceships."""

        result = 0
        for ss in self:
            if isinstance(ss, Spaceship):
                result += ss.cost_of_dead
        return result

    @property
    def build_time_of_original(self) -> int:
        """Time in seconds to build (at Spacecraft Plant level 1) all Spaceships before any Battles."""

        result = 0
        for ss in self:
            if isinstance(ss, Spaceship):
                result += ss.build_time_of_original
        return result

    @property
    def build_time_of_dead(self) -> int:
        """Time in seconds to build (at Spacecraft Plant level 1) all destroyed Spaceships."""

        result = 0
        for ss in self:
            if isinstance(ss, Spaceship):
                result += ss.build_time_of_dead
        return result

    @property
    def filtered_str(self) -> str:
        """Different short string of current spaceships quantities in self."""

        text = "Spacefleet: ["
        for ss in self:
            if isinstance(ss, Spaceship):
                if ss.quantity:
                    #text += f"{ss.quantity} of {battlesimulation._GGP.spaceships[ss.id].get('name_en')}s, "
                    text += f"{ss.filtered_str}, "
        if text != "Spacefleet: [":
            text = text[:-2]
        text += "]"
        if text == "Spacefleet: []":
            text = "Spacefleet: [empty]"
        return text

    @property
    def filtered_alive_str(self) -> str:
        """Different short string of alive spaceships quantities in self."""

        text = "Spacefleet alive: ["
        for ss in self:
            if isinstance(ss, Spaceship):
                if ss.original_quantity:        # ss.alive:
                    text += f"{ss.alive}/{ss.original_quantity} of {battlesimulation._GGP.spaceships[ss.id].get('name_en')}s, "
                #text += f"{ss}, "
        if text != "Spacefleet alive: [":
            text = text[:-2]
        text += "]"
        if text == "Spacefleet alive: []":
            text = "Spacefleet alive: [empty]"
        return text

    @property
    def filtered_dead_str(self) -> str:
        """Different short string of dead spaceships quantities in self."""

        fleet_original = self.fleet_original
        text = "Spacefleet dead: ["
        for id in self.fleet_dead:
            value = self.fleet_dead[id]
            if id in fleet_original and fleet_original[id] > 0:
                text += f"{value} of {battlesimulation._GGP.spaceships[id].get('name_en')}s, "
        if text != "Spacefleet dead: [":
            text = text[:-2]
        text += "]"
        if text == "Spacefleet dead: []":
            text = "Spacefleet dead: [empty]"
        return text
    
    @property
    def filtered_original_str(self) -> str:
        """Different short string of original spaceships quantities in self."""

        text = "Spacefleet original: ["
        for id in self.fleet_original:
            value = self.fleet_original[id]
            if value > 0:
                text += f"{value} of {battlesimulation._GGP.spaceships[id].get('name_en')}s, "
        if text != "Spacefleet original: [":
            text = text[:-2]
        text += "]"
        if text == "Spacefleet original: []":
            text = "Spacefleet original: [empty]"
        return text

    def __repr__(self) -> str:
        """Short string of spaceships quantities in self."""

        text = "<Spacefleet>: ["
        #fleet_current = self.fleet_current
        #for id in fleet_current:
            #text += f"{fleet_current[id]} of {battlesimulation._GGP.spaceships.get(id).get('name_en')}s, "
        for ss in self:
            if isinstance(ss, Spaceship):
                text += f"{ss}, "
        if text != "<Spacefleet>: [":
            text = text[:-2]
        text += "]"
        if text == "<Spacefleet>: []":
            text = "<Spacefleet>: [empty]"
        return text

##############################################