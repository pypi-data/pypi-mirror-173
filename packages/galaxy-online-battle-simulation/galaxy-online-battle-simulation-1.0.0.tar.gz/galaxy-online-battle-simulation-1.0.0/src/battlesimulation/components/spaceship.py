from __future__ import annotations
from typing import Union
import random
import math
import battlesimulation
from battlesimulation import _BasicGameEntity, Damage
from battlesimulation.components.utility import _my_truncate, _my_round_threshold_up

##############################################

class Spaceship(_BasicGameEntity):
    """Spaceship class (general, base) representing a spaceship from game."""

    def _get_quantity(self) -> Union[int,float]:
        return self._value

    def _set_quantity(self, quantity: Union[int, float]) -> None:
        if isinstance(quantity, float):
            quantity = _my_truncate(quantity, 6)
        self._set_value(quantity)

    def _get_original_quantity(self) -> Union[int,float]:
        return self._original_value

    def _set_original_quantity(self, quantity: Union[int, float]) -> None:
        if isinstance(quantity, float):
            quantity = _my_truncate(quantity, 6)
        self._set_original_value(quantity)

    quantity = property(_get_quantity, _set_quantity)
    original_quantity = property(_get_original_quantity, _set_original_quantity)

    def __init__(self, id: int, quantity: Union[int, float] = 0) -> None:
        """New instance of Spaceship class.

            Default ids: 1 - Hercules, 2 - Loki, 3 - Raptor, 4 - Hornet, 5 - Javelin,
            6 - Excalibur, 7 - Valkyrie, 8 - Titan, 9 - Abaddon.
        """

        super().__init__(id, quantity, battlesimulation._GGP.types_spaceship, Spaceship, 6)

        self.name = battlesimulation._GGP.spaceships[id]["name"]
        self.name_en = battlesimulation._GGP.spaceships[id]["name_en"]
        self.damage_type_id = battlesimulation._GGP.spaceships[id]["damage_type_id"]
        self.attack = battlesimulation._GGP.spaceships[id]["attack"]
        self.defense = battlesimulation._GGP.spaceships[id]["defense"]
        self.defenses = battlesimulation._GGP.spaceships[id]["defenses"]
        self.weight = battlesimulation._GGP.spaceships[id]["weight"]
        self.attack_priority = battlesimulation._GGP.spaceships[id]["attack_priority"]
        self.defense_priority = battlesimulation._GGP.spaceships[id]["defense_priority"]
        self.speed = battlesimulation._GGP.spaceships[id]["speed"]
        self.calc_speed = battlesimulation._GGP.spaceships[id]["calc_speed"]
        self.price = battlesimulation._GGP.spaceships[id]["price"]
        self.build_time = battlesimulation._GGP.spaceships[id]["build_time"]
        self.cargohold = battlesimulation._GGP.spaceships[id]["cargohold"]
        self.radar = battlesimulation._GGP.spaceships[id]["radar"]
        self.accuracy = battlesimulation._GGP.spaceships[id]["accuracy"]

    def single_hp(self, defense_type: int, final_defense_mod: float) -> float:
        """Calculates single spaceship's HP with the defense mods for the specified defense type."""

        if defense_type in self.defenses and isinstance(final_defense_mod, float) and final_defense_mod > 0:
            return _my_truncate(self.defenses[defense_type] * final_defense_mod, 2)

    def total_hp(self, defense_type: int) -> float:
        """Calculates total HP of all spaceships (quantity is float) for the specified defense type."""

        if defense_type in self.defenses:
            return _my_truncate(self.defenses[defense_type] * self.quantity, 6)

    def get_accuracy(self, acc_type: str = "min") -> int:
        """Returns actual accuracy value (percent) for the specified type.
        
            acc_type can be "min", "max", "random", self explanatory.
        """

        if acc_type in ("min","range_min"):
            return self.accuracy
        elif acc_type in ("max","range_max"):
            return 100
        elif acc_type == "random":
            return random.randint(self.accuracy, 100)
        else:
            return self.accuracy

    def take_damage(self, damage: Damage, def_mod: float) -> None:
        """Take damage; manages if damage is not more than HP, etc."""

        if isinstance(damage, Damage) and isinstance(def_mod, float) and def_mod > 0:
            total_hp = self.total_hp(damage.damage_type_id) * def_mod
            left_hp = damage._subtract_value(total_hp)
            self._set_quantity(_my_truncate(left_hp / self.defenses[damage.damage_type_id] / def_mod, 6))

    def calc_travel_time(self, x1: int, y1: int, x2: int, y2: int, speed_mod: float = 1.0) -> float:
        """Takes in game coordinates and speed_mod (Modules.speed, default is 1.0). Returns time to travel between those coordinates with given speed_mod."""

        #default_ship_speeds_for_calculations = {1: 2.56, 2: 5.12, 3: 3.072, 4: 3.584, 5: 4.096, 6: 2.56, 7: 1.536, 8: 1.536, 9: 2.048}
        if isinstance(x1, int) and x1 > 0 and isinstance(x2, int) and x2 > 0 \
                and isinstance(y1, int) and y1 > 0 and isinstance(y2, int) and y2 > 0 \
                and isinstance(speed_mod, float) and speed_mod > 0 and isinstance(self.calc_speed, float) and self.calc_speed > 0:
            distance = math.sqrt((x1-x2)**2 + (y1-y2)**2)
            travel_time = distance / (self.calc_speed * speed_mod)

            return travel_time

    @property
    def total_defense(self) -> int:
        "Total defense of current quantity of spaceships. Used by Superiority game mechanic."

        total_defense = 0
        for id in self.defenses:
            total_defense += self.quantity * self.defenses[id]
        return total_defense

    @property
    def total_defense_single_spaceship(self) -> int:
        """Returns total defenses of one spaceship."""

        single_spaceship_defenses = 0
        for key in self.defenses:
            single_spaceship_defenses += self.defenses[key]
        return single_spaceship_defenses

    @property
    def alive(self) -> int:
        """How many spaceships are alive, game uses math rounding: 0.5 -> 1, 0.49 -> 0."""

        return int(_my_round_threshold_up(self.quantity, 0, battlesimulation._GGP.threshold))

    @property
    def cost_of_original(self) -> int:
        """Cost in energy of Spaceships quantity before any Battles."""

        return self._original_value * self.price

    @property
    def cost_of_dead(self) -> int:
        """Cost in energy of destroyed Spaceships."""

        return (self._original_value - self.alive) * self.price

    @property
    def build_time_of_original(self) -> int:
        """Time in seconds to build (at Spacecraft Plant level 1) Spaceships quantity before any Battles."""

        return self._original_value * self.build_time

    @property
    def build_time_of_dead(self) -> int:
        """Time in seconds to build (at Spacecraft Plant level 1) destroyed Spaceships."""

        return (self._original_value - self.alive) * self.build_time

    @property
    def detailed_str(self) -> str:
        """String with all Spaceship's attributes."""

        text = f"Spaceship: {self.quantity} of {self.name_en} (id {self.id})"
        text += f". Params: attack {self.attack} of {battlesimulation._GGP.damages[self.damage_type_id]['name_en']} damage"
        defense_type_str = "undefined"
        defense_type = None
        for dt in self.defenses:
            if self.defenses[dt] == self.defense:
                defense_type = dt
                break
        if defense_type:
            defense_type_str = battlesimulation._GGP.damages[defense_type]['name_en']
        text += f", base defense {self.defense} from {defense_type_str}"
        text += f", att/def priority {self.attack_priority}/{self.defense_priority}"
        text += f" and \"weight for calc\" {self.weight}"
        text += f", speed={self.speed}, price={self.price}, build time={self.build_time}"
        text += f" and cargohold={self.cargohold}"
        if self.radar > 0:
            text += f", radar strength={self.radar}"
        text += f"."
        return text

    @property
    def filtered_str(self) -> str:
        """Different short string of self attributes."""

        return f"{self.quantity} of {self.name_en}s"

    def __repr__(self) -> str:
        """Short string of self attributes."""

        return f"<Spaceship>: {self.quantity} of {self.name_en}s"

###############################################################################################
# named spaceships are not used in this particular module, but they are here if you need them #
###############################################################################################

class Hercules(Spaceship):
    def __init__(self, quantity: Union[int,float] = 0) -> None:
        super().__init__(1, quantity)

class Loki(Spaceship):
    def __init__(self, quantity: Union[int,float] = 0) -> None:
        super().__init__(2, quantity)

class Raptor(Spaceship):
    def __init__(self, quantity: Union[int,float] = 0) -> None:
        super().__init__(3, quantity)

class Hornet(Spaceship):
    def __init__(self, quantity: Union[int,float] = 0) -> None:
        super().__init__(4, quantity)

class Javelin(Spaceship):
    def __init__(self, quantity: Union[int,float] = 0) -> None:
        super().__init__(5, quantity)

class Excalibur(Spaceship):
    def __init__(self, quantity: Union[int,float] = 0) -> None:
        super().__init__(6, quantity)

class Valkyrie(Spaceship):
    def __init__(self, quantity: Union[int,float] = 0) -> None:
        super().__init__(7, quantity)

class Titan(Spaceship):
    def __init__(self, quantity: Union[int,float] = 0) -> None:
        super().__init__(8, quantity)

class Abaddon(Spaceship):
    def __init__(self, quantity: Union[int,float] = 0) -> None:
        super().__init__(9, quantity)

##############################################