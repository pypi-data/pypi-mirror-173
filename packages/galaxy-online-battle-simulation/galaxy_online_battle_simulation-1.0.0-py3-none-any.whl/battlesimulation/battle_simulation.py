from __future__ import annotations
from typing import Union
import battlesimulation
from battlesimulation import debug_print, Damage, DamageArray, \
        Spaceship, SpaceFleet, ModuleAndBonuses, Planet, Rocket, RocketArray
from battlesimulation.components.building import Building, BuildingArray
from battlesimulation.components.utility import _my_truncate, _my_round_up, _my_round_down, _my_round_threshold_up, _my_round_threshold_down

##############################################

class BattleSimulation():
    """BattleSimulation Class for somewhat manual management of Simulation. Use Context class for more comfort."""

    def _formated_text_of_damage_per_spaceships(self, data: dict, priorities: dict) -> str:
        """Returns formated string of Damages per Spaceships."""

        text = ""
        if isinstance(data, dict) and isinstance(priorities, dict):
            for ss_id in data:
                damage_array = data[ss_id]
                if ss_id in priorities and isinstance(priorities[ss_id], float):
                    percent = _my_truncate(priorities[ss_id] * 100,2)
                else:
                    percent = "undefined"
                if ss_id in battlesimulation._GGP.types_spaceship and isinstance(damage_array, DamageArray):
                    if damage_array.filtered_str == "[empty]":
                        text += f"{battlesimulation._GGP.spaceships[ss_id].get('name_en')}: {damage_array.filtered_str}\n"
                    else:
                        text += f"{battlesimulation._GGP.spaceships[ss_id].get('name_en')}: {damage_array.filtered_str} ({percent}%)\n"

        return text

    def _formated_text_of_rocket_per_spaceships(self, id: int, data: dict, priorities: dict) -> str:
        """Returns formated string of Rockets per Spaceships."""

        text = ""
        if id in battlesimulation._GGP.types_rocket and isinstance(data, dict) and isinstance(priorities, dict):
            for ss_id in data:
                number = data[ss_id]
                if ss_id in priorities and isinstance(priorities[ss_id], float):
                    percent = _my_truncate(priorities[ss_id] * 100,2)
                else:
                    percent = "undefined"
                if ss_id in battlesimulation._GGP.types_spaceship and isinstance(number, int):
                    text += f"{battlesimulation._GGP.spaceships[ss_id].get('name_en')}: {number} of {battlesimulation._GGP.rockets[id]['name_en']} ({percent}%)\n"

        return text

    def _is_damage_left(self, damage_array: DamageArray) -> bool:
        """Returns True if there is any non-zero damage in DamageArray."""

        result = False
        if isinstance(damage_array, DamageArray):
            for damage in damage_array:
                if isinstance(damage, Damage):
                    if damage.damage > 0:
                        result = True
        return result

    def _calc_superiority(self, fleet1: SpaceFleet, fleet2: SpaceFleet) -> tuple:
        """Calculates Superiority bonus for the Fleet with more Spaceships (simplified explanation).

            Returns a tuple of two floats: one float is 1.0 (no bonus) and the other is superiority bonus (>= 1.0).
            The first item in tuple is for Fleet 1 and the second is for Fleet 2.
            For example Fleet 2 has really more Spaceships than Fleet 1 and the result will be (1.0, 1.5).
            Bonus cannot be more than 50% (1.5) unless you use custom data.
            Again, this is a bit simplified explanation of Superiority Game mechanic.
        """

        overbonus1 = 1.0
        overbonus2 = 1.0
        if isinstance(fleet1, SpaceFleet) and isinstance(fleet2, SpaceFleet):
            if fleet1.total_defenses == 0 or fleet2.total_defenses == 0:
                return (overbonus1, overbonus2)
            if fleet1.total_defenses > fleet2.total_defenses:
                overbonus1 = (fleet1.total_defenses / fleet2.total_defenses - 1) * battlesimulation._GGP.thold_per + 1
            elif fleet1.total_defenses < fleet2.total_defenses:
                overbonus2 = (fleet2.total_defenses / fleet1.total_defenses - 1) * battlesimulation._GGP.thold_per + 1
            if overbonus1 > battlesimulation._GGP.thold_max:
                overbonus1 = battlesimulation._GGP.thold_max 
            elif overbonus2 > battlesimulation._GGP.thold_max:
                overbonus2 = battlesimulation._GGP.thold_max
        return (overbonus1, overbonus2)

    def _calc_superiority_direct_bonus(self, total_defenses_1: Union[int,float], total_defenses_2: Union[int,float]) -> tuple:
        """Calculates Superiority bonus for the Fleet with more Spaceships (simplified explanation).

            Returns a tuple of two floats: one float is 1.0 (no bonus) and the other is superiority bonus (>= 1.0).
            The first item in tuple is for Fleet 1 and the second is for Fleet 2.
            For example Fleet 2 has really more Spaceships than Fleet 1 and the result will be (1.0, 1.5).
            Bonus cannot be more than 50% (1.5) unless you use custom data.
            Again, this is a bit simplified explanation of Superiority Game mechanic.
        """

        overbonus1 = 0.0
        overbonus2 = 0.0
        if (isinstance(total_defenses_1, int) or isinstance(total_defenses_1, float)) and total_defenses_1 >= 0 and \
                (isinstance(total_defenses_2, int) or isinstance(total_defenses_2, float)) and total_defenses_2 >= 0:
            if total_defenses_1 == 0 or total_defenses_2 == 0:
                return (overbonus1, overbonus2)
            if total_defenses_1 > total_defenses_2:
                overbonus1 = (total_defenses_1 / total_defenses_2 - 1) * battlesimulation._GGP.thold_per
            elif total_defenses_1 < total_defenses_2:
                overbonus2 = (total_defenses_2 / total_defenses_1 - 1) * battlesimulation._GGP.thold_per
            if overbonus1 > battlesimulation._GGP.thold_max:
                overbonus1 = battlesimulation._GGP.thold_max - 1
            elif overbonus2 > battlesimulation._GGP.thold_max:
                overbonus2 = battlesimulation._GGP.thold_max - 1
        return (overbonus1, overbonus2)

    def _finalize_bonuses_mods(self, fleet1: SpaceFleet, fleet2: SpaceFleet = None, \
            sequence: tuple = ("module","superiority","damage"), \
            combination_method_for_mods: tuple = ("add", "add", "multiply"), \
            truncate_to: int = 6) -> None:
        """Combines bonuses from Modules with from Modules attack/defense damage specific and with superiority bonus.

            You can change order and method of combinations.
            Also if you omit Fleet 2, bonuses for Fleet 1 will be combined without superiority.
        """

        if isinstance(sequence, tuple) and len(sequence) == 3 and "module" in sequence \
                and "superiority" in sequence and "damage" in sequence:
            # ok
            pass
        else:
            # set the defaults
            debug_print("Invalid input for sequence. Using defaults.")
            sequence = ("module","superiority","damage")
        if isinstance(combination_method_for_mods, tuple) and len(combination_method_for_mods) == 3:
            for item in combination_method_for_mods:
                if item not in ("add","multiply"):
                    # set the defaults
                    debug_print("Invalid input for combination_method_for_mods. Using defaults.")
                    combination_method_for_mods = ("add", "add", "multiply")
                    break
        else:
            # set the defaults
            debug_print("Invalid input for combination_method_for_mods. Using defaults.")
            combination_method_for_mods = ("add", "add", "multiply")
        if isinstance(fleet1, SpaceFleet) and isinstance(fleet2, SpaceFleet):
            superiority = self._calc_superiority(fleet1, fleet2)
            fleet1.modules.calc_final_damage_mods(superiority[0], *combination_method_for_mods, sequence, truncate_to)
            fleet2.modules.calc_final_damage_mods(superiority[1], *combination_method_for_mods, sequence, truncate_to)
        elif isinstance(fleet1, SpaceFleet) and fleet2 is None:
            fleet1.modules.calc_final_damage_mods(1.0, *combination_method_for_mods, sequence, truncate_to)

    def _wrapper_turrets_damage_dealer(self, fleet: SpaceFleet, planet: Planet = None, \
                _turrets_damage_array: DamageArray = None) -> int:
        """Manages dealing Turrets damage to Fleet.

            First, tries to use fleet's nested fleet.incoming_turrets_damage, if it specified and not empty.
            If not tries to get it from Planet instance.
            If not checks if it was passed directly in _turrets_damage_array variable.

            Returns number of recursive calls made.
        """

        turrets_damage_array = None
        if isinstance(fleet, SpaceFleet) and isinstance(fleet.incoming_turrets_damage, DamageArray) and self._is_damage_left(fleet.incoming_turrets_damage):
            turrets_damage_array = fleet.incoming_turrets_damage
        elif isinstance(planet, Planet):
            turrets_damage_array = planet.passive_damage
        elif isinstance(_turrets_damage_array, DamageArray):
            turrets_damage_array = _turrets_damage_array
        if isinstance(fleet, SpaceFleet) and isinstance(turrets_damage_array, DamageArray):

            debug_print("__________________________________________________________________________________")
            debug_print(f"\nStart of Fleet vs Turrets Battle Simulation\n")
            debug_print(f"Fleet: {fleet.filtered_str}")
            debug_print(f"Fleet all mod stats:\n{fleet.modules}")
            debug_print(f"turrets_damage_array: {turrets_damage_array.filtered_str}")

            if self._is_damage_left(turrets_damage_array) and fleet.is_populated:
                if fleet.attack_planet:
                    # ok
                    pass
                else:
                    # SpaceFleet is blockading Planet -> no Turrets damage
                    return 0
            else:
                debug_print(f"\nNothing to do in Fleet vs Turrets")
                debug_print("__________________________________________________________________________________")
                return 0

            # reset fleet._temp_incoming_damage_array with turrets_damage_array
            fleet._temp_incoming_damage_array.set_whole_array((*turrets_damage_array,))

            counter = self._recursive_deal_damage_simple_fleet_vs_damage_array(fleet=fleet, no_superiority_mod=True, counter=1, fleet_str="")

            # setting nested fleet incoming_turrets_damage, for example if no damage left
            # it will be like this [..., Damage: 0.0/20000.0, ...]
            # or this [..., Damage: 1330.0/20000.0, ...]
            # could be used for statistics or anything else
            if isinstance(fleet._temp_incoming_damage_array, DamageArray) and isinstance(fleet.incoming_turrets_damage, DamageArray):
                fleet.incoming_turrets_damage.reset_damage(fleet._temp_incoming_damage_array)
            # fleet._temp_incoming_damage_array is no longer needed

            debug_print(f"\nEnd of Fleet vs Turrets Battle Simulation.\nIt took {counter} recursive iterations to finish.")
            debug_print("__________________________________________________________________________________")
            return counter

    def _wrapper_rockets_damage_dealer(self, fleet: SpaceFleet, planet: Planet = None, \
                _rockets: RocketArray = None, target_blockade: bool = False) -> int:
        """Manages dealing Rockets damage to Fleet.

            First, tries to use Rockets in Planet instance.
            If not checks if it was passed directly in _rockets variable.

            target_blockade: whether Fleet is making an attack (False) on the Planet or a blockade (True).

            Returns number of recursive calls made.
        """

        rockets = None
        if isinstance(planet, Planet):
            rockets = planet.rockets
        elif isinstance(_rockets, RocketArray):
            rockets = _rockets
        if isinstance(fleet, SpaceFleet) and isinstance(rockets, RocketArray) and isinstance(target_blockade, bool):
            
            debug_print("__________________________________________________________________________________")
            debug_print(f"\nStart of Fleet vs Rockets Battle Simulation\n")
            debug_print(f"Fleet: {fleet.filtered_str}")
            debug_print(f"Fleet all mod stats:\n{fleet.modules}")
            debug_print(f"Rockets: {rockets.filtered_str}")
            
            if rockets.is_populated(fleet, target_blockade) and fleet.is_populated:
                # ok
                pass
            else:
                debug_print(f"\nNothing to do in Fleet vs Rockets")
                debug_print("__________________________________________________________________________________")
                return 0

            counter = self._recursive_rockets_damage_dealer(fleet, rockets, target_blockade, 1)
            debug_print(f"Fleet: {fleet.filtered_str}")
            debug_print(f"Rockets: {rockets.filtered_str}")

            text = "\nEnd of Fleet vs Rockets Battle Simulation.\n"
            text += f"It took {counter} recursive iterations to finish."
            debug_print(text)
            debug_print("__________________________________________________________________________________")
            return counter

    def _wrapper_fleet_vs_fleet_damage_dealer(self, fleet1: SpaceFleet, fleet2: SpaceFleet) -> tuple:
        """Manages dealing damage between two Fleets.

            Returns a tuple of two numbers: recursive calls made for each Fleet.
        """

        if isinstance(fleet1, SpaceFleet) and isinstance(fleet2, SpaceFleet):
            if isinstance(fleet1.incoming_damage_array, DamageArray) and self._is_damage_left(fleet1.incoming_damage_array):
                fleet1_incoming_damage_array = fleet1.incoming_damage_array
            else:
                fleet1_incoming_damage_array = fleet2.total_damage
            
            if isinstance(fleet2.incoming_damage_array, DamageArray) and self._is_damage_left(fleet2.incoming_damage_array):
                fleet2_incoming_damage_array = fleet2.incoming_damage_array
            else:
                fleet2_incoming_damage_array = fleet1.total_damage

            fleet1_custom_name = fleet1.custom_name if fleet1.custom_name != "SpaceFleet" else "Fleet 1"
            fleet2_custom_name = fleet2.custom_name if fleet2.custom_name != "SpaceFleet" else "Fleet 2"
            debug_print("__________________________________________________________________________________")
            debug_print(f"\nStart of Fleet vs Fleet Battle Simulation\n")
            debug_print(f"Fleet {fleet1_custom_name}: {fleet1.filtered_str}")
            debug_print(f"Fleet {fleet1_custom_name} all mod stats:\n{fleet1.modules}")
            debug_print(f"Fleet {fleet1_custom_name} incoming damage: {fleet1_incoming_damage_array.filtered_str}")
            debug_print("\n")
            debug_print(f"Fleet {fleet2_custom_name}: {fleet2.filtered_str}")
            debug_print(f"Fleet {fleet2_custom_name} all mod stats:\n{fleet2.modules}")
            debug_print(f"Fleet {fleet2_custom_name} incoming damage: {fleet2_incoming_damage_array.filtered_str}")
            
            if (not self._is_damage_left(fleet1_incoming_damage_array) or not fleet1.is_populated) and \
                    (not self._is_damage_left(fleet2_incoming_damage_array) or not fleet2.is_populated):
                debug_print(f"\nNothing to do in Fleet vs Fleet")
                debug_print("__________________________________________________________________________________")
                return (0,0)

            ### Fleet 1
            debug_print(f"\nFleet {fleet1_custom_name}:\n")

            # reset fleet._temp_incoming_damage_array with fleet1_incoming_damage_array
            fleet1._temp_incoming_damage_array.set_whole_array((*fleet1_incoming_damage_array,))

            counter_1 = self._recursive_deal_damage_simple_fleet_vs_damage_array(fleet=fleet1, no_superiority_mod=False, counter=1, fleet_str=fleet1_custom_name)

            # setting nested fleet incoming_damage_array, for example if no damage left
            # it will be like this [..., Damage: 0.0/20000.0, ...]
            # or this [..., Damage: 1330.0/20000.0, ...]
            # could be used for statistics or anything else
            if isinstance(fleet1._temp_incoming_damage_array, DamageArray) and isinstance(fleet1.incoming_damage_array, DamageArray):
                fleet1.incoming_damage_array.reset_damage(fleet1._temp_incoming_damage_array)
            # fleet._temp_incoming_damage_array is no longer needed

            ### Fleet 2
            debug_print(f"\nFleet {fleet2_custom_name}:\n")

            # reset fleet._temp_incoming_damage_array with fleet2_incoming_damage_array
            fleet2._temp_incoming_damage_array.set_whole_array((*fleet2_incoming_damage_array,))

            counter_2 = self._recursive_deal_damage_simple_fleet_vs_damage_array(fleet=fleet2, no_superiority_mod=False, counter=1, fleet_str=fleet2_custom_name)

            # setting nested fleet incoming_damage_array, for example if no damage left
            # it will be like this [..., Damage: 0.0/20000.0, ...]
            # or this [..., Damage: 1330.0/20000.0, ...]
            # could be used for statistics or anything else
            if isinstance(fleet2._temp_incoming_damage_array, DamageArray) and isinstance(fleet2.incoming_damage_array, DamageArray):
                fleet2.incoming_damage_array.reset_damage(fleet2._temp_incoming_damage_array)
            # fleet._temp_incoming_damage_array is no longer needed

            text = "\nEnd of Fleet vs Fleet Battle Simulation.\n"
            text += f"It took {counter_1} (Fleet {fleet1_custom_name}) and {counter_2} (Fleet {fleet2_custom_name}) recursive iterations to finish."
            debug_print(text)
            debug_print("__________________________________________________________________________________")
            return (counter_1, counter_2)

    def _wrapper_find_suitable_spaceship_to_beat_enemy(self, spaceship_id: int, spaceship_module: ModuleAndBonuses, \
                fleet2: SpaceFleet, planet: Planet, target_blockade: bool = False, fleet1_acc_type: Union[str,int] = "min", \
                var_to_save_spacefleet_1: dict = None) -> tuple:
        """Returns a tuple: (minimum, maximum) amount of Spaceships (passed id).

            var_to_save_spacefleet_1 is used by Context class, you can also manually use it by passing an empty dict and keeping a reference to it.
            The Fleet of found Spaceship after Battle Simulation will be saved there:
            var_to_save_spacefleet_1.update({spaceship_id: (SpaceFleet(min), SpaceFleet(max))})

            For more info check:
            
            _find_suitable_spaceship_to_beat_enemy_minimum

            _find_suitable_spaceship_to_beat_enemy_maximum

            _find_number_of_spaceships_to_neutralize_rockets

            _find_number_of_spaceships_to_absord_turrets_damage
        """

        if isinstance(var_to_save_spacefleet_1, dict):
            var_to_save_spacefleet_1.update({spaceship_id: []})

        full_attack = True
        if spaceship_id in battlesimulation._GGP.types_spaceship and isinstance(spaceship_module, ModuleAndBonuses) and \
                isinstance(fleet2, SpaceFleet) and \
                isinstance(planet, Planet) and isinstance(planet.rockets, RocketArray):
            amount_against_turrets_and_rockets = self._find_number_of_spaceships_to_neutralize_planet_rockets_and_turrets_damage(spaceship_id, \
                    spaceship_module, planet.make_a_copy_of_self(), target_blockade, full_attack)
            amount_against_turrets_and_rockets = _my_truncate(amount_against_turrets_and_rockets, 6)
            minimum_amount = self._find_suitable_spaceship_to_beat_enemy_minimum(spaceship_id, spaceship_module, fleet2, \
                    result_from_turrets_and_rockets=amount_against_turrets_and_rockets, planet=planet, target_blockade=target_blockade, \
                    fleet1_acc_type=fleet1_acc_type, var_to_save_spacefleet_1=var_to_save_spacefleet_1)
            maximum_amount = self._find_suitable_spaceship_to_beat_enemy_maximum(spaceship_id, spaceship_module, fleet2, \
                    result_from_turrets_and_rockets=amount_against_turrets_and_rockets, planet=planet, target_blockade=target_blockade, \
                    fleet1_acc_type=fleet1_acc_type, var_to_save_spacefleet_1=var_to_save_spacefleet_1)
            debug_print(f"\n{battlesimulation._GGP.spaceships[spaceship_id]['name_en']}: {amount_against_turrets_and_rockets=}, {minimum_amount=}, {maximum_amount=}\n")
            #result_min = _my_round_up(amount_against_turrets_and_rockets + minimum_amount)
            # minimum_amount now includes amount needed for turrets and rockets
            result_min = minimum_amount
            result_max = _my_round_up(amount_against_turrets_and_rockets + maximum_amount)
            return (result_min, result_max)

    def _wrapper_find_suitable_spaceship_to_beat_two_subsequent_enemies(self, spaceship_id: int, spaceship_module: ModuleAndBonuses, \
                fleet2: SpaceFleet, fleet3: SpaceFleet, planet: Planet = Planet(), target_blockade: bool = False, \
                fleet1_acc_type: Union[str,int] = "min", var_to_save_spacefleet_1: dict = None) -> tuple:
        """Returns a tuple: (minimum, maximum) amount of Spaceships (passed id).

            var_to_save_spacefleet_1 is used by Context class, you can also manually use it by passing an empty dict and keeping a reference to it.
            The Fleet of found Spaceship after Battle Simulation will be saved there:
            var_to_save_spacefleet_1.update({spaceship_id: (SpaceFleet(min), SpaceFleet(max))})

            For more info check:
            
            _find_suitable_spaceship_to_beat_enemy_minimum

            _find_suitable_spaceship_to_beat_enemy_maximum

            _find_number_of_spaceships_to_neutralize_rockets

            _find_number_of_spaceships_to_absord_turrets_damage
        """

        if spaceship_id in battlesimulation._GGP.types_spaceship and isinstance(spaceship_module, ModuleAndBonuses) and \
                isinstance(fleet2, SpaceFleet) and isinstance(fleet3, SpaceFleet) and isinstance(planet, Planet):
            # any fleet1_acc_type is ok except "random"
            # generate one "random" accuracy here and set it as fixed
            # and User should not use "random" acc_type to find suitable Fleets, because it's not correct
            if fleet1_acc_type == "random":
                ss = Spaceship(spaceship_id)
                fleet1_acc_type = ss.get_accuracy(fleet1_acc_type)
            # vs turrets and rockets
            amount_against_turrets_and_rockets = self._find_number_of_spaceships_to_neutralize_planet_rockets_and_turrets_damage(spaceship_id, \
                    spaceship_module, planet.make_a_copy_of_self(), target_blockade)
            # vs Fleets
            minimum_amount_1 = self._find_suitable_spaceship_to_beat_enemy_minimum(spaceship_id, spaceship_module, fleet3, fleet1_acc_type=fleet1_acc_type)
            if not target_blockade:
                minimum_amount_2 = self._find_suitable_spaceship_to_beat_enemy_minimum(spaceship_id, spaceship_module, fleet2, fleet1_acc_type=fleet1_acc_type)
            else:
                minimum_amount_2 = 0
            maximum_amount_1 = self._find_suitable_spaceship_to_beat_enemy_maximum(spaceship_id, spaceship_module, fleet3, fleet1_acc_type)
            if not target_blockade:
                maximum_amount_2 = self._find_suitable_spaceship_to_beat_enemy_maximum(spaceship_id, spaceship_module, fleet2, fleet1_acc_type)
            else:
                maximum_amount_2 = 0

            # Amounts are found, now we simulate battles to get actual leftovers of Fleets
            debug_print_flag = battlesimulation._debug_printing
            battlesimulation._debug_printing = False
            # Minimum
            fleet3_copy = fleet3.make_a_copy_of_self()
            fleet1 = SpaceFleet()
            fleet1.set_spaceship_in_fleet((spaceship_id, minimum_amount_1))
            fleet1.set_acc_type(fleet1_acc_type)
            fleet1.modules = spaceship_module
            self._finalize_bonuses_mods(fleet1, fleet3_copy)
            fleet1._temp_incoming_damage_array = fleet3_copy.total_damage
            self._recursive_deal_damage_simple_fleet_vs_damage_array(fleet1)
            fleet1.finalize_battle_results()
            minimum_leftover = fleet1.get_spaceship(spaceship_id).quantity
            # Maximum
            fleet3_copy = fleet3.make_a_copy_of_self()
            fleet1.set_spaceship_in_fleet((spaceship_id, maximum_amount_1))
            self._finalize_bonuses_mods(fleet1, fleet3_copy)
            fleet1._temp_incoming_damage_array = fleet3_copy.total_damage
            self._recursive_deal_damage_simple_fleet_vs_damage_array(fleet1)
            fleet1.finalize_battle_results()
            maximum_leftover = fleet1.get_spaceship(spaceship_id).quantity
            battlesimulation._debug_printing = debug_print_flag
            # Results
            debug_print(f"\n{battlesimulation._GGP.spaceships[spaceship_id]['name_en']}:")
            debug_print(f"{minimum_amount_1=} and {minimum_amount_2=} and {minimum_leftover=}")
            debug_print(f"{maximum_amount_1=} and {maximum_amount_2=} and {maximum_leftover=}")

            # finetuning minimum
            if minimum_amount_2 < minimum_leftover:
                result_min = minimum_amount_1
                if amount_against_turrets_and_rockets > minimum_leftover - minimum_amount_2:
                    result_min += amount_against_turrets_and_rockets - (minimum_leftover - minimum_amount_2)
            else:
                result_min = minimum_amount_1 + minimum_amount_2 - minimum_leftover + amount_against_turrets_and_rockets
            # finetuning maximum
            if maximum_amount_2 < maximum_leftover:
                result_max = maximum_amount_1
                if amount_against_turrets_and_rockets > maximum_leftover - maximum_amount_2:
                    result_max += amount_against_turrets_and_rockets - (maximum_leftover - maximum_amount_2)
            else:
                result_max = maximum_amount_1 + maximum_amount_2 - maximum_leftover + amount_against_turrets_and_rockets

            # if var_to_save_spacefleet_1 is specified, do full simulations and add spaceship_id, fleet1 to it
            if isinstance(var_to_save_spacefleet_1, dict):
                debug_print("\nDoing full simulation of found results.\n")
                debug_print_flag = battlesimulation._debug_printing
                battlesimulation._debug_printing = False
                ################
                # Minimum
                planet_copy = planet.make_a_copy_of_self()
                fleet3_copy = fleet3.make_a_copy_of_self()
                fleet3_copy.custom_name = "Minimum Fleet 3"
                fleet1 = SpaceFleet()
                fleet1.set_spaceship_in_fleet((spaceship_id, result_min))
                fleet1.set_acc_type(fleet1_acc_type)
                fleet1.custom_name = f"Minimum Fleet 1 ss_id={spaceship_id}"
                fleet1.modules = spaceship_module
                self._finalize_bonuses_mods(fleet1, fleet3_copy)
                fleet1._temp_incoming_damage_array = fleet3_copy.total_damage
                fleet3_copy._temp_incoming_damage_array = fleet1.total_damage
                self._recursive_deal_damage_simple_fleet_vs_damage_array(fleet1)
                self._recursive_deal_damage_simple_fleet_vs_damage_array(fleet3_copy)
                fleet1.finalize_battle_results()
                fleet3_copy.finalize_battle_results()
                if not target_blockade:
                    self._wrapper_turrets_damage_dealer(fleet1, planet)
                self._recursive_rockets_damage_dealer(fleet1, planet_copy.rockets, target_blockade)
                fleet2_copy = fleet2.make_a_copy_of_self()
                fleet2_copy.custom_name = "Minimum Fleet 2"
                if not target_blockade:
                    self._finalize_bonuses_mods(fleet1, fleet2_copy)
                    fleet1._temp_incoming_damage_array = fleet2_copy.total_damage
                    fleet2_copy._temp_incoming_damage_array = fleet1.total_damage
                    self._recursive_deal_damage_simple_fleet_vs_damage_array(fleet1)
                    self._recursive_deal_damage_simple_fleet_vs_damage_array(fleet2_copy)
                    fleet1.finalize_battle_results()
                    fleet2_copy.finalize_battle_results()
                target_result_minimum = fleet1
                ################
                ################
                # Maximum
                planet_copy = planet.make_a_copy_of_self()
                fleet3_copy = fleet3.make_a_copy_of_self()
                fleet3_copy.custom_name = "Maximum Fleet 3"
                fleet1 = SpaceFleet()
                fleet1.set_spaceship_in_fleet((spaceship_id, result_max))
                fleet1.set_acc_type(fleet1_acc_type)
                fleet1.custom_name = f"Maximum Fleet 1 ss_id={spaceship_id}"
                fleet1.modules = spaceship_module
                self._finalize_bonuses_mods(fleet1, fleet3_copy)
                fleet1._temp_incoming_damage_array = fleet3_copy.total_damage
                fleet3_copy._temp_incoming_damage_array = fleet1.total_damage
                self._recursive_deal_damage_simple_fleet_vs_damage_array(fleet1)
                self._recursive_deal_damage_simple_fleet_vs_damage_array(fleet3_copy)
                fleet1.finalize_battle_results()
                fleet3_copy.finalize_battle_results()
                if not target_blockade:
                    self._wrapper_turrets_damage_dealer(fleet1, planet)
                self._recursive_rockets_damage_dealer(fleet1, planet_copy.rockets, target_blockade)
                fleet2_copy = fleet2.make_a_copy_of_self()
                fleet2_copy.custom_name = "Maximum Fleet 2"
                if not target_blockade:
                    self._finalize_bonuses_mods(fleet1, fleet2_copy)
                    fleet1._temp_incoming_damage_array = fleet2_copy.total_damage
                    fleet2_copy._temp_incoming_damage_array = fleet1.total_damage
                    self._recursive_deal_damage_simple_fleet_vs_damage_array(fleet1)
                    self._recursive_deal_damage_simple_fleet_vs_damage_array(fleet2_copy)
                    fleet1.finalize_battle_results()
                    fleet2_copy.finalize_battle_results()
                target_result_maximum = fleet1
                ################
                var_to_save_spacefleet_1.update({spaceship_id: (target_result_minimum, target_result_maximum)})
                ################
                battlesimulation._debug_printing = debug_print_flag
            return (result_min, result_max)

    def _deal_damage_with_single_rocket(self, fleet: SpaceFleet, rocket: Rocket, counter: int) -> None:
        """Deal damage from single type of Rockets."""

        if isinstance(fleet, SpaceFleet) and isinstance(rocket, Rocket)and isinstance(counter, int):
            debug_print("<-------")
            debug_print(f"\nSingle rocket {rocket.name_en} damage dealing, parent iteration #{counter}")

            debug_print(f"\nStarting: {rocket.filtered_full_str}")
            priorities = fleet.get_priorities_array_for_rockets(rocket)
            debug_print("\nRaw pririties:\n" + str(priorities) + "\n\n")
            rockets_number_per_spaceship = fleet.calc_incoming_rockets_number_per_ship(rocket.quantity, priorities)
            debug_print(f"{self._formated_text_of_rocket_per_spaceships(rocket.id, rockets_number_per_spaceship, priorities)}")
            for ss in fleet:
                if isinstance(ss, Spaceship) and ss.id in rockets_number_per_spaceship and rockets_number_per_spaceship[ss.id] > 0:
                    # superiority is not in effect against turrets (or rockets)
                    def_mod = fleet.modules.final_no_superiority_defense_damage_mods[rocket.damage_type_id]
                    ss_hp = ss.single_hp(rocket.damage_type_id, def_mod)
                    if ss_hp < rocket.damage:
                        actual_damage_value = ss_hp
                    else:
                        actual_damage_value = rocket.damage
                    text = f"\nSingle {ss.name_en} HP {ss_hp} vs {rocket.name_en} single warhead damage {rocket.damage} | "
                    text += f"damage set to {actual_damage_value}"
                    debug_print(text)
                    actual_damage = Damage(rocket.damage_type_id, actual_damage_value * rocket.warheads * rockets_number_per_spaceship[ss.id])
                    debug_print(f"{ss.filtered_str} vs {actual_damage.filtered_str}")
                    ss.take_damage(actual_damage, def_mod)
                    debug_print(f"Result: {ss.filtered_str} vs {actual_damage.filtered_str}")
                    rockets_left = actual_damage.damage / (actual_damage_value * rocket.warheads)
                    debug_print(f"{rockets_left=}")
                    rockets_used = rockets_number_per_spaceship[ss.id] - int(rockets_left)
                    rocket._subtract_value(rockets_used)
            
            debug_print(f"\nEnding: {rocket.filtered_str}\n")
            debug_print("                                                                         -------/>")

    def _recursive_rockets_damage_dealer(self, fleet: SpaceFleet, rockets: RocketArray, \
                target_blockade: bool, counter: int = 1) -> int:
        """Recursive Rockets damage dealer.

            target_blockade -> if fleet is making a blockade (True) or just attacking the planet (False),
            counter should be 1 for the first call.
            Returns counter -> how many recursions it made.

            All battle changes are made in the corresponding class objects.
        """

        if isinstance(fleet, SpaceFleet) and isinstance(rockets, RocketArray) and isinstance(target_blockade, bool) and isinstance(counter, int):
            debug_print("</------------------------------------------------------------------------------->")
            debug_print(f"\nRecursive Fleet vs Rockets iteration {counter}")

            for rocket in rockets:
                if isinstance(rocket, Rocket):
                    if target_blockade:
                        if rocket.attack_type == 1 or rocket.attack_type == 3:
                            self._deal_damage_with_single_rocket(fleet, rocket, 1)
                    else:
                        if rocket.attack_type == 2 or rocket.attack_type == 3:
                            self._deal_damage_with_single_rocket(fleet, rocket, 1)
            
            
            counter += 1

            if rockets.is_populated(fleet, target_blockade) and fleet.is_populated:
                debug_print("<-------------------------------------------------------------------------------/>")
                counter = self._recursive_rockets_damage_dealer(fleet, rockets, target_blockade, counter)
            else:
                debug_print("Recursive Fleet vs Rockets is over\n")
                if counter - 1 == 1:
                    debug_print("<-------------------------------------------------------------------------------/>")
                return counter - 1
            debug_print("<-------------------------------------------------------------------------------/>")
            return counter

    def _recursive_deal_damage_simple_fleet_vs_damage_array(self, fleet: SpaceFleet, \
                no_superiority_mod: bool = False, counter: int = 1, fleet_str: str = "") -> int:
        """Recursive damage dealer to Fleet.

            Deals damage to the Fleet, damage should be specified in fleet._temp_incoming_damage_array.
            No_superiority_mod = True or False. Use True for Fleet vs no Fleet (only case right now is Fleet vs passive turrets damage).
            Counter = 1 for the first call of this func.
            Fleet_str is for debug print for you to identify the Fleet in command line.
            Returns number of iterations of made recursions.
        """

        if isinstance(fleet, SpaceFleet) and isinstance(fleet._temp_incoming_damage_array, DamageArray) and isinstance(counter, int):
            debug_print("</------------------------------------------------------------------------------->")
            debug_print(f"\nRecursive simple fleet {fleet_str} vs damage array iteration {counter}")

            ### Fleet

            debug_print(f"\nFleet {fleet_str} is receiving damage:")
            debug_print(f"\n{fleet.filtered_str}")
            debug_print(f"current incoming damage:\n{fleet._temp_incoming_damage_array.filtered_str}")
            fleet_incoming_damage_per_ship = fleet.calc_incoming_raw_damage_per_ship(fleet._temp_incoming_damage_array)
            text = f"damage by spaceship priorities:\n"
            text += f"{self._formated_text_of_damage_per_spaceships(fleet_incoming_damage_per_ship, fleet.priorities_array)}\n"
            debug_print(text)
            for ss_id in fleet_incoming_damage_per_ship:
                ss = fleet.get_spaceship(ss_id)
                if isinstance(ss, Spaceship):
                    if ss.id == ss_id and isinstance(fleet_incoming_damage_per_ship[ss_id], DamageArray):
                        for damage in fleet_incoming_damage_per_ship[ss_id]:
                            if isinstance(damage, Damage) and damage.damage > 0:
                                if no_superiority_mod:
                                    # superiority is not in effect against turrets (or rockets)
                                    def_mod = fleet.modules.final_no_superiority_defense_damage_mods[damage.damage_type_id]
                                else:
                                    def_mod = fleet.modules.final_defense_damage_mods[damage.damage_type_id]
                                debug_print(f"\n{ss.filtered_str} vs {damage.filtered_str}")
                                ss.take_damage(damage, def_mod)
                                debug_print(f"Result:\n{ss.filtered_str} vs {damage.filtered_str}")
            # discarded:
            # this will not save over original damage value
            #fleet._temp_incoming_damage_array = fleet.sum_up_leftover_damage(fleet_incoming_damage_per_ship)
            # 
            # this will save original damage values over iterations
            # target_array is our temp array
            fleet.sum_up_leftover_damage(fleet_incoming_damage_per_ship, target_array=fleet._temp_incoming_damage_array)
            debug_print(f"\nLeftover Fleet {fleet_str}:\n{fleet.filtered_str}")
            debug_print(f"Overall Fleet {fleet_str} leftover incoming damage:\n{fleet._temp_incoming_damage_array.filtered_str}")
            debug_print("\n")

            ### Check the need for one more recursion

            counter += 1

            if self._is_damage_left(fleet._temp_incoming_damage_array) and fleet.is_populated:
                debug_print("<-------------------------------------------------------------------------------/>")
                counter = self._recursive_deal_damage_simple_fleet_vs_damage_array(fleet, no_superiority_mod, counter, fleet_str)
            else:
                debug_print(f"Recursive simple fleet {fleet_str} vs damage array is over\n")
                if counter - 1 == 1:
                    debug_print("<-------------------------------------------------------------------------------/>")
                return counter - 1
            debug_print("<-------------------------------------------------------------------------------/>")
            return counter

    def _equilibrium_finder(self, damage_1: float, damage_increment_1: float, \
                total_defenses_1: Union[int,float], single_spaceship_defenses_1: int, total_defenses_2: Union[int,float], \
                particular_defenses_2: Union[int,float], defense_mod_2: float, \
                counter: int = 0, superiority_combination_type: str = "add") -> int:
        """Adds 1 spaceship to the pool 1: increases damage, decreases superiority.

            Suffix 1 for Fleet 1, 2 for Fleet 2.
            particular_defenses_2 is the total defense of Fleet 2 against only one specified damage type.
            Recalculates total HP, checks if new damage is enough.
            Returns number of recursions made == number of spaceships added.
        """

        if superiority_combination_type not in ("add", "multiply"):
            superiority_combination_type = "add"
        while True:
            superiority = self._calc_superiority_direct_bonus(total_defenses_1, total_defenses_2)
            if superiority_combination_type == "add":
                defense_mod_with_superiority = defense_mod_2 + superiority[1]
            else:
                defense_mod_with_superiority = defense_mod_2 * (1 + superiority[1])
            total_hp_2 = _my_truncate(particular_defenses_2 * defense_mod_with_superiority, 6)
            if damage_1 >= total_hp_2:
                break
            counter += 1
            damage_1 += damage_increment_1
            total_defenses_1 += single_spaceship_defenses_1
        return counter

    def _equilibrium_finder_only_damage(self, damage_1: float, damage_increment_1: float, \
                total_hp_2: Union[int,float], counter: int = 0) -> int:
        """Adds 1 spaceship to the pool 1: increases damage only.

            Suffix 1 for Fleet 1, 2 for Fleet 2.
            Returns number of recursions made == number of spaceships added.
        """

        while True:
            if damage_1 >= total_hp_2:
                break
            counter += 1
            damage_1 += damage_increment_1
        return counter

    def _find_suitable_spaceship_to_beat_enemy_minimum(self, spaceship_id: int, \
                spaceship_module: ModuleAndBonuses, fleet2: SpaceFleet, \
                superiority_combination_type: str = "add", fleet1_acc_type: Union[str,int] = "min", \
                result_from_turrets_and_rockets: float = 0.0, planet: Planet = Planet(), \
                target_blockade: bool = False, var_to_save_spacefleet_1: dict = None) -> int:
        """Returns final approximate minimal amount of spaceships (passed id) to beat enemy, Planet's defenses are included here if you pass them.

            The result is approximate, so you should always increase this number a little bit, unless you are an advanced user.
            result_from_turrets_and_rockets is the float result from _find_number_of_spaceships_to_neutralize_planet_rockets_and_turrets_damage.
        """

        if not fleet2.is_populated:
            return _my_round_up(0 + result_from_turrets_and_rockets)

        if isinstance(var_to_save_spacefleet_1, dict):
            if spaceship_id not in var_to_save_spacefleet_1:
                var_to_save_spacefleet_1.update({spaceship_id: []})
            else:
                if not isinstance(var_to_save_spacefleet_1[spaceship_id], list):
                    var_to_save_spacefleet_1.update({spaceship_id: []})

        if superiority_combination_type not in ("add", "multiply"):
            # invalid type, use default "add"
            superiority_combination_type = "add"

        if spaceship_id in battlesimulation._GGP.types_spaceship and isinstance(spaceship_module, ModuleAndBonuses) and \
                isinstance(fleet2, SpaceFleet):
            ss = Spaceship(spaceship_id)

            if isinstance(fleet1_acc_type, int) and 0 < fleet1_acc_type <= 100:
                ss_accuracy = fleet1_acc_type
            else:
                ss_accuracy = ss.get_accuracy(fleet1_acc_type)

            ss_dt = ss.damage_type_id
            mod_1 = spaceship_module
            mod_2 = fleet2.modules
            mod_1.calc_final_damage_mods(1.0)
            mod_2.calc_final_damage_mods(1.0)
            last_non_zero_spaceship_2 = 1
            for ss_2 in fleet2:
                if isinstance(ss_2, Spaceship) and ss_2.quantity:
                    last_non_zero_spaceship_2 = ss_2.id
            # we need to destroy at lease half of the last non-zero spaceship
            # because of Game mechanics, after the battle that less-than-half part will be rounded to zero
            # default threshold is 0.5, so we subtract this number
            fleet2.get_spaceship(last_non_zero_spaceship_2).quantity -= battlesimulation._GGP.threshold
            debug_print(f"\n{battlesimulation._GGP.spaceships[spaceship_id]['name_en']}: {fleet2.filtered_str} (.5 of Spaceship is intended)")
            # we need at least first_approach_quantity Spaceships to negate enemy's total HP, which is
            # total defense (of "spaceship_id"'s damage type) * by Module's bonus without Superiority mechanic
            particular_defenses_2 = fleet2.total_hp_for_defense_type(ss_dt)
            total_hp_to_beat = particular_defenses_2 * mod_2.final_no_superiority_defense_damage_mods[ss_dt]
            first_approach_quantity = total_hp_to_beat / (ss.attack * mod_1.final_attack_damage_mods[ss_dt] * ss_accuracy / 100)
            first_approach_quantity = _my_truncate(first_approach_quantity, 6)
            debug_print(f"{first_approach_quantity=}")
            # damage of Fleet 1 and of single spaceship is decreased by accuracy
            fleet_1_damage = first_approach_quantity * ss.attack * mod_1.final_attack_damage_mods[ss_dt] * ss.accuracy / 100
            damage_increment = ss.attack * mod_1.final_attack_damage_mods[ss_dt] * ss_accuracy / 100
            fleet_1_damage = _my_truncate(fleet_1_damage, 6)
            damage_increment = _my_truncate(damage_increment, 6)
            # we need total defenses of our first approach quantity to include Superiority mechanic
            single_spaceship_defenses = ss.total_defense_single_spaceship
            total_defenses_1 = single_spaceship_defenses * first_approach_quantity

            # call func, which adds 1 Spaceship to Fleet 1 and recalculates Fleet 2 Total HP with Superiority mechanic
            # untill Fleet 1 has enough damage to destroy Fleet 2
            to_add_spaceships = self._equilibrium_finder(fleet_1_damage, damage_increment, \
                    total_defenses_1, single_spaceship_defenses, fleet2.total_defenses, particular_defenses_2, \
                    mod_2.final_no_superiority_defense_damage_mods[ss_dt], 0, superiority_combination_type)
            # add that number to first approach, but subtract 1 spaceship for additional fine-tuning
            semifinal_result = first_approach_quantity + to_add_spaceships - 1
            #debug_print(f"semifinal with one less spaceship {to_add_spaceships=}: {semifinal_result=}")

            debug_print_flag = battlesimulation._debug_printing
            battlesimulation._debug_printing = False
            # round up 0.5 spaceship back to 1 before Simulation
            fleet2.get_spaceship(last_non_zero_spaceship_2).quantity = _my_round_up(fleet2.get_spaceship(last_non_zero_spaceship_2).quantity)
            fleet1 = SpaceFleet()
            fleet1.set_acc_type(ss_accuracy)
            fleet1.modules = spaceship_module
            # fine-tuning is made by full Battle Simulation
            while True:
                fleet2_copy = fleet2.make_a_copy_of_self()
                # include result for turrets and rockets and round all up (math.ceil)
                final_result = _my_round_up(semifinal_result + result_from_turrets_and_rockets)
                # reset Fleet 1 with new number
                fleet1.set_spaceship_in_fleet((spaceship_id, final_result))
                # do turrets damage if not blockade
                if not target_blockade:
                    fleet1._temp_incoming_damage_array = planet.passive_damage
                    self._recursive_deal_damage_simple_fleet_vs_damage_array(fleet1, True)
                # do appropriate rockets damage
                self._recursive_rockets_damage_dealer(fleet1, planet.rockets.make_a_copy_of_self(), target_blockade, 1)
                # finalize bonuses here, because Superiority needs quantity of Spaceships after they took damage from turrets and rockets
                # or rephrasing amount of Spaceships left alive
                self._finalize_bonuses_mods(fleet1, fleet2_copy)
                fleet1._temp_incoming_damage_array = fleet2_copy.total_damage
                fleet2_copy._temp_incoming_damage_array = fleet1.total_damage
                self._recursive_deal_damage_simple_fleet_vs_damage_array(fleet2_copy)
                # round up quantities of Spaceships by Game mechanic (0.49 -> 0 survived, 0.5 -> 1 survived)
                fleet2_copy.finalize_battle_results()
                # if there are Spaceships left in Fleet 2, add one more Spaceship to Fleet 1
                if fleet2_copy.is_populated:
                    semifinal_result += 1
                else:
                    # if var_to_save_spacefleet_1 was passed to func, deal damage to Fleet 1, round up and save Fleet 1 in var
                    if isinstance(var_to_save_spacefleet_1, dict):
                        self._recursive_deal_damage_simple_fleet_vs_damage_array(fleet1)
                        fleet1.finalize_battle_results()
                        var_to_save_spacefleet_1[spaceship_id].append(fleet1)
                    break

            battlesimulation._debug_printing = debug_print_flag
            debug_print(f"{battlesimulation._GGP.spaceships[spaceship_id]['name_en']}: {final_result=}\n")
            return final_result

    def _find_suitable_spaceship_to_beat_enemy_maximum(self, spaceship_id: int, \
                spaceship_module: ModuleAndBonuses, fleet2: SpaceFleet, \
                fleet1_acc_type: Union[str,int] = None, \
                result_from_turrets_and_rockets: float = 0.0, planet: Planet = Planet(), \
                target_blockade: bool = False, var_to_save_spacefleet_1: dict = None) -> int:
        """Returns amount of spaceships (passed id) to beat enemy with less casualties due to max Superiority bonus."""

        result_from_turrets_and_rockets = _my_round_up(result_from_turrets_and_rockets)

        if isinstance(var_to_save_spacefleet_1, dict):
            if spaceship_id not in var_to_save_spacefleet_1:
                var_to_save_spacefleet_1.update({spaceship_id: []})
            else:
                if not isinstance(var_to_save_spacefleet_1[spaceship_id], list):
                    var_to_save_spacefleet_1.update({spaceship_id: []})

        if spaceship_id in battlesimulation._GGP.types_spaceship and isinstance(spaceship_module, ModuleAndBonuses) and \
                isinstance(fleet2, SpaceFleet):
            ss = Spaceship(spaceship_id)

            if isinstance(fleet1_acc_type, int) and 0 < fleet1_acc_type <= 100:
                ss_accuracy = fleet1_acc_type
            else:
                ss_accuracy = ss.get_accuracy(fleet1_acc_type)

            # this method is easier to calculate, because we immediately set first approach quantity to have max Superiority bonus
            ss_dt = ss.damage_type_id
            total_defenses_1 = fleet2.total_defenses * 5
            single_spaceship_defenses = ss.total_defense_single_spaceship
            first_approach_quantity = _my_round_up(total_defenses_1 / single_spaceship_defenses)
            mod_1 = spaceship_module
            mod_2 = fleet2.modules
            mod_1.calc_final_damage_mods(battlesimulation._GGP.thold_max)       # default is 1.5
            mod_2.calc_final_damage_mods(1.0)
            total_hp_to_beat = fleet2.total_hp_for_defense_type(ss_dt) * mod_2.final_defense_damage_mods[ss_dt]
            fleet_1_damage = first_approach_quantity * ss.attack * ss_accuracy / 100

            # we only need to check if damage is enough, and if not add spaceships by one until it is
            if fleet_1_damage >= total_hp_to_beat:
                final_result = first_approach_quantity
            else:
                damage_increment = ss.attack * mod_1.final_attack_damage_mods[ss_dt] * ss_accuracy / 100
                to_add_spaceships = self._equilibrium_finder_only_damage(fleet_1_damage, damage_increment, total_hp_to_beat, 0)
                final_result = first_approach_quantity + to_add_spaceships

            # if var_to_save_spacefleet_1 was passed to func, do full Simulation and save Fleet 1 in var
            if isinstance(var_to_save_spacefleet_1, dict):
                debug_print_flag = battlesimulation._debug_printing
                battlesimulation._debug_printing = False
                fleet1 = SpaceFleet()
                fleet2_copy = fleet2.make_a_copy_of_self()
                fleet1.set_spaceship_in_fleet((spaceship_id, final_result + result_from_turrets_and_rockets))
                fleet1.acc_type = fleet1_acc_type
                fleet1.modules = spaceship_module
                self._finalize_bonuses_mods(fleet1, fleet2_copy)
                if not target_blockade:
                    fleet1._temp_incoming_damage_array = planet.passive_damage
                    self._recursive_deal_damage_simple_fleet_vs_damage_array(fleet1, True)
                self._recursive_rockets_damage_dealer(fleet1, planet.rockets.make_a_copy_of_self(), target_blockade, 1)
                self._finalize_bonuses_mods(fleet1, fleet2_copy)
                fleet1._temp_incoming_damage_array = fleet2_copy.total_damage
                self._recursive_deal_damage_simple_fleet_vs_damage_array(fleet1)
                fleet1.finalize_battle_results()
                var_to_save_spacefleet_1[spaceship_id].append(fleet1)
                battlesimulation._debug_printing = debug_print_flag

            return final_result
                    
    def _find_number_of_spaceships_to_absord_turrets_damage(self, spaceship_id: int, \
                spaceship_module: ModuleAndBonuses, planet: Planet) -> float:
        """Returns amount of spaceships (passed id) equal to Turrets damage output."""

        total_spaceships_destroyed = 0.0
        if spaceship_id in battlesimulation._GGP.types_spaceship and isinstance(spaceship_module, ModuleAndBonuses) and \
                isinstance(planet, Planet):
            ss = Spaceship(spaceship_id)
            spaceship_module.calc_final_damage_mods(1.0)
            turret_damage_type_id = planet.turret_damage_type_id
            total_damage = planet.passive_damage.get_damage(turret_damage_type_id).damage
            def_mod = spaceship_module.final_no_superiority_defense_damage_mods[turret_damage_type_id]
            ss_hp = ss.single_hp(turret_damage_type_id, def_mod)
            # this is simply total damage of turrets divided by single Spaceship HP for that defense type, nothing to elaborate here
            total_spaceships_destroyed = _my_truncate(total_damage / ss_hp, 6)
        return total_spaceships_destroyed

    def _find_number_of_spaceships_to_neutralize_rockets(self, spaceship_id: int, \
                spaceship_module: ModuleAndBonuses, rockets: RocketArray, \
                target_blockade: bool = False, result_from_turrets: float = 0.0, full_attack: bool = False) -> float:
        """Returns amount of spaceships (passed id) needed to fully neutralize rockets.

            result_from_turrets is the result from _find_number_of_spaceships_to_absord_turrets_damage.

            But if you do a full attack on the Planet a little more spaceships will be destroyed by rockets,
            so pass full_attack=True for better result.
        """

        if result_from_turrets:
            result_from_turrets = result_from_turrets % int(result_from_turrets) if result_from_turrets >= 1 else result_from_turrets
            #result_from_turrets = _my_truncate(1 - result_from_turrets, 6)
        total_spaceships_destroyed = 0.0
        if spaceship_id in battlesimulation._GGP.types_spaceship and isinstance(spaceship_module, ModuleAndBonuses) and \
                isinstance(rockets, RocketArray):
            ss = Spaceship(spaceship_id)
            spaceship_module.calc_final_damage_mods(1.0)
            for rocket in rockets:
                if isinstance(rocket, Rocket):
                    if spaceship_id not in rocket.valid_targets:
                        continue
                    if rocket.quantity < 1:
                        continue
                    if target_blockade:
                        if rocket.attack_type not in (1,3):
                            continue
                    else:
                        if rocket.attack_type not in (2,3):
                            continue
                    # superiority is not in effect against turrets (or rockets)
                    def_mod = spaceship_module.final_no_superiority_defense_damage_mods[rocket.damage_type_id]
                    ss_hp = ss.single_hp(rocket.damage_type_id, def_mod)
                    # Rocket cannot deal more base damage than there is defense of single Spaceship
                    flag_to_cap_damage = True if rocket.damage >= ss_hp else False
                    # so we cap it
                    # which results in 1 warhead destroying exactly one Spaceship
                    capped_damage_value = ss_hp if flag_to_cap_damage else rocket.damage
                    single_rocket_damage = capped_damage_value * rocket.warheads
                    actual_damage = single_rocket_damage * rocket.quantity
                    ss_destroyed = actual_damage / ss_hp

                    # if damage was not capped, we can add previous result from turrets
                    # result_from_turrets - 1 -> because result is how many will be destroyed, not how many were left Alive
                    if result_from_turrets and not flag_to_cap_damage:
                        ss_destroyed += result_from_turrets - 1
                        result_from_turrets = 0
                    # if we don't need Spaceships to survive after turrets and rockets, than
                    # we need a little less of them, because once rocket's first warhead is fired,
                    # all the rest warheads are fired too, even if there are no more Spaceships to target
                    # for full attack we can't do that
                    if not full_attack:
                        if ss_hp < capped_damage_value:
                            damage_div_hp = capped_damage_value // ss_hp
                            damage_mod_hp = capped_damage_value % ss_hp
                            if damage_mod_hp:
                                to_subtract_spaceships = damage_div_hp
                            else:
                                to_subtract_spaceships = damage_div_hp - 1
                            ss_destroyed -= to_subtract_spaceships
                    total_spaceships_destroyed += ss_destroyed
        total_spaceships_destroyed = _my_truncate(total_spaceships_destroyed, 6)
        return total_spaceships_destroyed

    def _find_number_of_spaceships_to_neutralize_planet_rockets_and_turrets_damage(self, \
                spaceship_id: int, spaceship_module: ModuleAndBonuses, planet: Planet, \
                target_blockade: bool = False, full_attack: bool = False) -> Union[int,float]:
        """Returns amount of spaceships (passed id) needed to absorb all damage from Planet.

            But if you do a full attack on the Planet a little more spaceships will be destroyed by turrets and rockets,
            so pass full_attack=True for better result.
        """

        if spaceship_id in battlesimulation._GGP.types_spaceship and isinstance(spaceship_module, ModuleAndBonuses) and \
                isinstance(planet, Planet) and isinstance(planet.rockets, RocketArray):
            if target_blockade:
                against_turrets = 0
            else:
                against_turrets = self._find_number_of_spaceships_to_absord_turrets_damage(spaceship_id, spaceship_module, planet)
            against_rockets = self._find_number_of_spaceships_to_neutralize_rockets(spaceship_id, spaceship_module, planet.rockets.make_a_copy_of_self(), target_blockade, against_turrets, full_attack)
            debug_print(f"\n{battlesimulation._GGP.spaceships[spaceship_id]['name_en']}: {against_turrets=}, {against_rockets=}")
            # this is a wrapper func used in _wrapper_find_suitable_spaceship_to_beat_enemy and _wrapper_find_suitable_spaceship_to_beat_two_subsequent_enemies
            # so for full attack we need float quantities
            # otherwise round up them here
            if full_attack:
                result = against_turrets + against_rockets
            else:
                result = _my_round_up(against_turrets + against_rockets)
            return result

    def _get_basic_vars_for_old_bombardment(self, spaceship_module: ModuleAndBonuses, planet: Planet) -> dict:
        """Old Bombardment Mechanic, returns a dict with values of Planetary Defenses."""

        if isinstance(spaceship_module, ModuleAndBonuses) and isinstance(planet, Planet) and \
                isinstance(planet.rockets, RocketArray) and isinstance(planet.buildings, BuildingArray):
            # calculate Valkyries needed to pass Turrets and Rockets
            spaceship_module.calc_final_damage_mods(1.0)
            valkyrie_dead_by_turrets = self._find_number_of_spaceships_to_absord_turrets_damage(7, spaceship_module, planet)
            valkyrie_dead_by_rockets = self._find_number_of_spaceships_to_neutralize_rockets(7, spaceship_module, \
                    planet.rockets.make_a_copy_of_self(), full_attack=True)

            shield_generator_defenses = 0
            shield_level = 0
            turrets_defenses = 0
            the_rest_buildings_defenses = 0
            for building in planet.buildings:
                if isinstance(building, Building):
                    if building.id == 9:
                        turrets_defenses += building.level * building.defense
                    elif building.id == 10:
                        shield_generator_defenses += building.level * building.defense
                        shield_level = building.level
                    else:
                        the_rest_buildings_defenses += building.level * building.defense
            debug_print(f"\nPlanet's structured defenses: Shield Generator={shield_generator_defenses}, Turrets={turrets_defenses}, the rest={the_rest_buildings_defenses}\n")
            debug_print(f"{valkyrie_dead_by_turrets=}, {valkyrie_dead_by_rockets=}\n")
            result = {"valkyrie_dead_by_turrets": valkyrie_dead_by_turrets, "valkyrie_dead_by_rockets": valkyrie_dead_by_rockets, \
                    "shield_generator_defenses": shield_generator_defenses, "turrets_defenses": turrets_defenses, \
                    "the_rest_buildings_defenses": the_rest_buildings_defenses, "shield_level": shield_level}
            return result

    def simulate(self, fleet1: SpaceFleet, fleet2: SpaceFleet, planet: Planet, target_blockade: bool = False) -> bool:
        """Simulate Battle between Fleets, acknowledging Planet's conditions.

            It's more like an example of usage. For your convinience, you should use Context class.
            This particular func simulates simple situation, where Fleet 1 is attacking or blockading Planet:
            Planet can have Turrets and Rockets and defenders: Fleet 2.
            
            If type is Fleet 1 is attacking Planet then Fleet 2 is considered to be on the Planet.

            Else type is Fleet 1 is going to blockade Planet then Fleet 2 is condsidered to be someone else's Fleet already blockading Planet.
        """

        result = False
        if isinstance(fleet1, SpaceFleet) and isinstance(fleet2, SpaceFleet) \
                and isinstance(planet, Planet):      # and isinstance(context, Context):
            
            # finalize bonuses from modules and damage type (commander in the future) bonuses
            self._finalize_bonuses_mods(fleet1, fleet2)
            
            debug_print("\n####################################################################\n")

            counter_1 = 0
            counter_2 = 0
            counter_3_tuple = (0,0)
            if target_blockade:

                debug_print("\n")
                debug_print("##################################")
                debug_print("Fleet vs Fleet Battle Simulation")
                debug_print("##################################")
                fleet1.incoming_damage_array = fleet2.total_damage
                fleet2.incoming_damage_array = fleet1.total_damage
                counter_3_tuple = self._wrapper_fleet_vs_fleet_damage_dealer(fleet1=fleet1, fleet2=fleet2)


                debug_print("\n\n")
                debug_print("##################################")
                debug_print("Fleet vs Rockets Battle Simulation")
                debug_print("##################################")
                counter_2 = self._wrapper_rockets_damage_dealer(fleet=fleet1, planet=planet, target_blockade=target_blockade)


            else:
                debug_print("\n")
                debug_print("##################################")
                debug_print("Fleet vs Turrets Battle Simulation")
                debug_print("##################################")
                counter_1 = self._wrapper_turrets_damage_dealer(fleet=fleet1, planet=planet)


                debug_print("\n\n")
                debug_print("##################################")
                debug_print("Fleet vs Rockets Battle Simulation")
                debug_print("##################################")
                counter_2 = self._wrapper_rockets_damage_dealer(fleet=fleet1, planet=planet, target_blockade=target_blockade)


                debug_print("\n")
                debug_print("##################################")
                debug_print("Fleet vs Fleet Battle Simulation")
                debug_print("##################################")
                # need to finalize mods again, because Fleet contents (spaceship quantity) did change. Needed for Superiority mechanic
                self._finalize_bonuses_mods(fleet1, fleet2)
                fleet1.incoming_damage_array = fleet2.total_damage
                fleet2.incoming_damage_array = fleet1.total_damage
                counter_3_tuple = self._wrapper_fleet_vs_fleet_damage_dealer(fleet1=fleet1, fleet2=fleet2)
                fleet1.finalize_battle_results()
                fleet2.finalize_battle_results()
            
            debug_print("\n\n##################################\n")
            
            text = f"\n\nBattle simulation is over.\n"
            text += f"Fleet vs Turrets took {counter_1} recursive iterations to finish.\n"
            text += f"Fleet vs Rockets took {counter_2} recursive iterations to finish.\n"
            text += f"Fleet vs Fleet took {counter_3_tuple[0]} (Fleet 1) and {counter_3_tuple[1]} (Fleet 2) recursive iterations to finish.\n"
            debug_print(text)

            debug_print("\n")
            debug_print(f"1: {fleet1.filtered_original_str}")
            debug_print(f"1: {fleet1.filtered_alive_str}")
            debug_print(f"1: {fleet1.filtered_dead_str}")
            debug_print("\n")
            debug_print(f"2: {fleet2.filtered_original_str}")
            debug_print(f"2: {fleet2.filtered_alive_str}")
            debug_print(f"2: {fleet2.filtered_dead_str}")
            debug_print("\n\n")
            debug_print(f"1: {fleet1.modules}")
            debug_print(f"2: {fleet2.modules}")
            debug_print("\n\n")
            
            debug_print("\n####################################################################\n")

            result = True
        return result

    def find_suitable_fleets_to_beat_enemy(self, spaceship_module: ModuleAndBonuses, \
                fleet2: SpaceFleet, planet: Planet, target_blockade: bool = False, fleet1_acc_type: Union[str,int] = "min", \
                list_of_spaceships_ids_to_use: Union[list,tuple] = (3,4,5,6,9), var_to_save_spacefleet_1: dict = None) -> dict:
        """Tries to find suitable Spaceships to beat passed Fleet with passed Planet (turrets and rockets are accounted).

            list_of_spaceships_ids_to_use -> will find suitable Spaceships for the specified ids.
            If passed as None, all Spaceship Ids will be used.

            Returns a dictionary with keys as ids of corresponding Spaceships, i.e. (3,4,5,6,9),
            for each key the value is a tuple of two values 
            (amount of Spaceships) for minimum and maximum methods. Also saves Fleet after Simulation in passed dict "var_to_save_spacefleet_1".

            For example returned dict could be: {3: (5, 25), 4: (4, 20), 5: (3, 15), 6: (2, 10), 9: (1, 5)}

            Because it returns many Spaceships variants, it is up to you to decide which one is more suitable, convinient, etc to you.

            Minimum and Maximum means:

            min - approximate minimal ammount to do the job
            assuming the RNG gives minimal accuracy to you and maximum accuracy to your enemy (the worst case scenario),

            max - the amount of Spaceships when you receive the maximum Superiority bonus (50%) and thus
            you have less casualties than in "min" case, but the RNG still gives your enemy max accuracy.
        """

        if list_of_spaceships_ids_to_use is None:
            list_of_spaceships_ids_to_use = battlesimulation._GGP.types_spaceship

        if isinstance(list_of_spaceships_ids_to_use, list) or isinstance(list_of_spaceships_ids_to_use, tuple):
            for ss_id in list_of_spaceships_ids_to_use:
                if ss_id not in battlesimulation._GGP.types_spaceship:
                    return {}
        else:
            return {}

        result = {}
        if isinstance(spaceship_module, ModuleAndBonuses) and isinstance(fleet2, SpaceFleet) and \
                isinstance(planet, Planet) and isinstance(planet.rockets, RocketArray):
            for ss_id in list_of_spaceships_ids_to_use:
                semi_result = self._wrapper_find_suitable_spaceship_to_beat_enemy(ss_id, spaceship_module, fleet2, planet, target_blockade, \
                        fleet1_acc_type, var_to_save_spacefleet_1)
                result.update({ss_id: semi_result})

        return result

    def find_suitable_fleets_to_beat_two_subsequent_enemies(self, spaceship_module: ModuleAndBonuses, \
                fleet2: SpaceFleet, fleet3: SpaceFleet, planet: Planet = Planet(), target_blockade: bool = False, \
                fleet1_acc_type: Union[str,int] = "min", list_of_spaceships_ids_to_use: Union[list,tuple] = (3,4,5,6,9), \
                var_to_save_spacefleet_1: dict = None) -> dict:
        """Tries to find suitable Spaceships to beat passed Fleet with passed Planet (turrets and rockets are accounted).

            list_of_spaceships_ids_to_use -> will find suitable Spaceships for the specified ids.
            If passed as None, all Spaceship Ids will be used.

            Returns a dictionary with keys as ids of corresponding Spaceships, i.e. (3,4,5,6,9),
            for each key the value is a tuple of two values 
            (amount of Spaceships) for minimum and maximum methods. Also saves Fleet after Simulation in passed dict "var_to_save_spacefleet_1".

            For example returned dict could be: {3: (5, 25), 4: (4, 20), 5: (3, 15), 6: (2, 10), 9: (1, 5)}

            Because it returns many Spaceships variants, it is up to you to decide which one is more suitable, convinient, etc to you.

            Minimum and Maximum means:

            min - approximate minimal ammount to do the job
            assuming the RNG gives minimal accuracy to you and maximum accuracy to your enemy (the worst case scenario),

            max - the amount of Spaceships when you receive the maximum Superiority bonus (50%) and thus
            you have less casualties than in "min" case, but the RNG still gives your enemy max accuracy.
        """

        if list_of_spaceships_ids_to_use is None:
            list_of_spaceships_ids_to_use = battlesimulation._GGP.types_spaceship

        if isinstance(list_of_spaceships_ids_to_use, list) or isinstance(list_of_spaceships_ids_to_use, tuple):
            for ss_id in list_of_spaceships_ids_to_use:
                if ss_id not in battlesimulation._GGP.types_spaceship:
                    return {}
        else:
            return {}

        result = {}
        if isinstance(spaceship_module, ModuleAndBonuses) and isinstance(fleet2, SpaceFleet) and isinstance(fleet3, SpaceFleet):
            for ss_id in list_of_spaceships_ids_to_use:
                semi_result = self._wrapper_find_suitable_spaceship_to_beat_two_subsequent_enemies(ss_id, spaceship_module, \
                        fleet2, fleet3, planet, target_blockade, fleet1_acc_type, var_to_save_spacefleet_1)
                result.update({ss_id: semi_result})

        return result

    def select_top_results_to_beat_enemy(self, results_from_find_suitable_fleets_to_beat_enemy: dict, \
                fleet_results: dict, add_departure_cost: int = 2, \
                coef_for_cost: float = 1.0, coef_for_time: float = 1.0, \
                top_length: int = 5) -> dict:
        """Selects best results by energy cost and build time of casualties separately for min and max parts
            from already simulated Fleet 1 (passed in as a dict from var_to_save_spacefleet_1).

            Returns a dict with two keys: "min" and "max", values are lists, starting from lower cost and build time, length is top_length passed to this func.

            You can specify coefficient for energy cost and build time,
            the higher the coefficient (for the cost, for example) the more the cost part will influence the result.

            Defaults are 1.0, 1.0.

            add_departure_cost (default 2%) - in Game it costs energy (2% of SpaceFleet's cost) to send an attack.
            If you don't want that, pass 0.
        """

        if not isinstance(top_length, int):
            top_length = 5
        if top_length < 0 or top_length > len(results_from_find_suitable_fleets_to_beat_enemy):
            top_length = len(results_from_find_suitable_fleets_to_beat_enemy)

        orig_result = results_from_find_suitable_fleets_to_beat_enemy
        result = {"min": [],"max": []}
        if isinstance(fleet_results, dict) and isinstance(orig_result, dict) and set(fleet_results.keys()) == set(orig_result.keys()):
            semi_result_min = {}
            semi_result_max = {}
            for ss_id in fleet_results:
                pair_of_fleets = fleet_results[ss_id]
                if (isinstance(pair_of_fleets, list) or isinstance(pair_of_fleets, tuple)) and len(pair_of_fleets) == 2:
                    fleet_min, fleet_max = pair_of_fleets
                    if isinstance(fleet_min, SpaceFleet):
                        cost_of_sending_fleet_to_attack = fleet_min.cost_of_original * add_departure_cost / 100
                        cost = fleet_min.cost_of_dead
                        build_time = fleet_min.build_time_of_dead
                        coef_of_efficiency = (cost + cost_of_sending_fleet_to_attack) * coef_for_cost + build_time * coef_for_time
                        semi_result_min.update({ss_id: coef_of_efficiency})
                    if isinstance(fleet_max, SpaceFleet):
                        cost_of_sending_fleet_to_attack = fleet_max.cost_of_original * add_departure_cost / 100
                        cost = fleet_max.cost_of_dead
                        build_time = fleet_max.build_time_of_dead
                        coef_of_efficiency = (cost + cost_of_sending_fleet_to_attack) * coef_for_cost + build_time * coef_for_time
                        semi_result_max.update({ss_id: coef_of_efficiency})

            semi_result_min_sorted = sorted(semi_result_min.items(), key=lambda x:x[1])
            #semi_result_min_sorted = dict(semi_result_min_sorted)
            semi_result_max_sorted = sorted(semi_result_max.items(), key=lambda x:x[1])
            #semi_result_max_sorted = dict(semi_result_max_sorted)
            if len(semi_result_min_sorted) >= top_length:
                for top_index in range(top_length):
                    result["min"].append(semi_result_min_sorted[top_index][0])
            if len(semi_result_max_sorted) >= top_length:
                for top_index in range(top_length):
                    result["max"].append(semi_result_max_sorted[top_index][0])

        return result

    def select_top_results_to_beat_enemy_simulate(self, results_from_find_suitable_fleets_to_beat_enemy: dict, \
                spaceship_module: ModuleAndBonuses, fleet2: SpaceFleet, planet: Planet, \
                target_blockade: bool = False, add_departure_cost: int = 2, \
                coef_for_cost: float = 1.0, coef_for_time: float = 1.0, \
                top_length: int = 5) -> dict:
        """Selects best results by energy cost and build time of casualties separately for min and max parts by first simulating Battle.

            Don't forget to change default accuracy type for fleet2 (i.e. to "max", for worst case scenario).

            Returns a dict with two keys: "min" and "max", values are lists, starting from lower cost and build time, length is top_length passed to this func.

            You can specify coefficient for energy cost and build time,
            the higher the coefficient (for the cost, for example) the more the cost part will influence the result.

            Defaults are 1.0, 1.0.

            add_departure_cost (default 2%) - in Game it costs energy (2% of SpaceFleet's cost) to send an attack.
            If you don't want that, pass 0.
        """

        debug_print_flag = battlesimulation._debug_printing
        battlesimulation._debug_printing = False

        if not isinstance(top_length, int):
            top_length = 5
        if top_length < 0 or top_length > len(results_from_find_suitable_fleets_to_beat_enemy):
            top_length = len(results_from_find_suitable_fleets_to_beat_enemy)

        orig_result = results_from_find_suitable_fleets_to_beat_enemy
        result = {"min": [],"max": []}
        if isinstance(spaceship_module, ModuleAndBonuses) and isinstance(fleet2, SpaceFleet) and fleet2.is_populated and \
                isinstance(planet, Planet):
            if isinstance(orig_result, dict):
                semi_result_min = {}
                semi_result_max = {}
                for ss_id in orig_result:
                    pair = orig_result[ss_id]
                    if (isinstance(pair, list) or isinstance(pair, tuple)) and len(pair) == 2:
                        min_amount, max_amount = pair
                        if isinstance(min_amount, int):
                            min_amount = ((ss_id, min_amount),)
                        if isinstance(max_amount, int):
                            max_amount = ((ss_id, max_amount),)
                        if isinstance(min_amount, list) or isinstance(min_amount, tuple):
                            fleet = SpaceFleet()
                            fleet.set_fleet(min_amount)
                            fleet.modules = spaceship_module
                            simulate_result = self.simulate(fleet, fleet2.make_a_copy_of_self(), planet.make_a_copy_of_self(), target_blockade)
                            if simulate_result:
                                cost_of_sending_fleet_to_attack = fleet.cost_of_original * add_departure_cost / 100
                                cost = fleet.cost_of_dead
                                build_time = fleet.build_time_of_dead
                                coef_of_efficiency = (cost + cost_of_sending_fleet_to_attack) * coef_for_cost + build_time * coef_for_time
                                semi_result_min.update({ss_id: coef_of_efficiency})
                        if isinstance(max_amount, list) or isinstance(max_amount, tuple):
                            fleet = SpaceFleet()
                            fleet.set_fleet(max_amount)
                            fleet.modules = spaceship_module
                            simulate_result = self.simulate(fleet, fleet2.make_a_copy_of_self(), planet.make_a_copy_of_self(), target_blockade)
                            if simulate_result:
                                cost_of_sending_fleet_to_attack = fleet.cost_of_original * add_departure_cost / 100
                                cost = fleet.cost_of_dead
                                build_time = fleet.build_time_of_dead
                                coef_of_efficiency = (cost + cost_of_sending_fleet_to_attack) * coef_for_cost + build_time * coef_for_time
                                semi_result_max.update({ss_id: coef_of_efficiency})
                semi_result_min_sorted = sorted(semi_result_min.items(), key=lambda x:x[1])
                #semi_result_min_sorted = dict(semi_result_min_sorted)
                semi_result_max_sorted = sorted(semi_result_max.items(), key=lambda x:x[1])
                #semi_result_max_sorted = dict(semi_result_max_sorted)
                if len(semi_result_min_sorted) >= top_length:
                    for top_index in range(top_length):
                        result["min"].append(semi_result_min_sorted[top_index][0])
                if len(semi_result_max_sorted) >= top_length:
                    for top_index in range(top_length):
                        result["max"].append(semi_result_max_sorted[top_index][0])

        battlesimulation._debug_printing = debug_print_flag

        return result

    def old_bombardment_calculate_valkyries_for_shield_generator(self, spaceship_module: ModuleAndBonuses, planet: Planet, \
            valkyrie_dead_by_turrets: float, valkyrie_dead_by_rockets: float, \
            shield_level: int) -> tuple:
        """This func is for old Bombardment mechanic, it returns a tuple of 4 item.

            It calculates the number of Valkyries needed to destroy Shield Generator.
            When one level of Shield Generator is destroyed, the Shield does EMP damage back to Valkyries.

            returns: item1 = number of Valkyries needed to fully destroy Shield Generator on the Planet in one go;
            item2 = number of Valkyries that will be destroyed during the attack;

            item3 = a list of Valkyries needed to destroy a particular level of Shield Generator
            (includes the amount of Valkyries that will be destroyed before the Bombardment will start
            (destroyed by turrets, and rockets only for the initial shield level)),
            index is reversed level of Shield Generator, index 0 - level 30, 1 - level 29, ... , 29 - level 1;

            item4 = is the same as item3 except that numbers are the Valkyries that will be destroyed by that particular level of Shield Generator.
        """

        if isinstance(spaceship_module, ModuleAndBonuses) and isinstance(planet, Planet) and \
                isinstance(planet.buildings, BuildingArray) and isinstance(shield_level, int) and \
                0 <= shield_level <= battlesimulation._GGP.globals["max_building_level"] and \
                isinstance(valkyrie_dead_by_turrets, float) and isinstance(valkyrie_dead_by_rockets, float) and \
                valkyrie_dead_by_turrets >= 0 and valkyrie_dead_by_rockets >= 0:
            if valkyrie_dead_by_turrets + valkyrie_dead_by_rockets >= 1:
                left_over_valkyries = (valkyrie_dead_by_turrets + valkyrie_dead_by_rockets) % int(valkyrie_dead_by_turrets + valkyrie_dead_by_rockets)
            else:
                left_over_valkyries = valkyrie_dead_by_turrets + valkyrie_dead_by_rockets
            valkyrie = Spaceship(7,1)
            shield_damage_type_id = planet.shield_damage_type_id
            # no Superiority mechanic in bombardment
            spaceship_module.calc_final_damage_mods(1.0)
            shield_max_coef = battlesimulation._GGP.globals["shield_max_coef"]
            damage_to_do = []
            damage_to_do_sum = 0
            valkyr_needed = []
            valkyr_dead = []
            j = battlesimulation._GGP.globals["max_building_level"] - shield_level
            for i in range(j):
                valkyr_needed.append(0)
                valkyr_dead.append(0)
            if shield_level == 0:
                return (0, 0, tuple(valkyr_needed), tuple(valkyr_dead))
            shield_lvl_now = shield_level
            for i in range(shield_level):
                all_defenses = planet.buildings._total_defense_up_to_level(shield_lvl_now)
                debug_print(f"all_defenses for {shield_lvl_now} shield level: {all_defenses}")
                dmg_to_do = _my_truncate((all_defenses * shield_max_coef), 6)
                # but probably I'll skip this kind of fine-tuning
                if i == -1:
                    # if there is a "part" of Valkyrie spaceship after Turrets and Rockets (Spaceship's quantity is float until the end of Battle)
                    # then it too does damage, so we subtract that from damage_to_do
                    # But only for the initial (upper) level
                    damage_to_do -= left_over_valkyries * valkyrie.attack * spaceship_module.final_attack_damage_mods[valkyrie.damage_type_id]
                damage_to_do.append(dmg_to_do)
                damage_to_do_sum += dmg_to_do
                valkyr_needed.append(_my_truncate(dmg_to_do / (valkyrie.attack * spaceship_module.final_attack_damage_mods[valkyrie.damage_type_id]),6))
                valkyr_dead.append(_my_truncate(dmg_to_do / (valkyrie.defenses[shield_damage_type_id] * spaceship_module.final_no_superiority_defense_damage_mods[shield_damage_type_id]),6))
                debug_print(f"{damage_to_do[i]=}, {valkyr_needed[i+j]=}, {valkyr_dead[i+j]=}\n")
                shield_lvl_now -= 1
            
            valkyr_needed_final = sum(valkyr_needed)
            valkyr_dead_final = sum(valkyr_dead)
            # 
            valkyr_dead_final += valkyrie_dead_by_turrets + valkyrie_dead_by_rockets
            valkyr_needed_final += valkyrie_dead_by_turrets + valkyrie_dead_by_rockets
            
            text = "\n"
            shield_lvl_now = shield_level
            for i in range(shield_level):
                if i == 0:
                    # at the time of attack on the initial level of S.G. Rockets are ready to fire (and they do)
                    valkyr_dead[i + j] += valkyrie_dead_by_turrets + valkyrie_dead_by_rockets
                    valkyr_needed[i + j] += valkyrie_dead_by_turrets + valkyrie_dead_by_rockets
                else:
                    # no more Rockets after
                    valkyr_dead[i + j] += valkyrie_dead_by_turrets
                    valkyr_needed[i + j] += valkyrie_dead_by_turrets
                text += f"Shield level {shield_lvl_now}\nDamage needed {damage_to_do[i]}\nValkyr needed {valkyr_needed[i + j]}\nValkyr will die {valkyr_dead[i + j]}\n\n"
                shield_lvl_now -= 1
            text += "\n"
            text += f"{valkyr_needed_final=}, {valkyr_dead_final=}\n"
            debug_print(text)
            valkyr_needed_final = int(_my_round_threshold_up(valkyr_needed_final, 0, battlesimulation._GGP.threshold))
            valkyr_dead_final = int(_my_round_threshold_up(valkyr_dead_final, 0, battlesimulation._GGP.threshold))
            for i in range(len(valkyr_needed)):
                valkyr_needed[i] = int(_my_round_threshold_up(valkyr_needed[i], 0, battlesimulation._GGP.threshold))
            for i in range(len(valkyr_dead)):
                valkyr_dead[i] = int(_my_round_threshold_up(valkyr_dead[i], 0, battlesimulation._GGP.threshold))
            
            return (valkyr_needed_final, valkyr_dead_final, tuple(valkyr_needed), tuple(valkyr_dead))

    def old_bombardment_calculate_valkyries_for_turrets(self, spaceship_module: ModuleAndBonuses, \
            valkyrie_dead_by_turrets: float, valkyrie_dead_by_rockets: float, \
            turrets_defenses: int, shield_level: int) -> tuple:
        """This func is for old Bombardment mechanic, it returns a tuple.

            returns: tuple = (valkyries_needed_to_destroy_turrets, valkyries_destroyed_for_turrets)
            It calculates the number of Valkyries needed to destroy all Turrets and not touch other buildings.
        """

        valkyrie_needed_for_turrets = 0
        if isinstance(spaceship_module, ModuleAndBonuses) and \
                isinstance(valkyrie_dead_by_turrets, float) and isinstance(valkyrie_dead_by_rockets, float) and \
                valkyrie_dead_by_turrets >= 0 and valkyrie_dead_by_rockets >= 0 and isinstance(shield_level, int) and \
                0 <= shield_level <= battlesimulation._GGP.globals["max_building_level"] and \
                isinstance(turrets_defenses, int) and turrets_defenses >= 0:
            if turrets_defenses == 0:
                return (0, 0)
            if shield_level == 0:
                valkyrie_destroyed_for_turrets = int(_my_round_threshold_down(valkyrie_dead_by_turrets + valkyrie_dead_by_rockets, 0, battlesimulation._GGP.threshold))
                if valkyrie_dead_by_turrets + valkyrie_dead_by_rockets >= 1:
                    left_over_valkyries = (valkyrie_dead_by_turrets + valkyrie_dead_by_rockets) % int(valkyrie_dead_by_turrets + valkyrie_dead_by_rockets)
                else:
                    left_over_valkyries = valkyrie_dead_by_turrets + valkyrie_dead_by_rockets
            else:
                valkyrie_destroyed_for_turrets = int(_my_round_threshold_down(valkyrie_dead_by_turrets, 0, battlesimulation._GGP.threshold))
                if valkyrie_dead_by_turrets >= 1:
                    left_over_valkyries = (valkyrie_dead_by_turrets) % int(valkyrie_dead_by_turrets)
                else:
                    left_over_valkyries = valkyrie_dead_by_turrets
            left_over_valkyries = _my_truncate(1 - left_over_valkyries, 6)
            valkyrie = Spaceship(7,1)
            # no Superiority mechanic in bombardment
            spaceship_module.calc_final_damage_mods(1.0)
            # if there is a "part" of Valkyrie spaceship after Turrets and Rockets (Spaceship's quantity is float until the end of Battle)
            # then it too does damage, so we subtract that damage from turret_defenses
            turrets_defenses -= left_over_valkyries * valkyrie.attack * spaceship_module.final_attack_damage_mods[valkyrie.damage_type_id]
            valkyrie_needed_for_turrets = turrets_defenses / (valkyrie.attack * spaceship_module.final_attack_damage_mods[valkyrie.damage_type_id])
            valkyrie_needed_for_turrets += valkyrie_dead_by_turrets
            # if the initial Shield Generator level is 0, then there was no separate attack on it and the Rockets are intact
            # N.B although the Player should destroy rockets (except X-Rays) before making a Bombardment
            if shield_level == 0:
                valkyrie_needed_for_turrets += valkyrie_dead_by_rockets
            valkyrie_needed_for_turrets = _my_round_up(valkyrie_needed_for_turrets)
            debug_print(f"{valkyrie_needed_for_turrets=}")
        return (valkyrie_needed_for_turrets, valkyrie_destroyed_for_turrets)

    def old_bombardment_calculate_valkyries_for_the_rest_of_buildings(self, spaceship_module: ModuleAndBonuses, the_rest_buildings_defenses: int) -> int:
        """This func is for old Bombardment mechanic, it returns an amount of Valkyries needed to destroy all other buildings."""

        valkyries_needed_for_buildings = 0
        if isinstance(spaceship_module, ModuleAndBonuses) and \
                isinstance(the_rest_buildings_defenses, int) and the_rest_buildings_defenses >= 0:
            valkyrie = Spaceship(7,1)
            # no Superiority mechanic in bombardment
            spaceship_module.calc_final_damage_mods(1.0)
            valkyries_needed_for_buildings = the_rest_buildings_defenses / (valkyrie.attack * spaceship_module.final_attack_damage_mods[valkyrie.damage_type_id])
            valkyries_needed_for_buildings = _my_round_up(valkyries_needed_for_buildings)
            debug_print(f"{valkyries_needed_for_buildings=}")
        return valkyries_needed_for_buildings

    def old_simulate_bombardment(self, spaceship_module: ModuleAndBonuses, planet: Planet) -> dict:
        """Old Bombardment Mechanic, returns dict of numbers of Valkyries needed to destroy Planetary Defense.

            This game mechanic is still in effect on live (main) Game Galaxies, but it's going to change.

            There is already a new Bombardment mechanic in the Closed Beta Test and in the special game mode called "Seasons".

            So this func will not be needed in the future, and thus it is not well documented and not user friendly, sorry.
        """

        result = {}
        if isinstance(spaceship_module, ModuleAndBonuses) and isinstance(planet, Planet) and \
                isinstance(planet.rockets, RocketArray) and isinstance(planet.buildings, BuildingArray):
            planetary_defenses = self._get_basic_vars_for_old_bombardment(spaceship_module, planet.make_a_copy_of_self())
            if isinstance(planetary_defenses, dict):
                valkyrie_dead_by_turrets = planetary_defenses["valkyrie_dead_by_turrets"]
                valkyrie_dead_by_rockets = planetary_defenses["valkyrie_dead_by_rockets"]
                shield_generator_defenses = planetary_defenses["shield_generator_defenses"]
                turrets_defenses = planetary_defenses["turrets_defenses"]
                the_rest_buildings_defenses = planetary_defenses["the_rest_buildings_defenses"]
                shield_level = planetary_defenses["shield_level"]
                #
                result_for_shield_generator = self.old_bombardment_calculate_valkyries_for_shield_generator(spaceship_module, planet, valkyrie_dead_by_turrets, \
                        valkyrie_dead_by_rockets, shield_level)
                result_for_turrets = self.old_bombardment_calculate_valkyries_for_turrets(spaceship_module, valkyrie_dead_by_turrets, valkyrie_dead_by_rockets, \
                        turrets_defenses, shield_level)
                result_for_buildings = self.old_bombardment_calculate_valkyries_for_the_rest_of_buildings(spaceship_module, the_rest_buildings_defenses)
                result.update({"needed_for_shield": result_for_shield_generator[0]})
                result.update({"dead_for_shield": result_for_shield_generator[1]})
                result.update({"needed_for_shield_per_level": result_for_shield_generator[2]})
                result.update({"dead_for_shield_per_level": result_for_shield_generator[3]})
                result.update({"needed_for_turrets": result_for_turrets[0]})
                result.update({"dead_for_turrets": result_for_turrets[1]})
                result.update({"needed_for_buildings": result_for_buildings})
        return result

##############################################