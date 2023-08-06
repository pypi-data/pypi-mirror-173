from __future__ import annotations
from typing import Union
import battlesimulation
from battlesimulation.components.utility import _my_truncate

##############################################

class ModuleAndBonuses():
    """Module class representing a Game Module plus additional functionality for other bonuses."""

    def __init__(self) -> None:
        self.attack_damage_mods = {}
        self.defense_damage_mods = {}
        self.final_attack_damage_mods = {}
        self.final_defense_damage_mods = {}
        self.final_no_superiority_defense_damage_mods = {}
        self._reinit()

    def _reinit(self):
        self.id = -1
        self.level = 1
        self.attack = 1.0
        self.defense = 1.0
        self.speed = 1.0
        self.name = "Общий"
        self.name_en = "General"
        self.price = 1000
        self.solarium = 1
        self.build_time = 60
        self.attack_damage_mods.clear()
        self.defense_damage_mods.clear()
        self.final_defense_damage_mods.clear()
        for id in battlesimulation._GGP.types_damage:
            self.attack_damage_mods.update({id:1.0})
            self.defense_damage_mods.update({id:1.0})
            self.final_attack_damage_mods.update({id:1.0})
            self.final_defense_damage_mods.update({id:1.0})
            self.final_no_superiority_defense_damage_mods.update({id:1.0})

    def set_module_params(self, attack: Union[int,float] = None, defense: Union[int,float] = None, \
            speed: Union[int,float] = None) -> None:
        """Sets module bonuses for attack, defense and speed.

            Accepts int (percent (but times 100 for an option of 3725/10000 -> 37.25 bonus), 5000 -> 0.5 + 1 -> 1.5) or float (1.5).
            For the case of testing values can be a negative int (but not below -100*100 (not included) -> -9999) or 0 < float < 1.
            That is kinda antibonus.
            If value is omitted a default value of 1.0 will be used.
        """

        if isinstance(attack, int):
            attack = 1 + attack / 10000
        if isinstance(attack, float) and attack > 0:
            attack = _my_truncate(attack, 6, True)
            self.attack = attack
        if isinstance(defense, int):
            defense = 1 + defense / 10000
        if isinstance(defense, float) and defense > 0:
            defense = _my_truncate(defense, 6, True)
            self.defense = defense
        if isinstance(speed, int):
            speed = 1 + speed / 10000
        if isinstance(speed, float) and speed > 0:
            speed = _my_truncate(speed, 6, True)
            self.speed = speed

    def set_module_by_id(self, id: int, level: int = 100) -> None:
        """Set module by id and level to existing named Game Module.

            1 - Disintegrator, 2 - Afterburner, 3 - Shield Booster, 4 - Complex Bastion,
            5 - Complex Luch, 6 - Complex Halo, 7 - Complex Guardian,
            no bonuses:
            8 - Satellite Solarium, 9 - Satellite Energy, 10 - Complex Boarding.
        """

        if id in battlesimulation._GGP.types_module:
            if not isinstance(level, int):
                level = 100
            if battlesimulation._debug_limit_variables:
                if level < 0 or level > 100:
                    level = 100
            self.id = id
            self.level = level
            self.name = battlesimulation._GGP.modules[id]["name"]
            self.name_en = battlesimulation._GGP.modules[id]["name_en"]
            self.attack = 1 + battlesimulation._GGP.modules[id]["attack"] * level / 10000
            self.defense = 1 + battlesimulation._GGP.modules[id]["defense"] * level / 10000
            self.speed = 1 + battlesimulation._GGP.modules[id]["speed"] * level / 10000
            self.price = battlesimulation._GGP.modules[id]["price"]
            self.solarium = battlesimulation._GGP.modules[id]["solarium"]
            self.build_time = battlesimulation._GGP.modules[id]["build_time"]

    def set_attack_damage_mods(self, data: Union[list,tuple,dict]):
        """Sets attack damage mods (for example for Commanders in the future or for tests).

            Accepts input data of list or tuple of pairs (also list or tuple): ((id1,value1),(id2,value2)) or dict {id1:value1,id2:value2}.
            Ids should be valid and unique, otherwise the last id will overwrite previous.
            Values should be int (percent but times 100, i.e. 5000 -> 1.5) or float (1.5).
            For the case of testing values can be a negative int (but not below -100*100 (not included) -> -9999) or 0 < float < 1.
            Ids may be omitted and default value of 1.0 will be used for them.
        """

        self._set_damage_mods(data, "attack")

    def set_defense_damage_mods(self, data: Union[list,tuple,dict]):
        """Sets defense damage mods (for example for Commanders in the future or for tests).

            Accepts input data of list or tuple of pairs (also list or tuple): ((id1,value1),(id2,value2)) or dict {id1:value1,id2:value2}.
            Ids should be valid and unique, otherwise the last id will overwrite previous.
            Values should be int (percent but times 100, i.e. 5000 -> 1.5) or float (1.5).
            For the case of testing values can be a negative int (but not below -100*100 (not included) -> -9999) or 0 < float < 1.
            Ids may be omitted and default value of 1.0 will be used for them.
        """

        self._set_damage_mods(data, "defense")

    def _set_damage_mods(self, data: Union[list,tuple,dict], target: str):
        """Inner setter of attack/defense damage mods.

            Better look at set_attack_damage_mods and/or set_defense_damage_mods descriptions.
        """

        result = {}
        if isinstance(data, list) or isinstance(data, tuple):
            for pair in data:
                if (isinstance(pair, list) or isinstance(pair, tuple)) and len(pair) == 2:
                    id, value = pair
                    if id in battlesimulation._GGP.types_damage:
                        if isinstance(value, int):
                            value = 1 + value / 10000
                        if isinstance(value, float) and value > 0:
                            value = _my_truncate(value, 6, True)
                            result.update({id: value})
        elif isinstance(data, dict):
            for id in data:
                value = data[id]
                if id in battlesimulation._GGP.types_damage:
                    if isinstance(value, int):
                        value = 1 + value / 10000
                    if isinstance(value, float) and value > 0:
                        value = _my_truncate(value, 6, True)
                        result.update({id: value})
        if target == "attack":
            self.attack_damage_mods.update(result)
        elif target == "defense":
            self.defense_damage_mods.update(result)
        else:
            pass

    def calc_final_damage_mods(self, superiority: float, combination_module: str = "add", \
            combination_superiority: str = "add", combination_damage: str = "add", \
            sequence: Union[list,tuple] = ("module","superiority","damage"), \
            truncate_to: int = 6) -> None:
        """Combines bonuses from Modules with from Modules attack/defense damage specific and with superiority bonus.

            There are two ways to combine bonuses: add percentage or multiply fractions.
            Also you can define the order in which those combinations will be done.
        """

        if isinstance(superiority, float) and superiority >= 1.0 and \
                (isinstance(sequence, list) or isinstance(sequence, tuple)) and len(sequence) == 3:
            result_attack = {}
            result_defense = {}
            result_no_superiority_defense = {}
            for id in battlesimulation._GGP.types_damage:
                result_attack.update({id:1.0})
                result_defense.update({id:1.0})
                result_no_superiority_defense.update({id:1.0})
            for operation in sequence:
                if operation == "module":
                    if combination_module == "add":
                        for id in result_attack:
                            result_attack[id] += self.attack - 1
                            result_defense[id] += self.defense - 1
                            result_no_superiority_defense[id] += self.defense - 1
                    elif combination_module == "multiply":
                        for id in result_attack:
                            result_attack[id] *= self.attack
                            result_defense[id] *= self.defense
                            result_no_superiority_defense[id] *= self.defense
                    else:
                        # don't combine modules
                        pass
                elif operation == "superiority":
                    if combination_superiority == "add":
                        for id in result_defense:
                            result_defense[id] += superiority - 1
                    elif combination_superiority == "multiply":
                        for id in result_defense:
                            result_defense[id] *= superiority
                    else:
                        # don't combine superiority mod
                        pass
                elif operation == "damage":
                    if combination_damage == "add":
                        for id in result_attack:
                            result_attack[id] += self.attack_damage_mods[id] - 1
                            result_defense[id] += self.defense_damage_mods[id] - 1
                            result_no_superiority_defense[id] += self.defense_damage_mods[id] - 1
                    elif combination_damage == "multiply":
                        for id in result_attack:
                            result_attack[id] *= self.attack_damage_mods[id]
                            result_defense[id] *= self.defense_damage_mods[id]
                            result_no_superiority_defense[id] *= self.defense_damage_mods[id]
                    else:
                        # don't combine damage mods
                        pass
            for id in result_attack:
                result_attack[id] = _my_truncate(result_attack[id], truncate_to)
                if result_attack[id] <= 0:
                    result_attack[id] = 0.000001
                result_defense[id] = _my_truncate(result_defense[id], truncate_to)
                result_no_superiority_defense[id] = _my_truncate(result_no_superiority_defense[id], truncate_to)
                if result_defense[id] <= 0:
                    result_defense[id] = 0.000001
                if result_no_superiority_defense[id] <= 0:
                    result_no_superiority_defense[id] = 0.000001
            self.final_attack_damage_mods = result_attack
            self.final_defense_damage_mods = result_defense
            self.final_no_superiority_defense_damage_mods = result_no_superiority_defense

    def make_a_copy_of_self(self) -> ModuleAndBonuses:
        """Return a new instance of ModuleAndBonuses with the same attributes."""

        new_module = ModuleAndBonuses()
        if self.id in battlesimulation._GGP.types_module:
            new_module.set_module_by_id(self.id, self.level)
        else:
            new_module.set_module_params(self.attack, self.defense, self.speed)
        new_module.attack_damage_mods = self.attack_damage_mods.copy()
        new_module.defense_damage_mods = self.defense_damage_mods.copy()
        new_module.final_attack_damage_mods = self.final_attack_damage_mods.copy()
        new_module.final_defense_damage_mods = self.final_defense_damage_mods.copy()
        new_module.final_no_superiority_defense_damage_mods = self.final_no_superiority_defense_damage_mods.copy()
        return new_module

    @property
    def filtered_str_short(self) -> str:
        """Short string for basic Module."""

        return f"{self.name_en} Module level {self.level}: fractioned bonuses:\nA/D/S: {self.attack}/{self.defense}/{self.speed},\n"

    def __repr__(self) -> str:
        """Short string of self attributes."""

        text = f"{self.name_en} Module: A/D/S: {self.attack}/{self.defense}/{self.speed},\n"
        text += f"att dmg mods: {self.attack_damage_mods},\ndef dmg mods: {self.defense_damage_mods},\n"
        text += f"final att mods: {self.final_attack_damage_mods},\nfinal def mods: {self.final_defense_damage_mods},\n"
        text += f"final no superiority def mods: {self.final_no_superiority_defense_damage_mods}"
        return text

##############################################