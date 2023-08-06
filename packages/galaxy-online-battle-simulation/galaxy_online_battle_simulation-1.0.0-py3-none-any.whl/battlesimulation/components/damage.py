from __future__ import annotations
from typing import Union
import battlesimulation
from battlesimulation.components.utility import _my_truncate
from battlesimulation import _BasicGameEntity, _BasicGameEntityArray

class Damage(_BasicGameEntity):
    """Damage class with specific damage type id and damage value."""

    def _get_damage_type_id(self) -> int:
        return self._id

    def _set_damage_type_id(self, damage_type_id: int) -> None:
        self._set_id(damage_type_id)
    
    def _get_damage(self) -> float:
        return self._value
    
    def _set_damage(self, damage: Union[int,float]) -> None:
        if isinstance(damage, int):
            damage = float(damage)
        if isinstance(damage, float) and damage >= 0:
            damage = _my_truncate(damage, 1)
            self._set_value(damage)
    
    def _get_original_damage(self):
        return self._original_value
    
    def _set_original_damage(self, damage):
        if isinstance(damage, int):
            damage = float(damage)
        if isinstance(damage, float) and damage >= 0:
            damage = _my_truncate(damage, 1)
            self._set_original_value(damage)

    damage_type_id = property(_get_damage_type_id, _set_damage_type_id)
    damage = property(_get_damage, _set_damage)
    original_damage = property(_get_original_damage, _set_original_damage)

    def __init__(self, id: int, damage: Union[int,float] = 0.0) -> None:
        """New instance of Damage class.

            Default ids: 1 - Plasma, 2 - Laser, 3 - Kinetic, 4 - Rocket, 5 - Rail.
        """

        if isinstance(damage, int):
            damage = float(damage)
        if isinstance(damage, float) and damage >= 0:
            damage = _my_truncate(damage, 1)

        super().__init__(id, damage, battlesimulation._GGP.types_damage, \
            Damage, 1)

        self.name = battlesimulation._GGP.damages[id]["name"]
        self.name_en = battlesimulation._GGP.damages[id]["name_en"]
    
    def add_damage(self, damage: Damage) -> None:
        """Add damage value to self."""

        if isinstance(damage, Damage) and damage.id == self.id:
            self._add_value(damage.value)

    def subtract_damage(self, damage: Damage) -> float:
        """Subtrack damage value from self and return 0.0.
        
            If difference is negative, set damage to 0.0 and return abs(difference).
        """

        if isinstance(damage, Damage) and damage.id == self.id:
            return self._subtract_value(damage.value, default_float=True)

    def reset_damage(self, damage: Union[int,float], original_damage: Union[int,float] = None) -> None:
        """Set self.damage with given and set self.original_damage with original_damage (if specified) or just damage."""

        self._reset_value(damage, original_damage)

    def reset_original_damage(self):
        """Reset self.original_damage with self.damage."""

        self._reset_original_value()

    def discard_low_damage(self) -> None:
        """Set self.damage to 0.0 if it was below 1."""

        if self.value < 1:
            self._set_value(0.0)

    @property
    def filtered_str(self) -> str:
        """Different short string of self attributes."""

        return f"{self.damage}/{self.original_damage} of {self.name_en} damage"

    def __repr__(self) -> str:
        """Short string of self attributes."""

        return f"<Damage>: {self.damage}/{self.original_damage} of {self.name_en}"

##############################################

class DamageArray(_BasicGameEntityArray):
    """DamageArray with fixed order and the same types of items (Damage)."""

    def __init__(self) -> None:
        """New instance of DamageArray class."""

        super().__init__(battlesimulation._GGP.types_damage, Damage, DamageArray)

    def get_damage(self, id: int) -> Damage:
        """Returns reference to corresponding Damage instance contained in self."""

        return self._get_item_of_array_by_id(id)

    def add_damage(self, damage: Damage) -> None:
        """Add damage value to self."""

        self._add_value(damage)

    def subtract_damage(self, damage: Damage) -> float:
        """Subtrack damage value from self and return 0.0.
        
            If difference is negative, set damage to 0.0 and return abs(difference).
        """

        return self._subtract_value(damage, default_float=True)

    def reset_damage(self, damage_array: DamageArray):
        """Reset self damages to the values of a given damage_array."""

        if isinstance(damage_array, DamageArray):
            self._reset_value(damage_array)

    @property
    def is_populated(self) -> bool:
        result = False
        for damage in self:
            if isinstance(damage, Damage) and damage.damage > 0:
                result = True
                break
        return result

    @property
    def filtered_str(self) -> str:
        """Different short string of self attributes."""

        text = "Damages: ["
        for damage in self:
            if isinstance(damage, Damage) and damage.damage > 0:
                text += f"{damage.filtered_str}, "
        if text != "Damages: [":
            text = text[:-2]
        text += "]"
        if text == "Damages: []":
            text = "Damages: [empty]"
        return text

    def __repr__(self) -> str:
        """Short string of self attributes."""

        text = "<DamageArray>: ["
        for damage in self:
            text += f"{damage}, "
        if text != "<DamageArray>: [":
            text = text[:-2]
        text += "]"
        if text == "<DamageArray>: []":
            text = "<DamageArray>: [empty]"
        return text

##############################################