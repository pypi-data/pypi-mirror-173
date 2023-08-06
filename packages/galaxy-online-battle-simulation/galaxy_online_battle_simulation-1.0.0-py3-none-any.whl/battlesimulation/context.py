from __future__ import annotations
from typing import Union
from datetime import timedelta

##############################################

import battlesimulation
from battlesimulation import debug_print, Spaceship, SpaceFleet, ModuleAndBonuses, Planet

class Context():
    """Context is used to make user input more convinient and to do simulation.

        func help() will return a string and print it if debug printing is enabled.
    """

    def get_fleet_1_acc_type(self) -> str:
        return self._fleet_1_acc_type

    def set_fleet_1_acc_type(self, acc_type: Union[str,int]) -> None:
        """Set type of accuracy to use for Fleet 1.

            min = minumal accuracy for each Spaceship
            max = 100% or:

            range_min or range_max = a new Context will be initiated in self.context_branch for additional simulation.
            The parent Context's Fleet 1 will use the set acc_type (range_min in this example)
            and the branch one will use the opposite (range_max in this example)

            So if you need results for Every Part of battle, use several Context objects.

            random = random accuracy between min and max
            or specified accuracy: 0 < interger <= 100
        """

        if acc_type in ("min","max","random","range_min","range_max"):
            self._fleet_1_acc_type = acc_type
            if isinstance(self._fleet_1, SpaceFleet):
                self._fleet_1.acc_type = acc_type
        elif isinstance(acc_type, int) and 0 < acc_type and acc_type <= 100:
            self._fleet_1_acc_type = acc_type
            if isinstance(self._fleet_1, SpaceFleet):
                self._fleet_1.acc_type = acc_type
    
    def get_fleet_2_acc_type(self) -> str:
        return self._fleet_2_acc_type
    
    def set_fleet_2_acc_type(self, acc_type: Union[str,int]) -> None:
        """Set type of accuracy to use for Fleet 2.

            min = minumal accuracy for each Spaceship
            max = 100% or:

            range_min or range_max = a new Context will be initiated in self.context_branch for additional simulation.
            The parent Context's Fleet 2 will use the set acc_type (range_min in this example)
            and the branch one will use the opposite (range_max in this example)

            So if you need results for Every Part of battle, use several Context objects.

            random = random accuracy between min and max
            or specified accuracy: 0 < interger <= 100
        """

        if acc_type in ("min","max","random","range_min","range_max"):
            self._fleet_2_acc_type = acc_type
            if isinstance(self._fleet_2, SpaceFleet):
                self._fleet_2.acc_type = acc_type
        elif isinstance(acc_type, int) and 0 < acc_type and acc_type <= 100:
            self._fleet_2_acc_type = acc_type
            if isinstance(self._fleet_2, SpaceFleet):
                self._fleet_2.acc_type = acc_type
    
    def get_fleet_3_acc_type(self) -> str:
        return self._fleet_3_acc_type
    
    def set_fleet_3_acc_type(self, acc_type: Union[str,int]) -> None:
        """Set type of accuracy to use for Fleet 3.

            min = minumal accuracy for each Spaceship
            max = 100% or:

            range_min or range_max = a new Context will be initiated in self.context_branch for additional simulation.
            The parent Context's Fleet 3 will use the set acc_type (range_min in this example)
            and the branch one will use the opposite (range_max in this example)

            So if you need results for Every Part of battle, use several Context objects.

            random = random accuracy between min and max
            or specified accuracy: 0 < interger <= 100
        """

        if acc_type in ("min","max","random","range_min","range_max"):
            self._fleet_3_acc_type = acc_type
            if isinstance(self._fleet_3, SpaceFleet):
                self._fleet_3.acc_type = acc_type
        elif isinstance(acc_type, int) and 0 < acc_type and acc_type <= 100:
            self._fleet_3_acc_type = acc_type
            if isinstance(self._fleet_3, SpaceFleet):
                self._fleet_3.acc_type = acc_type

    fleet_1_acc_type = property(get_fleet_1_acc_type, set_fleet_1_acc_type)
    fleet_2_acc_type = property(get_fleet_2_acc_type, set_fleet_2_acc_type)
    fleet_3_acc_type = property(get_fleet_3_acc_type, set_fleet_3_acc_type)
    
    def __init__(self) -> None:
        """New instance of Context class."""

        self.context_branch = None
        self._flag_to_make_context_branch = False
        self._text_for_finding_suitable_fleets = ""
        self._battle_simulation = battlesimulation._root_battle_simulation
        self._fleet_1 = SpaceFleet()
        self._fleet_2 = SpaceFleet()
        self._fleet_3 = SpaceFleet()
        self._fleet_1.attacking = True
        self._fleet_2.attacking = False
        self._fleet_3.attacking = False
        self._planet = Planet()
        self._fleet_1_acc_type = "min"
        self._fleet_2_acc_type = "min"
        self._fleet_3_acc_type = "min"
        self._attack_target = True
        self._fleet_finder_raw_results_dict = {}
        self._fleet_finder_top_sorted_dict = {}
        self._fleet_finder_dict = {}
        self._results_for_old_bombardment = {}
        self._top_sorted_length = 5
        self._add_energy_cost_to_departure = 2
        self._coef_for_cost = 1.0
        self._coef_for_time = 1.0

    def help(self) -> str:
        """prints and returns string: short list of to do things to Simulate Battle."""

        text = "\n\nThis is the module for making calculations for MMO Strategy Game Galaxy Online (https://galaxyonline.io)\n"
        text += "Project page: https://github.com/fadedness/galaxy-online-battle-simulation\n"
        text += "There is a GUI wrapper for this module: https://github.com/fadedness/Galaxy-Online-Battle-Calculator\n\n"
        text += "You can use this module to analize your possibilities, casualties, costs; you can find possible good counters to incoming attacks on you.\n"
        text += f"version is {battlesimulation.__version__}\n\n"
        text += "Unless you don't need or you save Simulation results, you should not use the same instantiated Context object for other simulations.\n\n"
        text += "Anything left unset will be instatiated as default: empty Fleet, empty Planet, etc\n"
        text += "Fleet 1 is considered always attacking the Fleet 2, which is defending Planet's surface. If Planet is not set, "
        text += "it is a space battle. You can set both Fleets to use attack or defense priorities for calculations. "
        text += "If there's also a blockading Fleet 3, set it with set_fleet_3 or other commands listed in \"1.\". "
        text += "Fleet 3 uses defense priorities by default, use the same commands changing number 1 to 3 in the name.\n\n"
        text += "Order of your actions:\n"
        text += "1. Instantiate SpaceFleets 1 and 2: set_fleet_1, init_fleet_1, add_spaceship_to_fleet_1, add_%ShipName_to_fleet_1\n"
        text += "2. Set accuracy type of both Fleets (default is min): set_fleet_1_acc_type\n"
        text += "3. Set module params for both Fleets: set_fleet_1_module, set_fleet_1_module_by_id_and_level\n"
        text += "3.a. Set damage/defense bonuses from commanders (if needed): set_fleet_1_module_attack_bonuses, set_fleet_1_module_defense_bonuses\n"
        text += "4. Set a Planet: set_planet or set_planet_by_dict\n"
        text += "4.a. Set rockets on the Planet: set_rockets\n"
        text += "5. Change Fleet priorities (if needed) with set_fleet_1_attacking(True or False)\n"
        text += "6. Set attack type on the Planet (Fleet 1 is attacking Planet (True) or making a blockade (False): set_planet_attack_type\n"
        text += "7. Finally call simulate, all the results will be inside corresponding class instancies. "
        text += "Info and results will be printed.\n"
        text += "If you call Context.enable_debug_printing(), some more technical info inside calculations will be printed.\n"
        text += "You can omit Fleet 1, then the Context will try to find suitable Fleet 1 to defeat the rest set Game objects.\n"
        text += "Results will be printed, and you can access them via _fleet_finder_dict - Fleet 1 variants, "
        text += "_fleet_finder_raw_results_dict simple dict keys = spaceships ids, values = tuple (min, max) quantity, "
        text += "_fleet_finder_top_sorted_dict - the same but sorted.\n"
        text += "Don't forget to set Fleet 1 modules if you want to use them while finding Fleet 1.\n"
        #text += "If you are making a GUI for this module, than refer to github for additional info:\n"
        #text += "https://github.com/fadedness/galaxy-online-battle-simulation/\n\n"
        text += "\n\nAfter Simulation, you can directly access leftovers of Fleets, Rockets, their costs and build times via:\n"
        text += "Context._fleet_1,2,3, Context._planet.rockets\n"
        text += "Properties: .cost_of_original, .cost_of_dead, .build_time_of_original, .build_time_of_dead\n"
        print(text)
        return text

    def help_game_parameters(self) -> str:
        """prints and returns string: info of some Game Parameters."""

        text = "_________________________________________________________________________________________"
        text += "\nGame Objects:\n\n"
        text += "\nAvailable Spaceships:\n\n"
        for key in battlesimulation._GGP.spaceships:
            ss = battlesimulation._GGP.spaceships[key]
            text += f"{ss['name_en']}: id={ss['id']}, damage type={battlesimulation._GGP.damages[ss['damage_type_id']]['name_en']}, "
            text += f"attack={ss['attack']}, defenses: "
            defenses_string = ""
            for d_key in battlesimulation._GGP.damages:
                dd = battlesimulation._GGP.damages[d_key]
                defenses_string += f"{ss['defenses'][d_key]} against {dd['name_en']}, "
            defenses_string = defenses_string[:-2]
            text += f"{defenses_string}, attack/defense priority={ss['attack_priority']}/{ss['defense_priority']}, "
            text += f"price={ss['price']}, build time in seconds={ss['build_time']}, accuracy={ss['accuracy']}%\n\n"

        text += "\nAvalable Rockets:\n\n"
        for key in battlesimulation._GGP.rockets:
            rr = battlesimulation._GGP.rockets[key]
            text += f"{rr['name_en']}: id={rr['id']}, warheads={rr['warheads']}, damage={rr['damage']} of "
            text += f"{battlesimulation._GGP.damages[rr['damage_type_id']]['name_en']} damage type, valid_targets="
            if rr['valid_targets'] == (1,3,4,5,6,7,8,9):
                valid_targets_string = "all Spaceships (except Loki)"
            else:
                valid_targets_string = ""
                for id in rr['valid_targets']:
                    valid_targets_string += f"{battlesimulation._GGP.spaceships[id]['name_en']}, "
                valid_targets_string = valid_targets_string[:-2]
            if rr['attack_type'] == 1:
                attack_type_string = "blockade"
            elif rr['attack_type'] == 2:
                attack_type_string = "attack"
            else:
                attack_type_string = "both"
            text += f"{valid_targets_string}, attack against={attack_type_string}, price={rr['price']}, build time in seconds={rr['build_time']}\n\n"

        text += f"\nAvailable Buildings:\nMax level is {battlesimulation._GGP.globals['max_building_level']}\n\n"
        for key in battlesimulation._GGP.buildings:
            bb = battlesimulation._GGP.buildings[key]
            text += f"{bb['name_en']}: id={bb['id']}, defense per level={bb['defense']}, maximum number on Planet={bb['max_buildings']}\n\n"

        text += "\nAvailable Modules:\nparams are per one level (max 100 lvl), build time is for level 20 Factory (I don't have exact base data right now)\n\n"
        for key in battlesimulation._GGP.modules:
            mm = battlesimulation._GGP.modules[key]
            text += f"{mm['name_en']}: id={mm['id']}, attack={mm['attack']/100}%, defense={mm['defense']/100}%, "
            text += f"speed={mm['speed']/100}%, price={mm['price']}, additional price in solarium={mm['solarium']}, "
            text += f"build time in seconds={mm['build_time']}\n\n"

        text += "\nPlanet types and sizes\n\n"
        text += "id 1 - Torium\nid 2 - Wanadium,\nid 3 - Ottarium,\nid 4 - Chromium,\nid 5 - Kladium,\nid 6 - Neodium,\nid 7 - Minterium.\n"
        text += "Sizes:\n0 - 3 Mines\n1 - 4 Mines\n2 - 5 Mines.\n\n"
        text += "_________________________________________________________________________________________"

        print(text)
        return text

    def enable_debug_printing(self) -> None:
        """Enable printing of different info inside some functions."""

        battlesimulation._debug_printing = True

    def disable_debug_printing(self) -> None:
        """Disable printing of different info inside some functions."""

        battlesimulation._debug_printing = False

    def set_length_of_top_sorted(self, length: int = 5) -> None:
        """Sets number of variants after sorting for "fleet finder" calculations."""

        self._top_sorted_length = length

    def set_add_energy_cost_to_depature(self, cost_percent: int = 2) -> None:
        """Sets additional energy cost when sorting for "fleet finder" calculations.

            Game requires to pay 2% energy cost to send Spaceships to attack.
        """

        self._add_energy_cost_to_departure = cost_percent

    def set_energy_cost_coef(self, coef: float = 1.0) -> None:
        """Sets coef for how much energy cost will affect sorting evaluation for "fleet finder" calculations."""

        self._coef_for_cost = coef

    def set_build_time_coef(self, coef: float = 1.0) -> None:
        """Sets coef for how much build time will affect sorting evaluation for "fleet finder" calculations."""

        self._coef_for_time = coef

    def set_fleet_1(self, fleet1: SpaceFleet) -> None:
        """Sets Fleet 1 to already instanciated SpaceFleet (makes a copy)."""

        if isinstance(fleet1, SpaceFleet):
            self._fleet_1 = fleet1.make_a_copy_of_self()
    
    def set_fleet_2(self, fleet2: SpaceFleet) -> None:
        """Sets Fleet 2 to already instanciated SpaceFleet (makes a copy)."""

        if isinstance(fleet2, SpaceFleet):
            self._fleet_2 = fleet2.make_a_copy_of_self()
    
    def set_fleet_3(self, fleet3: SpaceFleet) -> None:
        """Sets Fleet 3 to already instanciated SpaceFleet (makes a copy)."""

        if isinstance(fleet3, SpaceFleet):
            self._fleet_3 = fleet3.make_a_copy_of_self()

    def init_fleet_1(self, data: Union[list,tuple,dict]) -> bool:
        """Sets a new Fleet 1 of spaceships.

            Accepts input data of list or tuple of pairs (also list or tuple): ((id1,value1),(id2,value2)) or dict {id1:value1,id2:value2}.
            Ids should be valid and unique, for list or tuple with duplicated ids, spaceships will be overwritten with the last ones.
            Values (quantity of spaceships) should be int (whole spaceship) or float (should not be used, left for testing).
            N.B. Spaceships quantity when battle is simulated will become float.

            Default ids: 1 - Hercules, 2 - Loki, 3 - Raptor, 4 - Hornet, 5 - Javelin,
            6 - Excalibur, 7 - Valkyrie, 8 - Titan, 9 - Abaddon.

            Pass an empty list to clear all Spaceships.
        """

        if not isinstance(self._fleet_1, SpaceFleet):
            self._fleet_1 = SpaceFleet()
        return self._fleet_1.set_fleet(data)

    def init_fleet_2(self, data: Union[list,tuple,dict]) -> bool:
        """Sets a new Fleet 2 of spaceships.

            Accepts input data of list or tuple of pairs (also list or tuple): ((id1,value1),(id2,value2)) or dict {id1:value1,id2:value2}.
            Ids should be valid and unique, for list or tuple with duplicated ids, spaceships will be overwritten with the last ones.
            Values (quantity of spaceships) should be int (whole spaceship) or float (should not be used, left for testing).
            N.B. Spaceships quantity when battle is simulated will become float.

            Default ids: 1 - Hercules, 2 - Loki, 3 - Raptor, 4 - Hornet, 5 - Javelin,
            6 - Excalibur, 7 - Valkyrie, 8 - Titan, 9 - Abaddon.

            Pass an empty list to clear all Spaceships.
        """

        if not isinstance(self._fleet_2, SpaceFleet):
            self._fleet_2 = SpaceFleet()
        return self._fleet_2.set_fleet(data)

    def init_fleet_3(self, data: Union[list,tuple,dict]) -> bool:
        """Sets a new Fleet 3 of spaceships.

            Accepts input data of list or tuple of pairs (also list or tuple): ((id1,value1),(id2,value2)) or dict {id1:value1,id2:value2}.
            Ids should be valid and unique, for list or tuple with duplicated ids, spaceships will be overwritten with the last ones.
            Values (quantity of spaceships) should be int (whole spaceship) or float (should not be used, left for testing).
            N.B. Spaceships quantity when battle is simulated will become float.

            Default ids: 1 - Hercules, 2 - Loki, 3 - Raptor, 4 - Hornet, 5 - Javelin,
            6 - Excalibur, 7 - Valkyrie, 8 - Titan, 9 - Abaddon.

            Pass an empty list to clear all Spaceships.
        """

        if not isinstance(self._fleet_3, SpaceFleet):
            self._fleet_3 = SpaceFleet()
        return self._fleet_3.set_fleet(data)

    def clear_fleet_1(self) -> None:
        """Clears Fleet 1 of all Spaceships."""

        self.init_fleet_1([])

    def clear_fleet_2(self) -> None:
        """Clears Fleet 2 of all Spaceships."""

        self.init_fleet_2([])

    def clear_fleet_3(self) -> None:
        """Clears Fleet 3 of all Spaceships."""

        self.init_fleet_3([])

    def add_spaceship_to_fleet_1(self, data: Union[list,tuple,dict,Spaceship]) -> bool:
        """Add a new spaceship to the Fleet 1, overwriting previous same spaceship (if any).

            Accepts list or tuple with length of 2: [id,quantity] or (id,quantity) or dict: {id:quantity}
            or an already instantiated spaceship (makes a copy).
        """

        if not isinstance(self._fleet_1, SpaceFleet):
            self._fleet_1 = SpaceFleet()
        return self._fleet_1.set_spaceship_in_fleet(data)

    def add_spaceship_to_fleet_2(self, data: Union[list,tuple,dict,Spaceship]) -> bool:
        """Add a new spaceship to the Fleet 2, overwriting previous same spaceship (if any).

            Accepts list or tuple with length of 2: [id,quantity] or (id,quantity) or dict: {id:quantity}
            or an already instantiated spaceship (makes a copy).
        """

        if not isinstance(self._fleet_2, SpaceFleet):
            self._fleet_2 = SpaceFleet()
        return self._fleet_2.set_spaceship_in_fleet(data)

    def add_spaceship_to_fleet_3(self, data: Union[list,tuple,dict,Spaceship]) -> bool:
        """Add a new spaceship to the Fleet 3, overwriting previous same spaceship (if any).

            Accepts list or tuple with length of 2: [id,quantity] or (id,quantity) or dict: {id:quantity}
            or an already instantiated spaceship (makes a copy).
        """

        if not isinstance(self._fleet_3, SpaceFleet):
            self._fleet_3 = SpaceFleet()
        return self._fleet_3.set_spaceship_in_fleet(data)

    def add_hercules_to_fleet_1(self, quantity: Union[int,float]) -> bool:
        """Add Hercules Spaceship to Fleet 1"""

        if (isinstance(quantity, int) or isinstance(quantity, float)) and quantity >= 0:
            return self.add_spaceship_to_fleet_1((1,quantity))

    def add_loki_to_fleet_1(self, quantity: Union[int,float]) -> bool:
        """Add Loki Spaceship to Fleet 1"""

        if (isinstance(quantity, int) or isinstance(quantity, float)) and quantity >= 0:
            return self.add_spaceship_to_fleet_1((2,quantity))

    def add_raptor_to_fleet_1(self, quantity: Union[int,float]) -> bool:
        """Add Raptor Spaceship to Fleet 1"""

        if (isinstance(quantity, int) or isinstance(quantity, float)) and quantity >= 0:
            return self.add_spaceship_to_fleet_1((3,quantity))

    def add_hornet_to_fleet_1(self, quantity: Union[int,float]) -> bool:
        """Add Hornet Spaceship to Fleet 1"""

        if (isinstance(quantity, int) or isinstance(quantity, float)) and quantity >= 0:
            return self.add_spaceship_to_fleet_1((4,quantity))

    def add_javelin_to_fleet_1(self, quantity: Union[int,float]) -> bool:
        """Add Javelin Spaceship to Fleet 1"""

        if (isinstance(quantity, int) or isinstance(quantity, float)) and quantity >= 0:
            return self.add_spaceship_to_fleet_1((5,quantity))

    def add_excalibur_to_fleet_1(self, quantity: Union[int,float]) -> bool:
        """Add Excalibur Spaceship to Fleet 1"""

        if (isinstance(quantity, int) or isinstance(quantity, float)) and quantity >= 0:
            return self.add_spaceship_to_fleet_1((6,quantity))

    def add_valkyrie_to_fleet_1(self, quantity: Union[int,float]) -> bool:
        """Add Valkyrie Spaceship to Fleet 1"""

        if (isinstance(quantity, int) or isinstance(quantity, float)) and quantity >= 0:
            return self.add_spaceship_to_fleet_1((7,quantity))

    def add_titan_to_fleet_1(self, quantity: Union[int,float]) -> bool:
        """Add Titan Spaceship to Fleet 1"""

        if (isinstance(quantity, int) or isinstance(quantity, float)) and quantity >= 0:
            return self.add_spaceship_to_fleet_1((8,quantity))

    def add_abaddon_to_fleet_1(self, quantity: Union[int,float]) -> bool:
        """Add Abaddon Spaceship to Fleet 1"""

        if (isinstance(quantity, int) or isinstance(quantity, float)) and quantity >= 0:
            return self.add_spaceship_to_fleet_1((9,quantity))

    def add_hercules_to_fleet_2(self, quantity: Union[int,float]) -> bool:
        """Add Hercules Spaceship to Fleet 2"""

        if (isinstance(quantity, int) or isinstance(quantity, float)) and quantity >= 0:
            return self.add_spaceship_to_fleet_2((1,quantity))

    def add_loki_to_fleet_2(self, quantity: Union[int,float]) -> bool:
        """Add Loki Spaceship to Fleet 2"""

        if (isinstance(quantity, int) or isinstance(quantity, float)) and quantity >= 0:
            return self.add_spaceship_to_fleet_2((2,quantity))

    def add_raptor_to_fleet_2(self, quantity: Union[int,float]) -> bool:
        """Add Raptor Spaceship to Fleet 2"""

        if (isinstance(quantity, int) or isinstance(quantity, float)) and quantity >= 0:
            return self.add_spaceship_to_fleet_2((3,quantity))

    def add_hornet_to_fleet_2(self, quantity: Union[int,float]) -> bool:
        """Add Hornet Spaceship to Fleet 2"""

        if (isinstance(quantity, int) or isinstance(quantity, float)) and quantity >= 0:
            return self.add_spaceship_to_fleet_2((4,quantity))

    def add_javelin_to_fleet_2(self, quantity: Union[int,float]) -> bool:
        """Add Javelin Spaceship to Fleet 2"""

        if (isinstance(quantity, int) or isinstance(quantity, float)) and quantity >= 0:
            return self.add_spaceship_to_fleet_2((5,quantity))

    def add_excalibur_to_fleet_2(self, quantity: Union[int,float]) -> bool:
        """Add Excalibur Spaceship to Fleet 2"""

        if (isinstance(quantity, int) or isinstance(quantity, float)) and quantity >= 0:
            return self.add_spaceship_to_fleet_2((6,quantity))

    def add_valkyrie_to_fleet_2(self, quantity: Union[int,float]) -> bool:
        """Add Valkyrie Spaceship to Fleet 2"""

        if (isinstance(quantity, int) or isinstance(quantity, float)) and quantity >= 0:
            return self.add_spaceship_to_fleet_2((7,quantity))

    def add_titan_to_fleet_2(self, quantity: Union[int,float]) -> bool:
        """Add Titan Spaceship to Fleet 2"""

        if (isinstance(quantity, int) or isinstance(quantity, float)) and quantity >= 0:
            return self.add_spaceship_to_fleet_2((8,quantity))

    def add_abaddon_to_fleet_2(self, quantity: Union[int,float]) -> bool:
        """Add Abaddon Spaceship to Fleet 2"""

        if (isinstance(quantity, int) or isinstance(quantity, float)) and quantity >= 0:
            return self.add_spaceship_to_fleet_2((9,quantity))

    def add_hercules_to_fleet_3(self, quantity: Union[int,float]) -> bool:
        """Add Hercules Spaceship to Fleet 3"""

        if (isinstance(quantity, int) or isinstance(quantity, float)) and quantity >= 0:
            return self.add_spaceship_to_fleet_3((1,quantity))

    def add_loki_to_fleet_3(self, quantity: Union[int,float]) -> bool:
        """Add Loki Spaceship to Fleet 3"""

        if (isinstance(quantity, int) or isinstance(quantity, float)) and quantity >= 0:
            return self.add_spaceship_to_fleet_3((2,quantity))

    def add_raptor_to_fleet_3(self, quantity: Union[int,float]) -> bool:
        """Add Raptor Spaceship to Fleet 3"""

        if (isinstance(quantity, int) or isinstance(quantity, float)) and quantity >= 0:
            return self.add_spaceship_to_fleet_3((3,quantity))

    def add_hornet_to_fleet_3(self, quantity: Union[int,float]) -> bool:
        """Add Hornet Spaceship to Fleet 3"""

        if (isinstance(quantity, int) or isinstance(quantity, float)) and quantity >= 0:
            return self.add_spaceship_to_fleet_3((4,quantity))

    def add_javelin_to_fleet_3(self, quantity: Union[int,float]) -> bool:
        """Add Javelin Spaceship to Fleet 3"""

        if (isinstance(quantity, int) or isinstance(quantity, float)) and quantity >= 0:
            return self.add_spaceship_to_fleet_3((5,quantity))

    def add_excalibur_to_fleet_3(self, quantity: Union[int,float]) -> bool:
        """Add Excalibur Spaceship to Fleet 3"""

        if (isinstance(quantity, int) or isinstance(quantity, float)) and quantity >= 0:
            return self.add_spaceship_to_fleet_3((6,quantity))

    def add_valkyrie_to_fleet_3(self, quantity: Union[int,float]) -> bool:
        """Add Valkyrie Spaceship to Fleet 3"""

        if (isinstance(quantity, int) or isinstance(quantity, float)) and quantity >= 0:
            return self.add_spaceship_to_fleet_3((7,quantity))

    def add_titan_to_fleet_3(self, quantity: Union[int,float]) -> bool:
        """Add Titan Spaceship to Fleet 3"""

        if (isinstance(quantity, int) or isinstance(quantity, float)) and quantity >= 0:
            return self.add_spaceship_to_fleet_3((8,quantity))

    def add_abaddon_to_fleet_3(self, quantity: Union[int,float]) -> bool:
        """Add Abaddon Spaceship to Fleet 3"""

        if (isinstance(quantity, int) or isinstance(quantity, float)) and quantity >= 0:
            return self.add_spaceship_to_fleet_3((9,quantity))

    def set_fleet_1_module(self, data: Union[list,tuple,ModuleAndBonuses]) -> None:
        """Sets Fleet 1 module to given data.

            data: already instantiated Modules or
            pass list or tuple with length 3 with values of bonuses: [attack, defense, speed]
        """

        if isinstance(self._fleet_1, SpaceFleet):
            if isinstance(data, ModuleAndBonuses):
                self._fleet_1.modules = data.make_a_copy_of_self()
            elif (isinstance(data, list) or isinstance(data, tuple)) and len(data) == 3:
                self._fleet_1.set_module_params(*data)

    def set_fleet_2_module(self, data: Union[list,tuple,ModuleAndBonuses]) -> None:
        """Sets Fleet 2 module to given data.

            data: already instantiated Modules or
            pass list or tuple with length 3 with values of bonuses: [attack, defense, speed]
        """

        if isinstance(self._fleet_2, SpaceFleet):
            if isinstance(data, ModuleAndBonuses):
                self._fleet_2.modules = data.make_a_copy_of_self()
            elif (isinstance(data, list) or isinstance(data, tuple)) and len(data) == 3:
                self._fleet_2.set_module_params(*data)

    def set_fleet_3_module(self, data: Union[list,tuple,ModuleAndBonuses]) -> None:
        """Sets Fleet 3 module to given data.

            data: already instantiated Modules or
            pass list or tuple with length 3 with values of bonuses: [attack, defense, speed]
        """

        if isinstance(self._fleet_3, SpaceFleet):
            if isinstance(data, ModuleAndBonuses):
                self._fleet_3.modules = data.make_a_copy_of_self()
            elif (isinstance(data, list) or isinstance(data, tuple)) and len(data) == 3:
                self._fleet_3.set_module_params(*data)

    def set_fleet_1_module_by_id_and_level(self, id: int, level: int = 100) -> None:
        """Sets Fleet 1 module to named Game Module by id.

            1 - Disintegrator, 2 - Afterburner, 3 - Shield Booster, 4 - Complex Bastion,
            5 - Complex Luch, 6 - Complex Halo, 7 - Complex Guardian,
            no bonuses:
            8 - Satellite Solarium, 9 - Satellite Energy, 10 - Complex Boarding.
        """

        if isinstance(self._fleet_1, SpaceFleet):
            if id in battlesimulation._GGP.modules and isinstance(level, int) and 1 <= level <= 100:
                self._fleet_1.modules.set_module_by_id(id, level)

    def set_fleet_2_module_by_id_and_level(self, id: int, level: int = 100) -> None:
        """Sets Fleet 2 module to named Game Module by id.

            1 - Disintegrator, 2 - Afterburner, 3 - Shield Booster, 4 - Complex Bastion,
            5 - Complex Luch, 6 - Complex Halo, 7 - Complex Guardian,
            no bonuses:
            8 - Satellite Solarium, 9 - Satellite Energy, 10 - Complex Boarding.
        """

        if isinstance(self._fleet_2, SpaceFleet):
            if id in battlesimulation._GGP.modules and isinstance(level, int) and 1 <= level <= 100:
                self._fleet_2.modules.set_module_by_id(id, level)

    def set_fleet_3_module_by_id_and_level(self, id: int, level: int = 100) -> None:
        """Sets Fleet 3 module to named Game Module by id.

            1 - Disintegrator, 2 - Afterburner, 3 - Shield Booster, 4 - Complex Bastion,
            5 - Complex Luch, 6 - Complex Halo, 7 - Complex Guardian,
            no bonuses:
            8 - Satellite Solarium, 9 - Satellite Energy, 10 - Complex Boarding.
        """

        if isinstance(self._fleet_3, SpaceFleet):
            if id in battlesimulation._GGP.modules and isinstance(level, int) and 1 <= level <= 100:
                self._fleet_3.modules.set_module_by_id(id, level)

    def set_fleet_1_module_attack_bonuses(self, data: Union[list,tuple,dict]) -> None:
        """Not necessary.

            Set attack bonuses for each damage type.
            Input is either a list or a tuple of pairs of list or tuple (id,value):
            [(1, 1.0), (5, 1.2), (3, 1.1), (4, 1.3), (2, 1.5)]. Order doesn't matter, damage types may be omitted -> no bonus.
            Or a dictionary where key is damage type id and value is the bonus.
        """

        if isinstance(self._fleet_1, SpaceFleet) and isinstance(self._fleet_1.modules, ModuleAndBonuses):
            if (isinstance(data, list) or isinstance(data, tuple)):
                self._fleet_1.set_module_attack_damage_mods(*data)
            elif isinstance(data, dict):
                self._fleet_1.set_module_attack_damage_mods(data)

    def set_fleet_1_module_defense_bonuses(self, data: Union[list,tuple,dict]) -> None:
        """Not necessary.

            Set defense bonuses for each damage type.
            Input is either a list or a tuple of pairs of list or tuple (id,value):
            [(1, 1.0), (5, 1.2), (3, 1.1), (4, 1.3), (2, 1.5)]. Order doesn't matter, damage types may be omitted -> no bonus.
            Or a dictionary where key is damage type id and value is the bonus.
        """

        if isinstance(self._fleet_1, SpaceFleet) and isinstance(self._fleet_1.modules, ModuleAndBonuses):
            if (isinstance(data, list) or isinstance(data, tuple)):
                self._fleet_1.set_module_defense_damage_mods(*data)
            elif isinstance(data, dict):
                self._fleet_1.set_module_defense_damage_mods(data)

    def set_fleet_2_module_attack_bonuses(self, data: Union[list,tuple,dict]) -> None:
        """Not necessary.

            Set attack bonuses for each damage type.
            Input is either a list or a tuple of pairs of list or tuple (id,value):
            [(1, 1.0), (5, 1.2), (3, 1.1), (4, 1.3), (2, 1.5)]. Order doesn't matter, damage types may be omitted -> no bonus.
            Or a dictionary where key is damage type id and value is the bonus.
        """

        if isinstance(self._fleet_2, SpaceFleet) and isinstance(self._fleet_2.modules, ModuleAndBonuses):
            if (isinstance(data, list) or isinstance(data, tuple)):
                self._fleet_2.set_module_attack_damage_mods(*data)
            elif isinstance(data, dict):
                self._fleet_2.set_module_attack_damage_mods(data)

    def set_fleet_2_module_defense_bonuses(self, data: Union[list,tuple,dict]) -> None:
        """Not necessary.

            Set defense bonuses for each damage type.
            Input is either a list or a tuple of pairs of list or tuple (id,value):
            [(1, 1.0), (5, 1.2), (3, 1.1), (4, 1.3), (2, 1.5)]. Order doesn't matter, damage types may be omitted -> no bonus.
            Or a dictionary where key is damage type id and value is the bonus.
        """

        if isinstance(self._fleet_2, SpaceFleet) and isinstance(self._fleet_2.modules, ModuleAndBonuses):
            if (isinstance(data, list) or isinstance(data, tuple)):
                self._fleet_2.set_module_defense_damage_mods(*data)
            elif isinstance(data, dict):
                self._fleet_2.set_module_defense_damage_mods(data)

    def set_fleet_3_module_attack_bonuses(self, data: Union[list,tuple,dict]) -> None:
        """Not necessary.

            Set attack bonuses for each damage type.
            Input is either a list or a tuple of pairs of list or tuple (id,value):
            [(1, 1.0), (5, 1.2), (3, 1.1), (4, 1.3), (2, 1.5)]. Order doesn't matter, damage types may be omitted -> no bonus.
            Or a dictionary where key is damage type id and value is the bonus.
        """

        if isinstance(self._fleet_3, SpaceFleet) and isinstance(self._fleet_3.modules, ModuleAndBonuses):
            if (isinstance(data, list) or isinstance(data, tuple)):
                self._fleet_3.set_module_attack_damage_mods(*data)
            elif isinstance(data, dict):
                self._fleet_3.set_module_attack_damage_mods(data)

    def set_fleet_3_module_defense_bonuses(self, data: Union[list,tuple,dict]) -> None:
        """Not necessary.

            Set defense bonuses for each damage type.
            Input is either a list or a tuple of pairs of list or tuple (id,value):
            [(1, 1.0), (5, 1.2), (3, 1.1), (4, 1.3), (2, 1.5)]. Order doesn't matter, damage types may be omitted -> no bonus.
            Or a dictionary where key is damage type id and value is the bonus.
        """

        if isinstance(self._fleet_3, SpaceFleet) and isinstance(self._fleet_3.modules, ModuleAndBonuses):
            if (isinstance(data, list) or isinstance(data, tuple)):
                self._fleet_3.set_module_defense_damage_mods(*data)
            elif isinstance(data, dict):
                self._fleet_3.set_module_defense_damage_mods(data)

    def set_planet(self, planet_type: int, planet_size: int, turrets_lvl: int = False) -> None:
        """Sets Planet's mandatory params.

            turrets_lvl = False if you are going to set buildings or
            int number = sum of all turrets levels;

            planet_type in (1,...,7,9,12,15) and
            planet_size in (0,1,2) where 0 - 3 mines, 1 - 4 mines, 2 - 5 mines

            see help_game_parameters().
        """

        if planet_type in battlesimulation._GGP.types_planet_type and planet_size in battlesimulation._GGP.types_planet_size \
                and isinstance(turrets_lvl, int) and turrets_lvl >= 0 and isinstance(self._planet, Planet):
            self._planet.set_planet_type_and_size(planet_type, planet_size)
            self._planet.set_simple_turrets_lvl(turrets_lvl)
    
    def set_planet_by_dict(self, planet_data: dict) -> None:
        """Sets planet by given dict.

            Example:

            planet_data = {"planet_type": 3, "planet_size": 2, "turrets_lvl": i.e. 137, 
            optional (you can specify buildings on the planet or just pass a number = sum of all turret levels), 
            "rockets": optional (see set_rockets), "buildings": optional, see set_buildings}
        """

        if isinstance(self._planet, Planet):
            self._planet.set_planet_params(planet_data)

    def set_rockets(self, rockets_data: Union[list,tuple,dict]) -> None:
        """Sets rockets.

            Accepts list or tuple of pairs of list or tuple ((id1,value1),(id1,value2))
            or dict of id:value keypair {id1:value1,id2:value2}.
            Ids should be valid and unique, otherwise the last id will overwrite previous.

            Default ids: 1 - Sticks-XL, 2 - Cobra-M1, 3 - Aurora, 4 - X-Ray.
        """

        if isinstance(self._planet, Planet):
            self._planet.set_rockets(rockets_data)

    def add_rocket(self, rocket_id: int, quantity: int) -> None:
        """Add single id Rocket to Planet, overwriting existing of the same id (if any).

            Default ids: 1 - Sticks-XL, 2 - Cobra-M1, 3 - Aurora, 4 - X-Ray.
        """

        self._planet.rockets.set_item_of_array((rocket_id, quantity))

    def reset_rockets_to_zero(self) -> None:
        """Reset Rockets on the Planet to zero quantity."""

        self._planet.rockets.set_to_zero()

    def set_buildings(self, buildings_data: Union[list,tuple,dict]) -> None:
        """Sets buildings.

            Accepts list or tuple of pairs of list or tuple ((id1,value1),(id1,value2))
            or dict of id:value keypair {id1:value1,id2:value2}.
            Ids should be valid and unique, otherwise the last id will overwrite previous.
            Also certain buildings have a maximum buildable number on a Planet.

            Default ids: 1 - Command Center, 2 - Mine, 3 - Warehouse, 4 - Trade Office, 5 - Cosmodrome,
            6 - Spacecraft Plant, 7 - Power Plant, 8 - Detection Station, 9 - Missile Turret, 10 - Shield Generator.
        """

        if isinstance(self._planet, Planet):
            self._planet.set_buildings(buildings_data)

    def add_building(self, building_id: int, level: int) -> None:
        """Add single id Building to Planet, if possible. And no overwriting.

            Default ids: 1 - Command Center, 2 - Mine, 3 - Warehouse, 4 - Trade Office, 5 - Cosmodrome,
            6 - Spacecraft Plant, 7 - Power Plant, 8 - Detection Station, 9 - Missile Turret, 10 - Shield Generator.
        """

        self._planet.buildings.set_item_of_array((building_id, level))

    def reset_all_buildings(self) -> None:
        """Completely remove all buildings on the Planet."""

        self._planet.buildings._reinit()

    def set_fleet_1_attacking(self, attack: bool = True) -> None:
        """Set Fleet 1 to use attack (True) or defense (False) priorities. Default is True."""

        if attack:
            self._fleet_1.attacking = True
        else:
            self._fleet_1.attacking = False

    def set_fleet_2_attacking(self, attack: bool = False) -> None:
        """Set Fleet 2 to use attack (True) or defense (False) priorities. Default is False."""

        if attack:
            self._fleet_2.attacking = True
        else:
            self._fleet_2.attacking = False

    def set_fleet_3_attacking(self, attack: bool = False) -> None:
        """Set Fleet 3 to use attack (True) or defense (False) priorities. Default is False."""

        if attack:
            self._fleet_3.attacking = True
        else:
            self._fleet_3.attacking = False

    def set_planet_attack_type(self, attack: bool = True) -> None:
        """True: Fleet 1 is attacking Planet. False: Fleet 1 is going to blockade Planet. Default is True."""

        if attack:
            self._attack_target = True
            self._fleet_1.attack_planet = True
        else:
            self._attack_target = False
            self._fleet_1.attack_planet = False

    def _print_context_branch_start(self) -> str:
        """Returns text for printing for starting Context Branch."""

        text = "\n\n\n"
        text += "###############################################\n"
        text += "############# Context Branch Start ############\n"
        text += "###############################################\n"
        text += "\n\n\n"
        text += f"Fleet 1: {self.context_branch._fleet_1.filtered_original_str}\n"
        text += f"Fleet 2: {self.context_branch._fleet_2.filtered_original_str}\n"
        text += f"Fleet 3: {self.context_branch._fleet_3.filtered_original_str}\n"
        text += f"Planet and Rockets:\n{self.context_branch._planet.filtered_str_full}"
        text += "\n\n\n"
        return text

    def _print_context_branch_end(self) -> str:
        """Returns text for printing for ending Context Branch."""

        text = "\n\n\n"
        if self.context_branch._attack_target:
            text += f"Fleet 1 Alive: {self.context_branch._fleet_1.filtered_alive_str}\n"
            text += f"Fleet 1 Dead: {self.context_branch._fleet_1.filtered_dead_str}\n"
            text += f"Cost of Fleet 1: {self.context_branch._fleet_1.cost_of_original}, "
            text += f"Cost of Fleet 1 destroyed Spaceships: {self.context_branch._fleet_1.cost_of_dead}\n"
            build_time_original = self.context_branch._fleet_1.build_time_of_original
            build_time_dead = self.context_branch._fleet_1.build_time_of_dead
            text += f"Build time of Fleet 1: {timedelta(seconds=build_time_original)}, "
            text += f"Build time of Fleet 1 destroyed Spaceships: {timedelta(seconds=build_time_dead)}\n"
            if any(self._fleet_3.fleet_original.values()):
                text += f"\n"
                text += f"Fleet 3 Alive: {self.context_branch._fleet_3.filtered_alive_str}\n"
                text += f"Fleet 3 Dead: {self.context_branch._fleet_3.filtered_dead_str}"
                text += f"Cost of Fleet 3: {self.context_branch._fleet_3.cost_of_original}, "
                text += f"Cost of Fleet 3 destroyed Spaceships: {self.context_branch._fleet_3.cost_of_dead}\n"
                build_time_original = self.context_branch._fleet_3.build_time_of_original
                build_time_dead = self.context_branch._fleet_3.build_time_of_dead
                text += f"Build time of Fleet 3: {timedelta(seconds=build_time_original)}, "
                text += f"Build time of Fleet 3 destroyed Spaceships: {timedelta(seconds=build_time_dead)}\n"
            text += f"\n"
            text += f"Fleet 2 Alive: {self.context_branch._fleet_2.filtered_alive_str}\n"
            text += f"Fleet 2 Dead: {self.context_branch._fleet_2.filtered_dead_str}\n"
            text += f"Cost of Fleet 2: {self.context_branch._fleet_2.cost_of_original}, "
            text += f"Cost of Fleet 2 destroyed Spaceships: {self.context_branch._fleet_2.cost_of_dead}\n"
            build_time_original = self.context_branch._fleet_2.build_time_of_original
            build_time_dead = self.context_branch._fleet_2.build_time_of_dead
            text += f"Build time of Fleet 2: {timedelta(seconds=build_time_original)}, "
            text += f"Build time of Fleet 2 destroyed Spaceships: {timedelta(seconds=build_time_dead)}\n"
        else:
            text += f"Fleet 1 Alive: {self.context_branch._fleet_1.filtered_alive_str}\n"
            text += f"Fleet 1 Dead: {self.context_branch._fleet_1.filtered_dead_str}\n"
            text += f"Cost of Fleet 1: {self.context_branch._fleet_1.cost_of_original}, "
            text += f"Cost of Fleet 1 destroyed Spaceships: {self.context_branch._fleet_1.cost_of_dead}\n"
            build_time_original = self.context_branch._fleet_1.build_time_of_original
            build_time_dead = self.context_branch._fleet_1.build_time_of_dead
            text += f"Build time of Fleet 1: {timedelta(seconds=build_time_original)}, "
            text += f"Build time of Fleet 1 destroyed Spaceships: {timedelta(seconds=build_time_dead)}\n"
            text += f"\n"
            text += f"Fleet 3 Alive: {self.context_branch._fleet_3.filtered_alive_str}\n"
            text += f"Fleet 3 Dead: {self.context_branch._fleet_3.filtered_dead_str}"
            text += f"Cost of Fleet 3: {self.context_branch._fleet_3.cost_of_original}, "
            text += f"Cost of Fleet 3 destroyed Spaceships: {self.context_branch._fleet_3.cost_of_dead}\n"
            build_time_original = self.context_branch._fleet_3.build_time_of_original
            build_time_dead = self.context_branch._fleet_3.build_time_of_dead
            text += f"Build time of Fleet 3: {timedelta(seconds=build_time_original)}, "
            text += f"Build time of Fleet 3 destroyed Spaceships: {timedelta(seconds=build_time_dead)}\n"
        text += "\n\n\n"
        text += "###############################################\n"
        text += "############## Context Branch End #############\n"
        text += "###############################################\n"
        text += "\n\n\n"
        return text

    def _print_simulate_start(self) -> str:
        """Returns text for printing for starting Battle Simulation."""

        text = "\n\n\n"
        text += "###############################################\n"
        text += "########## Start of Battle Simulation #########\n"
        text += "###############################################\n"
        text += "\n\n\n"
        text += f"Fleet 1: {self._fleet_1.filtered_original_str}\n"
        text += f"Fleet 2: {self._fleet_2.filtered_original_str}\n"
        text += f"Fleet 3: {self._fleet_3.filtered_original_str}\n"
        text += f"Planet and Rockets:\n{self._planet.filtered_str_full}"
        text += "\n\n\n"
        return text

    def _print_simulate_end(self) -> str:
        """Returns text for printing for ending Battle Simulation."""

        text = "\n\n\n"
        if self._attack_target:
            text += f"Fleet 1 Alive: {self._fleet_1.filtered_alive_str}\n"
            text += f"Fleet 1 Dead: {self._fleet_1.filtered_dead_str}\n"
            text += f"Cost of Fleet 1: {self._fleet_1.cost_of_original}, "
            text += f"Cost of Fleet 1 destroyed Spaceships: {self._fleet_1.cost_of_dead}\n"
            build_time_original = self._fleet_1.build_time_of_original
            build_time_dead = self._fleet_1.build_time_of_dead
            text += f"Build time of Fleet 1: {timedelta(seconds=build_time_original)}, "
            text += f"Build time of Fleet 1 destroyed Spaceships: {timedelta(seconds=build_time_dead)}\n"
            if any(self._fleet_3.fleet_original.values()):
                text += f"\n"
                text += f"Fleet 3 Alive: {self._fleet_3.filtered_alive_str}\n"
                text += f"Fleet 3 Dead: {self._fleet_3.filtered_dead_str}\n"
                text += f"Cost of Fleet 3: {self._fleet_3.cost_of_original}, "
                text += f"Cost of Fleet 3 destroyed Spaceships: {self._fleet_3.cost_of_dead}\n"
                build_time_original = self._fleet_3.build_time_of_original
                build_time_dead = self._fleet_3.build_time_of_dead
                text += f"Build time of Fleet 3: {timedelta(seconds=build_time_original)}, "
                text += f"Build time of Fleet 3 destroyed Spaceships: {timedelta(seconds=build_time_dead)}\n"
            text += f"\n"
            text += f"Fleet 2 Alive: {self._fleet_2.filtered_alive_str}\n"
            text += f"Fleet 2 Dead: {self._fleet_2.filtered_dead_str}\n"
            text += f"Cost of Fleet 2: {self._fleet_2.cost_of_original}, "
            text += f"Cost of Fleet 2 destroyed Spaceships: {self._fleet_2.cost_of_dead}\n"
            build_time_original = self._fleet_2.build_time_of_original
            build_time_dead = self._fleet_2.build_time_of_dead
            text += f"Build time of Fleet 2: {timedelta(seconds=build_time_original)}, "
            text += f"Build time of Fleet 2 destroyed Spaceships: {timedelta(seconds=build_time_dead)}\n"
        else:
            text += f"Fleet 1 Alive: {self._fleet_1.filtered_alive_str}\n"
            text += f"Fleet 1 Dead: {self._fleet_1.filtered_dead_str}\n"
            text += f"Cost of Fleet 1: {self._fleet_1.cost_of_original}, "
            text += f"Cost of Fleet 1 destroyed Spaceships: {self._fleet_1.cost_of_dead}\n"
            build_time_original = self._fleet_1.build_time_of_original
            build_time_dead = self._fleet_1.build_time_of_dead
            text += f"Build time of Fleet 1: {timedelta(seconds=build_time_original)}, "
            text += f"Build time of Fleet 1 destroyed Spaceships: {timedelta(seconds=build_time_dead)}\n"
            text += f"\n"
            text += f"Fleet 3 Alive: {self._fleet_3.filtered_alive_str}\n"
            text += f"Fleet 3 Dead: {self._fleet_3.filtered_dead_str}\n"
            text += f"Cost of Fleet 3: {self._fleet_3.cost_of_original}, "
            text += f"Cost of Fleet 3 destroyed Spaceships: {self._fleet_3.cost_of_dead}\n"
            build_time_original = self._fleet_3.build_time_of_original
            build_time_dead = self._fleet_3.build_time_of_dead
            text += f"Build time of Fleet 3: {timedelta(seconds=build_time_original)}, "
            text += f"Build time of Fleet 3 destroyed Spaceships: {timedelta(seconds=build_time_dead)}\n"
        text += "\n\n\n"
        text += "###############################################\n"
        text += "########### End of Battle Simulation ##########\n"
        text += "###############################################\n"
        text += "\n\n\n"
        return text

    def _print_combined_results(self) -> str:
        """Returns text for printing for main and context branch results."""

        text = ""
        text += "\n\n\n"
        text += "###############################################\n"
        text += "########## Combined Results of Battle #########\n"
        text += "###############################################\n"
        text += "\n\n\n"
        text += f"Fleet 1: {self._fleet_1.filtered_original_str}\n"
        text += f"Fleet 2: {self._fleet_2.filtered_original_str}\n"
        text += f"Fleet 3: {self._fleet_3.filtered_original_str}\n"
        text += f"Planet and Rockets:\n{self._planet.filtered_str_full_original}\n"
        text += f"_____________________________________________________________________________\n\n"

        text += f"Fleet 1 against accuracy type {self.context_branch._fleet_1.acc_type}:\n"
        text += f"Alive: {self.context_branch._fleet_1.filtered_alive_str}\n"
        text += f"Dead: {self.context_branch._fleet_1.filtered_dead_str}\n"
        text += f"     vs against accuracy type {self._fleet_1.acc_type}:\n"
        text += f"Alive: {self._fleet_1.filtered_alive_str}\n"
        text += f"Dead: {self._fleet_1.filtered_dead_str}\n\n"
        text += f"Cost of full Fleet 1: {self._fleet_1.cost_of_original}\n"
        text += f"Fleet 1 against accuracy type {self.context_branch._fleet_1.acc_type}:\n"
        text += f"Cost of destroyed Spaceships: {self.context_branch._fleet_1.cost_of_dead}\n"
        text += f"     vs against accuracy type {self._fleet_1.acc_type}:\n"
        text += f"Cost of destroyed Spaceships: {self._fleet_1.cost_of_dead}\n\n"
        build_time_original = self.context_branch._fleet_1.build_time_of_original
        build_time_dead = self.context_branch._fleet_1.build_time_of_dead
        text += f"Build time of full Fleet 1: {timedelta(seconds=build_time_original)}\n"
        text += f"Fleet 1 against accuracy type {self.context_branch._fleet_1.acc_type}:\n"
        text += f"Build time of destroyed Spaceships: {timedelta(seconds=build_time_dead)}\n"
        build_time_dead = self._fleet_1.build_time_of_dead
        text += f"     vs against accuracy type {self._fleet_1.acc_type}:\n"
        text += f"Build time of destroyed Spaceships: {timedelta(seconds=build_time_dead)}\n"
        text += f"_____________________________________________________________________________\n\n"
        if any(self._fleet_3.fleet_original.values()):
            text += f"Fleet 3 against accuracy type {self.context_branch._fleet_3.acc_type}:\n"
            text += f"Alive: {self.context_branch._fleet_3.filtered_alive_str}\n"
            text += f"Dead: {self.context_branch._fleet_3.filtered_dead_str}\n"
            text += f"     vs against accuracy type {self._fleet_3.acc_type}:\n"
            text += f"Alive: {self._fleet_3.filtered_alive_str}\n"
            text += f"Dead: {self._fleet_3.filtered_dead_str}\n\n"
            text += f"Cost of Fleet 3: {self.context_branch._fleet_3.cost_of_original}\n"
            text += f"Fleet 3 against accuracy type {self.context_branch._fleet_3.acc_type}:\n"
            text += f"Cost of destroyed Spaceships: {self.context_branch._fleet_3.cost_of_dead}\n"
            text += f"     vs against accuracy type {self._fleet_3.acc_type}:\n"
            text += f"Cost of destroyed Spaceships: {self._fleet_3.cost_of_dead}\n\n"
            build_time_original = self.context_branch._fleet_3.build_time_of_original
            build_time_dead = self.context_branch._fleet_3.build_time_of_dead
            text += f"Build time of full Fleet: {timedelta(seconds=build_time_original)}\n"
            text += f"Fleet 3 against accuracy type {self.context_branch._fleet_3.acc_type}:\n"
            text += f"Build time of destroyed Spaceships: {timedelta(seconds=build_time_dead)}\n"
            build_time_dead = self._fleet_3.build_time_of_dead
            text += f"     vs against accuracy type {self._fleet_3.acc_type}:\n"
            text += f"Build time of destroyed Spaceships: {timedelta(seconds=build_time_dead)}\n"
            text += f"_____________________________________________________________________________\n\n"
        if self._attack_target:
            text += f"Fleet 2 against accuracy type {self.context_branch._fleet_2.acc_type}:\n"
            text += f"Alive: {self.context_branch._fleet_2.filtered_alive_str}\n"
            text += f"Dead: {self.context_branch._fleet_2.filtered_dead_str}\n"
            text += f"     vs against accuracy type {self._fleet_2.acc_type}:\n"
            text += f"Alive: {self._fleet_2.filtered_alive_str}\n"
            text += f"Dead: {self._fleet_2.filtered_dead_str}\n\n"
            text += f"Cost of Fleet 2: {self.context_branch._fleet_2.cost_of_original}\n"
            text += f"Fleet 2 against accuracy type {self.context_branch._fleet_2.acc_type}:\n"
            text += f"Cost of destroyed Spaceships: {self.context_branch._fleet_2.cost_of_dead}\n"
            text += f"     vs against accuracy type {self._fleet_2.acc_type}:\n"
            text += f"Cost of destroyed Spaceships: {self._fleet_2.cost_of_dead}\n\n"
            build_time_original = self.context_branch._fleet_2.build_time_of_original
            build_time_dead = self.context_branch._fleet_2.build_time_of_dead
            text += f"Build time of full Fleet: {timedelta(seconds=build_time_original)}\n"
            text += f"Fleet 2 against accuracy type {self.context_branch._fleet_2.acc_type}:\n"
            text += f"Build time of destroyed Spaceships: {timedelta(seconds=build_time_dead)}\n"
            build_time_dead = self._fleet_2.build_time_of_dead
            text += f"     vs against accuracy type {self._fleet_2.acc_type}:\n"
            text += f"Build time of destroyed Spaceships: {timedelta(seconds=build_time_dead)}\n"
            text += f"_____________________________________________________________________________\n\n"

        return text

    def _print_pretty_ranges_text(self) -> str:
        """Returns text for printing for every Fleet with ranges of dead or alive Spaceships."""

        text = ""
        if self._fleet_1.was_populated:
            fleet1_dead_ranges = self._make_dict_for_accuracy_ranges(self.context_branch._fleet_1, self._fleet_1, "dead")
            fleet1_dead_ranges_text = self._make_text_for_accuracy_ranges(fleet1_dead_ranges, "destroyed", True)
            fleet1_alive_ranges = self._make_dict_for_accuracy_ranges(self.context_branch._fleet_1, self._fleet_1, "alive")
            fleet1_alive_ranges_text = self._make_text_for_accuracy_ranges(fleet1_alive_ranges, "survived", True)

        if self._fleet_2.was_populated:
            fleet2_dead_ranges = self._make_dict_for_accuracy_ranges(self.context_branch._fleet_2, self._fleet_2, "dead")
            fleet2_dead_ranges_text = self._make_text_for_accuracy_ranges(fleet2_dead_ranges, "destroyed", True)
            fleet2_alive_ranges = self._make_dict_for_accuracy_ranges(self.context_branch._fleet_2, self._fleet_2, "alive")
            fleet2_alive_ranges_text = self._make_text_for_accuracy_ranges(fleet2_alive_ranges, "survived", True)

        if self._fleet_3.was_populated:
            fleet3_dead_ranges = self._make_dict_for_accuracy_ranges(self.context_branch._fleet_3, self._fleet_3, "dead")
            fleet3_dead_ranges_text = self._make_text_for_accuracy_ranges(fleet3_dead_ranges, "destroyed", True)
            fleet3_alive_ranges = self._make_dict_for_accuracy_ranges(self.context_branch._fleet_3, self._fleet_3, "alive")
            fleet3_alive_ranges_text = self._make_text_for_accuracy_ranges(fleet3_alive_ranges, "survived", True)

        if self._fleet_1.was_populated:
            text += "\nPossible result ranges for Fleet 1:\n"
            text += fleet1_dead_ranges_text
            text += fleet1_alive_ranges_text
            text += "\n"

        if self._fleet_2.was_populated:
            text += "\nPossible result ranges for Fleet 2:\n"
            text += fleet2_dead_ranges_text
            text += fleet2_alive_ranges_text
            text += "\n"

        if self._fleet_3.was_populated:
            text += "\nPossible result ranges for Fleet 3:\n"
            text += fleet3_dead_ranges_text
            text += fleet3_alive_ranges_text
            text += "\n"
        return text

    def _simulate_fleet_1_vs_fleet_3(self) -> None:
        """Fleet 1 vs Fleet 3 simulation part."""

        if self._fleet_1.is_populated and self._fleet_3.is_populated:
            self._battle_simulation._finalize_bonuses_mods(self._fleet_1, self._fleet_3)
            self._battle_simulation._wrapper_fleet_vs_fleet_damage_dealer(self._fleet_1, self._fleet_3)
            #self._fleet_1.finalize_battle_results()
            #self._fleet_3.finalize_battle_results()
            self._fleet_1.incoming_damage_array._reinit()
        else:
            debug_print("Nothing to do in simulate Fleet 1 vs Fleet 3.")

    def _simulate_fleet_1_vs_rockets(self) -> None:
        """Fleet 1 vs Rockets simulation part."""

        if self._fleet_1.is_populated and self._planet.rockets.is_populated(self._fleet_1, self._attack_target):
            self._battle_simulation._wrapper_rockets_damage_dealer(self._fleet_1, \
                    self._planet, target_blockade=not self._attack_target)
        else:
            debug_print("Nothing to do in simulate Fleet 1 vs Rockets for type %s Planet." % ('attack' if self._attack_target else 'blockade'))

    def _simulate_fleet_1_vs_turrets(self) -> None:
        """Fleet 1 vs Turrets simulation part."""

        if self._fleet_1.is_populated and self._planet.turrets_lvl > 0:
            self._battle_simulation._wrapper_turrets_damage_dealer(self._fleet_1, self._planet)
        else:
            debug_print("Nothing to do in simulate Fleet 1 vs Turrets.")

    def _simulate_fleet_1_vs_fleet_2(self) -> None:
        """Fleet 1 vs Fleet 2 simulation part."""

        if self._fleet_1.is_populated and self._fleet_2.is_populated:
            self._battle_simulation._finalize_bonuses_mods(self._fleet_1, self._fleet_2)
            self._battle_simulation._wrapper_fleet_vs_fleet_damage_dealer(self._fleet_1, self._fleet_2)
            #self._fleet_1.finalize_battle_results()
            #self._fleet_2.finalize_battle_results()
        else:
            debug_print("Nothing to do in simulate Fleet 1 vs Fleet 2.")

    def _check_acc_type_of_fleets_for_a_context_branch(self) -> bool:
        """Checks the need to instantiate another Context class for additional use of accuracy."""

        flag_to_make_context_branch = False
        if self._fleet_1.get_acc_type() in ("range_min","range_max"):
            flag_to_make_context_branch = True
        if self._fleet_2.get_acc_type() in ("range_min","range_max"):
            flag_to_make_context_branch = True
        if self._fleet_3.get_acc_type() in ("range_min","range_max"):
            flag_to_make_context_branch = True
        return flag_to_make_context_branch

    def _check_single_fleet_acc_type_and_return_opposite_range_value(self, fleet: SpaceFleet) -> str:
        """Checks if SpaceFleet's accuracy_type.

           If it is set to range_max or range_min, sets it to simple max or min and returns the opposite type.
        """

        if isinstance(fleet, SpaceFleet):
            if fleet.get_acc_type() == "range_min":
                fleet.set_acc_type("min")
                return "max"
            elif fleet.get_acc_type() == "range_max":
                fleet.set_acc_type("max")
                return "min"

    def _check_top_sorted_length(self) -> None:
        """Checks if top sorted length is valid and inside bounds."""

        if not isinstance(self._top_sorted_length, int):
            self._top_sorted_length = 5
        if self._top_sorted_length < 0 or self._top_sorted_length > len(self._fleet_finder_raw_results_dict):
            self._top_sorted_length = len(self._fleet_finder_raw_results_dict)

    def _manage_context_branch_instancing(self) -> None:
        """Creates new Context in self.context_branch and sets its params."""

        self.context_branch = Context()

        self.context_branch._fleet_1 = self._fleet_1.make_a_copy_of_self()
        self.context_branch._fleet_2 = self._fleet_2.make_a_copy_of_self()
        self.context_branch._fleet_3 = self._fleet_3.make_a_copy_of_self()

        fleet_1_acc_type = self._check_single_fleet_acc_type_and_return_opposite_range_value(self._fleet_1)
        if fleet_1_acc_type in ("min","max"):
            self.context_branch._fleet_1.set_acc_type(fleet_1_acc_type)

        fleet_2_acc_type = self._check_single_fleet_acc_type_and_return_opposite_range_value(self._fleet_2)
        if fleet_2_acc_type in ("min","max"):
            self.context_branch._fleet_2.set_acc_type(fleet_2_acc_type)

        fleet_3_acc_type = self._check_single_fleet_acc_type_and_return_opposite_range_value(self._fleet_3)
        if fleet_3_acc_type in ("min","max"):
            self.context_branch._fleet_3.set_acc_type(fleet_3_acc_type)
        
        self.context_branch._planet = self._planet.make_a_copy_of_self()
        self.context_branch._attack_target = self._attack_target

    def _make_dict_for_accuracy_ranges(self, fleet1: SpaceFleet, fleet2: SpaceFleet, for_type: str = "dead") -> dict:
        """Creates dict with dead or alive Spaceship quantities for when context_branch is used.

            params: fleet1 and fleet2 is the same Fleet, 1 is for range_min and 2 for range_max accuracy setting.
            returns: dict = {"min": {id1: amount, id2: amount, ... , id9: amount}, "max": {id1: amount, id2: amount, ... , id9: amount}}

            N.B. accuracy settings of other Fleets (that did damage to passed Fleet) affects results.
        """

        if for_type not in ("dead","alive"):
            for_type = "dead"

        result = {"min": {}, "max": {}}
        if isinstance(fleet1, SpaceFleet) and isinstance(fleet2, SpaceFleet):
            for ss in fleet1:
                if isinstance(ss, Spaceship):
                    if for_type == "dead":
                        orig_v = ss.original_quantity
                        value = orig_v - ss.quantity
                    else:
                        orig_v = ss.original_quantity
                        value = ss.quantity
                    result["min"].update({ss.id: (value, orig_v)})
            for ss in fleet2:
                if isinstance(ss, Spaceship):
                    if for_type == "dead":
                        orig_v = ss.original_quantity
                        value = orig_v - ss.quantity
                    else:
                        orig_v = ss.original_quantity
                        value = ss.quantity
                    result["max"].update({ss.id: (value, orig_v)})
        return result

    def _make_text_for_accuracy_ranges(self, result_dict_for_accuracy_ranges: dict, type_str: str = "destroyed", \
                filtered: bool = True) -> str:
        """Makes text for passed dict from _make_dict_for_accuracy_ranges.

            params: type_str will be added to text to mark result,
            filtered if True will add only non-zero quantities.
        """

        max_quantity_min_str_length = 0
        max_spaceship_name_length = 0
        spaceship_names_list = []
        quantity_min_str_list = []
        quantity_max_str_list = []
        text = f"\nSpaceship name: min {type_str} <-> max {type_str}\n"
        if isinstance(result_dict_for_accuracy_ranges, dict) and len(result_dict_for_accuracy_ranges) == 2 and \
                "min" in result_dict_for_accuracy_ranges and "max" in result_dict_for_accuracy_ranges:
            sub_min = result_dict_for_accuracy_ranges["min"]
            sub_max = result_dict_for_accuracy_ranges["max"]
            if isinstance(sub_min, dict) and isinstance(sub_max, dict) and set(sub_min.keys()) == set(sub_max.keys()):
                for ss_id in sub_min:
                    if isinstance(sub_min[ss_id], tuple) and len(sub_min[ss_id]) == 2 and isinstance(sub_max[ss_id], tuple) and len(sub_max[ss_id]) == 2:
                        spaceship_name = None
                        if filtered:
                            if sub_min[ss_id][1]:
                                spaceship_name = f"{battlesimulation._GGP.spaceships[ss_id]['name_en']}: "
                                if sub_min[ss_id][0] < sub_max[ss_id][0]:
                                    quantity_min_str = f"{sub_min[ss_id][0]} <-> "
                                    quantity_max_str = f"{sub_max[ss_id][0]} out of {sub_min[ss_id][1]}"
                                else:
                                    quantity_min_str = f"{sub_max[ss_id][0]} <-> "
                                    quantity_max_str = f"{sub_min[ss_id][0]} out of {sub_min[ss_id][1]}"
                        else:
                            spaceship_name = f"{battlesimulation._GGP.spaceships[ss_id]['name_en']}: "
                            if sub_min[ss_id][0] < sub_max[ss_id][0]:
                                quantity_min_str = f"{sub_min[ss_id][0]} <-> "
                                quantity_max_str = f"{sub_max[ss_id][0]} out of {sub_min[ss_id][1]}"
                            else:
                                quantity_min_str = f"{sub_max[ss_id][0]} <-> "
                                quantity_max_str = f"{sub_min[ss_id][0]} out of {sub_min[ss_id][1]}"
                        if spaceship_name is not None:
                            if max_quantity_min_str_length < len(quantity_min_str):
                                max_quantity_min_str_length = len(quantity_min_str)
                            if max_spaceship_name_length < len(spaceship_name):
                                max_spaceship_name_length = len(spaceship_name)
                            spaceship_names_list.append(spaceship_name)
                            quantity_min_str_list.append(quantity_min_str)
                            quantity_max_str_list.append(quantity_max_str)
        for i in range(len(spaceship_names_list)):
            spacing = (max_spaceship_name_length - len(spaceship_names_list[i]) + 4 + max_quantity_min_str_length - len(quantity_min_str_list[i])) * " "
            text += f"{spaceship_names_list[i]}{spacing}{quantity_min_str_list[i]}{quantity_max_str_list[i]}\n"
        return text

    def _make_text_for_costs_and_build_times_single_fleet(self, fleet: SpaceFleet) -> str:
        """Makes text for single SpaceFleet, consists of Alive Spaceships, Dead/Original costs and build times."""

        text = ""
        if isinstance(fleet, SpaceFleet):
            text += f"{fleet.filtered_alive_str}:\n"
            cost_str = f"Cost: {fleet.cost_of_dead} / {fleet.cost_of_original}"
            build_time_str = f"Build time: {timedelta(seconds=fleet.build_time_of_dead)} / {timedelta(seconds=fleet.build_time_of_original)}"
            text += f"Dead/Original: {cost_str}, {build_time_str}\n\n"
        return text

    def _make_text_for_costs_and_build_times_min_max(self, pair_of_fleets: Union[list,tuple]) -> str:
        """Makes text for min max results of finding suitable Fleet 1, consists of Alive Spaceships, Dead/Original costs and build times."""

        text = ""
        if (isinstance(pair_of_fleets, list) or isinstance(pair_of_fleets, tuple)) and len(pair_of_fleets) == 2:
            text += "\"Minimum\":\n"
            text += self._make_text_for_costs_and_build_times_single_fleet(pair_of_fleets[0])
            text += "\"Maximum\":\n"
            text += self._make_text_for_costs_and_build_times_single_fleet(pair_of_fleets[1])
        return text

    def make_text_for_costs_and_build_times(self, fleet_finder_dict: dict = None) -> str:
        """Makes text for results of finding suitable Fleet 1, consists of Alive Spaceships, Dead/Original costs and build times."""

        text = ""
        if fleet_finder_dict is None:
            fleet_finder_dict = self._fleet_finder_dict
        if isinstance(fleet_finder_dict, dict) and len(fleet_finder_dict):
            for ss_id in fleet_finder_dict:
                pair = fleet_finder_dict[ss_id]
                if (isinstance(pair, list) or isinstance(pair, tuple)) and len(pair) == 2:
                    text += f"{battlesimulation._GGP.spaceships[ss_id]['name_en']}:\n"
                    text += self._make_text_for_costs_and_build_times_min_max(pair)
                    text += "\n"
        return text

    def make_text_for_costs_and_build_times_for_top_sorted(self, top_sorted: dict, fleet_finder_dict: dict = None) -> str:
        """Makes text for results of finding suitable Fleet 1, consists of Alive Spaceships, Dead/Original costs and build times."""

        text = f"Top {self._top_sorted_length}, sorted in ascending order by cost and build times of the destroyed Spaceships:\n\n"
        if fleet_finder_dict is None:
            fleet_finder_dict = self._fleet_finder_dict
        if isinstance(top_sorted, dict) and len(top_sorted) == 2 and isinstance(fleet_finder_dict, dict) and len(fleet_finder_dict):
            if "min" in top_sorted and "max" in top_sorted:
                if isinstance(top_sorted["min"], list) and isinstance(top_sorted["max"], list):
                    text += "\"Minimum\":\n\n"
                    for ss_id in top_sorted["min"]:
                        text += f"{battlesimulation._GGP.spaceships[ss_id]['name_en']}:\n"
                        text += self._make_text_for_costs_and_build_times_single_fleet(fleet_finder_dict[ss_id][0])
                    text += "\n\n\"Maximum\":\n\n"
                    for ss_id in top_sorted["max"]:
                        text += f"{battlesimulation._GGP.spaceships[ss_id]['name_en']}:\n"
                        text += self._make_text_for_costs_and_build_times_single_fleet(fleet_finder_dict[ss_id][1])
        return text

    def find_suitable_fleet_branch(self) ->  None:
        """Finds suitable Fleet 1 to defeat the rest set Game objects.

            If Context._attack_target is False (Fleet 1 is going to make a blockade) then Fleet 2 is not going to take part in simulation.
            Don't forget to set Fleet 1 modules if you want to use them.

            You can manually check results in Context._fleet_finder_dict:
            _fleet_finder_dict = {spaceship_id_1: (SpaceFleet(min), SpaceFleet(max)), ..., spaceship_id_N: (SpaceFleet(min), SpaceFleet(max))}
        """

        raw_result_complicated = None
        raw_result_simple = None
        fleet_to_pass = None
        if self._attack_target and self._fleet_3.is_populated and self._fleet_2.is_populated:
            raw_result_complicated = self._battle_simulation.find_suitable_fleets_to_beat_two_subsequent_enemies(self._fleet_1.modules, \
                    self._fleet_2, self._fleet_3, self._planet, not self._attack_target, fleet1_acc_type=self._fleet_1.acc_type, \
                    var_to_save_spacefleet_1=self._fleet_finder_dict)
        else:
            if self._attack_target and self._fleet_3.is_populated:
                fleet_to_pass = self._fleet_3
            elif self._attack_target and self._fleet_2.is_populated:
                fleet_to_pass = self._fleet_2
            elif not self._attack_target and self._fleet_3.is_populated:
                fleet_to_pass = self._fleet_3
            raw_result_simple = self._battle_simulation.find_suitable_fleets_to_beat_enemy(self._fleet_1.modules, fleet_to_pass, self._planet, \
                    not self._attack_target, self._fleet_1.acc_type, var_to_save_spacefleet_1=self._fleet_finder_dict)

        raw_result = raw_result_complicated if raw_result_complicated is not None else raw_result_simple
        self._fleet_finder_raw_results_dict = raw_result
        debug_print(f"raw result for finding:\n{raw_result}")
        return raw_result

    def simulate(self) -> None:
        """Simulates Battle."""

        # Order of Battles:
        # If Fleet 1 is going to blockade the Planet
        #     If there is enemy's (enemy to Fleet 1) blockade
        #     1. Fleet 1 vs Fleet 3 - blockading Fleet 3 will fight with Fleet 1
        #     2. Rockets (Sticks and Aurora (if any)) will fire at Fleet 1
        # else (Fleet 1 is attacking the Planet):
        #     1. Fleet 1 vs Fleet 3 - blockading Fleet 3 will fight with Fleet 1 (doesn't matter if Fleet 1 is attacking or blockading)
        #     2. Fleet 1 vs Turrets -> Turrets fire passive damage before Rockets
        #     3. Fleet 1 vs Rockets (Cobra, Aurora and X-Ray (only against Valkyries))
        #     4. Fleet 1 vs Fleet 2
        # The End.

        if isinstance(self._fleet_1, SpaceFleet) and isinstance(self._fleet_2, SpaceFleet) \
                and isinstance(self._fleet_3, SpaceFleet) and isinstance(self._planet, Planet):

            if self._fleet_1.is_populated:
                # ok, will continue to do stuff
                pass
            else:
                # IF Fleet 1 is not set
                # then we assume the task is to find a proper Fleet 1 to successfully attack the rest set Game objects
                raw_result = self.find_suitable_fleet_branch()
                if len(self._fleet_finder_dict):
                    self._check_top_sorted_length()
                    top_sorted = self._battle_simulation.select_top_results_to_beat_enemy(raw_result, self._fleet_finder_dict, \
                            self._add_energy_cost_to_departure, self._coef_for_cost, self._coef_for_time, self._top_sorted_length)
                    self._fleet_finder_top_sorted_dict = top_sorted
                    self._text_for_finding_suitable_fleets = self.make_text_for_costs_and_build_times_for_top_sorted(top_sorted)
                    print("\n\n")
                    print(self._text_for_finding_suitable_fleets)
                    print("\n")
                return

            if self._fleet_1.custom_name == "SpaceFleet":
                self._fleet_1.custom_name = "1"
            if self._fleet_2.custom_name == "SpaceFleet":
                self._fleet_2.custom_name = "2"
            if self._fleet_3.custom_name == "SpaceFleet":
                self._fleet_3.custom_name = "3"
            self._fleet_1.acc_type = self._fleet_1_acc_type
            self._fleet_2.acc_type = self._fleet_2_acc_type
            self._fleet_3.acc_type = self._fleet_3_acc_type

            self._flag_to_make_context_branch = self._check_acc_type_of_fleets_for_a_context_branch()

            if self._flag_to_make_context_branch:
                self._manage_context_branch_instancing()
                #print(self._print_context_branch_start())
                print("\n\n############# Context Branch Start ############")
                self.context_branch.simulate()
                #print(self._print_context_branch_end())
                print("############## Context Branch End #############\n\n")

            # Fleet 1 is going to blockade the Planet
            if not self._attack_target:
                print(self._print_simulate_start())
                self._simulate_fleet_1_vs_fleet_3()
                # this is kind of rare (if possible) situation for Planet to have any anti blockade Rockets
                # to fire against Fleet 1, because those Rockets automatically fire at Fleet 3.
                # So probably we should finalize Fleet 1 results before rockets (?)
                # If Fleet 3 is actually a Support, sent by Planet's ally, 
                # then at this moment I don't know how Game mechanics DO work in this case.
                # TODO research
                self._fleet_1.finalize_battle_results()
                self._simulate_fleet_1_vs_rockets()
                self._fleet_1.finalize_battle_results()
                self._fleet_3.finalize_battle_results()
                print(self._print_simulate_end())
                return

            # Fleet 1 is attacking the Planet
            print(self._print_simulate_start())
            self._simulate_fleet_1_vs_fleet_3()
            self._simulate_fleet_1_vs_turrets()
            self._simulate_fleet_1_vs_rockets()
            self._simulate_fleet_1_vs_fleet_2()
            self._fleet_1.finalize_battle_results()
            self._fleet_2.finalize_battle_results()
            self._fleet_3.finalize_battle_results()
            print(self._print_simulate_end())

            if self._flag_to_make_context_branch:
                print(self._print_combined_results())
                print(self._print_pretty_ranges_text())

        return

    def old_simulate_bombardment(self) -> str:
        """Old Bombardment Mechanic, prints and returns text of numbers of Valkyries needed to destroy Planetary Defense.

            First you need to set Fleet 1 Module, then set Planet with buildings and rockets. Call this func and results will be printed.
            And saved in _results_for_old_bombardment (dict).

            This game mechanic is still in effect on live (main) Game Galaxies, but it's going to change.

            There is already a new Bombardment mechanic in the Closed Beta Test and in the special game mode called "Seasons".

            So this func will not be needed in the future.
        """

        self._results_for_old_bombardment = self._battle_simulation.old_simulate_bombardment(self._fleet_1.modules, self._planet)
        text = ""
        text += "\n\nOld Bombardment Calculations.\n"
        text += f"{self._planet.filtered_str_full}\n"
        text += f"Valkyries needed to destroy Shield Generator in one go: {self._results_for_old_bombardment['needed_for_shield']}\n"
        text += f"Valkyries destroyed after attack on the Shield Generator: {self._results_for_old_bombardment['dead_for_shield']}\n\n"
        text += f"Valkyries needed to destroy Turrets in one go and not touch other buildings: {self._results_for_old_bombardment['needed_for_turrets']}\n"
        text += f"Valkyries destroyed after attack on the Turrets: {self._results_for_old_bombardment['dead_for_turrets']}\n\n"
        text += f"Valkyries needed to destroy all other buildings (limit: only down to level 2) in one go: {self._results_for_old_bombardment['needed_for_buildings']}\n\n"
        print(text)
        return text

##############################################