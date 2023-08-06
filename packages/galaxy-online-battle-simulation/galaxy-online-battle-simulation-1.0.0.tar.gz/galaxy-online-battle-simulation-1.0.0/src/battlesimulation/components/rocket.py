from __future__ import annotations
from typing import Union
import battlesimulation
from battlesimulation import _BasicGameEntity, _BasicGameEntityArray

##############################################

class Rocket(_BasicGameEntity):
    """Rocket class with specific number of warheads, damage of each warhead, attack type (blockade or attack), valid targets."""

    def _get_quantity(self) -> int:
        return self._value

    def _set_quantity(self, quantity: int) -> None:
        if isinstance(quantity, int) and quantity >= 0:
            self._set_value(quantity)
    
    def _get_original_quantity(self) -> int:
        return self._original_value

    def _set_original_quantity(self, quantity: int) -> None:
        if isinstance(quantity, int) and quantity >= 0:
            self._set_original_value(quantity)
    
    quantity = property(_get_quantity, _set_quantity)
    original_quantity = property(_get_original_quantity, _set_original_quantity)

    def __init__(self, id: int, quantity: int = 0) -> None:
        """New instance of Rocket class.

            Default ids: 1 - Sticks-XL, 2 - Cobra-M1, 3 - Aurora, 4 - X-Ray.
        """

        super().__init__(id, quantity, battlesimulation._GGP.types_rocket, Rocket, None)

        self.name = battlesimulation._GGP.rockets[id]["name"]
        self.name_en = battlesimulation._GGP.rockets[id]["name_en"]
        self.warheads = battlesimulation._GGP.rockets[id]["warheads"]
        self.damage = battlesimulation._GGP.rockets[id]["damage"]
        self.price = battlesimulation._GGP.rockets[id]["price"]
        self.build_time = battlesimulation._GGP.rockets[id]["build_time"]
        self.damage_type_id = battlesimulation._GGP.rockets[id]["damage_type_id"]
        self.attack_type = battlesimulation._GGP.rockets[id]["attack_type"]
        self.valid_targets = battlesimulation._GGP.rockets[id]["valid_targets"]

    def reset_quantity(self, quantity: int, original_quantity: int = None) -> None:
        """Set self.quantity with given and set self.original_quantity with original_quantity (if specified) or just quantity."""

        self._reset_value(quantity, original_quantity)

    def reset_original_quantity(self):
        """Reset self.original_quantity with self.quantity."""

        self._reset_original_value()

    def add_rocket(self, rocket: Rocket) -> None:
        """Add rocket quantity to self."""

        if isinstance(rocket, Rocket) and rocket.id == self.id and isinstance(rocket.quantity, int) and rocket.quantity >= 0:
            self._set_quantity(self.quantity + rocket.quantity)

    def subtract_rocket(self, rocket: Rocket) -> int:
        """Subtrack rocket quantity from self and return 0.
        
            If difference is negative, set rocket quantity to 0 and return abs(difference).
        """

        if isinstance(rocket, Rocket) and rocket.id == self.id and isinstance(rocket.quantity, int) and rocket.quantity >= 0:
            return self._subtract_value(rocket.quantity)

    @property
    def cost_of_original(self) -> int:
        """Cost in energy of Rockets before they were used."""

        return self._original_value * self.price

    @property
    def cost_of_dead(self) -> int:
        """Cost in energy of used Rockets."""

        return (self._original_value - self._value) * self.price

    @property
    def build_time_of_original(self) -> int:
        """Time in seconds to build (at Turret level 1) Rockets before they were used."""

        return self._original_value * self.build_time

    @property
    def build_time_of_dead(self) -> int:
        """Time in seconds to build (at Turret level 1) used Rockets."""

        return (self._original_value - self._value) * self.build_time

    @property        
    def filtered_str_original(self) -> str:
        """Different short string of self original attributes."""

        return f"{self.original_quantity} of {self.name_en} rockets"

    @property        
    def filtered_str(self) -> str:
        """Different short string of self attributes."""

        return f"{self.quantity}/{self.original_quantity} of {self.name_en} rockets"

    @property
    def filtered_full_str(self) -> str:
        """Full string of self attributes."""

        text = f"Rocket: {self.quantity}/{self.original_quantity} of {self.name_en} with "
        text += f"{self.warheads} warhead(s) of {self.damage} {battlesimulation._GGP.damages[self.damage_type_id]['name_en']} damage"
        return text

    @property
    def filtered_basic_str(self) -> str:
        """String of basic self attributes."""

        if self.valid_targets == (1,3,4,5,6,7,8,9):
            valid_targets_string = "all Spaceships (except Loki)"
        else:
            valid_targets_string = ""
            for id in self.valid_targets:
                valid_targets_string += f"{battlesimulation._GGP.spaceships[id]['name_en']}, "
            valid_targets_string = valid_targets_string[:-2]
        if self.attack_type == 1:
            attack_type_string = "blockade"
        elif self.attack_type == 2:
            attack_type_string = "attack"
        else:
            attack_type_string = "both"
        text = f"{self.warheads} warhead(s) of {self.damage} {battlesimulation._GGP.damages[self.damage_type_id]['name_en']} damage, "
        text += f"targets {valid_targets_string}, attacks against {attack_type_string}."
        return text

    def __repr__(self) -> str:
        """Short string of self attributes."""

        text = f"<Rocket>: {self.quantity}/{self.original_quantity} of {self.name_en}"
        return text

##############################################

class RocketArray(_BasicGameEntityArray):
    """RocketArray with fixed order and the same types of items (Rocket)."""

    def __init__(self) -> None:
        """New instance of RocketArray class."""

        super().__init__(battlesimulation._GGP.types_rocket, Rocket, RocketArray)

    def add_rocket(self, rocket: Rocket) -> None:
        """Add rocket quantity to self."""

        self._add_value(rocket)

    def subtract_rocket(self, rocket: Rocket) -> int:
        """Subtrack rocket quantity from self and return 0.
        
            If difference is negative, set rocket qunantity to 0 and return abs(difference).
        """

        return self._subtract_value(rocket)
    
    def add_rocket_array(self, rocket_array: RocketArray) -> None:
        if isinstance(rocket_array, RocketArray):
            for rocket in rocket_array:
                if isinstance(rocket, Rocket):
                    self.add_rocket(rocket)

    def reset_rockets(self, rocket_array: RocketArray) -> None:
        """Reset self rockets to the values of a given rocket_array."""

        if isinstance(rocket_array, RocketArray):
            self._reset_value(rocket_array)

    def is_populated(self, fleet, target_blockade: bool) -> bool:
        """Returns True if there are rockets left that can strike specific Spaceships in a given type of attack."""

        result = False
        for rocket in self:
            if isinstance(rocket, Rocket):
                if rocket.quantity == 0:
                    continue
                if target_blockade:
                    if rocket.attack_type == 1 or rocket.attack_type == 3:
                        fleet_current = fleet.fleet_current
                        for ss_id in fleet_current:
                            if fleet_current[ss_id]:
                                if ss_id in rocket.valid_targets:
                                    result = True
                else:
                    if rocket.attack_type == 2 or rocket.attack_type == 3:
                        fleet_current = fleet.fleet_current
                        for ss_id in fleet_current:
                            if fleet_current[ss_id]:
                                if ss_id in rocket.valid_targets:
                                    result = True
        return result

    @property
    def rockets_left(self) -> dict:
        """Returns a dict where key is rocket id and value is rocket quantity."""

        result = {}
        for id in battlesimulation._GGP.types_rocket:
            result.update({id:0})
        for rocket in self:
            if isinstance(rocket, Rocket) and rocket.id in result:
                result[rocket.id] = rocket.quantity
        return result

    @property
    def rockets_used(self) -> dict:
        """Returns a dict where key is rocket id and value is rockets used from original_quantity."""

        result = self.rockets_original
        rockets_left = self.rockets_left
        for id in result:
            if id in rockets_left:
                result[id] -= rockets_left[id]
        return result

    @property
    def rockets_original(self) -> dict:
        """Returns a dict where key is rocket id and value is rocket's original quantity."""

        result = {}
        for id in battlesimulation._GGP.types_rocket:
            result.update({id:0})
        for rocket in self:
            if isinstance(rocket, Rocket) and rocket.id in result:
                result[rocket.id] = rocket.original_quantity
        return result

    @property
    def cost_of_original(self) -> int:
        """Cost in energy of all Rockets before they were used."""

        result = 0
        for rocket in self:
            if isinstance(rocket, Rocket):
                result += rocket.cost_of_original
        return result

    @property
    def cost_of_dead(self) -> int:
        """Cost in energy of all used Rockets."""

        result = 0
        for rocket in self:
            if isinstance(rocket, Rocket):
                result += rocket.cost_of_dead
        return result

    @property
    def build_time_of_original(self) -> int:
        """Time in seconds to build (at Turret level 1) all Rockets before they were used."""

        result = 0
        for rocket in self:
            if isinstance(rocket, Rocket):
                result += rocket.build_time_of_original
        return result

    @property
    def build_time_of_dead(self) -> int:
        """Time in seconds to build (at Turret level 1) all used Rockets."""

        result = 0
        for rocket in self:
            if isinstance(rocket, Rocket):
                result += rocket.build_time_of_dead
        return result

    @property
    def filtered_str_original(self) -> str:
        """Different short string of self original attributes."""

        text = "Rockets: ["
        for rocket in self:
            if isinstance(rocket, Rocket) and rocket.original_quantity > 0:
                text += f"{rocket.filtered_str_original}, "
        if text != "Rockets: [":
            text = text[:-2]
        text += "]"
        if text == "Rockets: []":
            text = "Rockets: [empty]"
        return text

    @property
    def filtered_str(self) -> str:
        """Different short string of self attributes."""

        text = "Rockets: ["
        for rocket in self:
            if isinstance(rocket, Rocket) and rocket.quantity > 0:
                text += f"{rocket.filtered_str}, "
        if text != "Rockets: [":
            text = text[:-2]
        text += "]"
        if text == "Rockets: []":
            text = "Rockets: [empty]"
        return text

    def __repr__(self) -> str:
        """Short string of self attributes."""

        text = "<RocketArray>: ["
        for rocket in self:
            text += f"{rocket}, "
        if text != "<RocketArray>: [":
            text = text[:-2]
        text += "]"
        if text == "<RocketArray>: []":
            text = "<RocketArray>: [empty]"
        return text

##############################################