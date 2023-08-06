from __future__ import annotations
from typing import Union
import battlesimulation
from battlesimulation.components.utility import _my_truncate

##############################################

class _BasicGameEntity():
    """Basic Game Entity is a parent class with general attributes and methods for children.
    
        Id is a valid game id, value can represent either damage for Damage class or quantity of spaceships, rockets, buildings, etc.
        For expample, in Damage class self.damage will be a property with get and set methods referring to self._value.
    """

    def _get_id(self) -> int:
        """Id getter."""

        return self._id

    def _set_id(self, id: int) -> None:
        """Id setter."""

        if id in self._valid_ids:
            self._id = id

    def _get_value(self) -> Union[int,float]:
        """Value getter."""

        return self._value

    def _set_value(self, value: Union[int,float]) -> None:
        """Value setter."""

        if self._truncate_decimals is not None and isinstance(value, float):
            value = _my_truncate(value, self._truncate_decimals)
        if (isinstance(value, int) or isinstance(value, float)) and value >= 0:
            self._value = value

    def _get_original_value(self) -> None:
        """original value getter."""

        return self._original_value

    def _set_original_value(self, value: Union[int,float]) -> None:
        """original value setter."""

        if self._truncate_decimals is not None and isinstance(value, float):
            value = _my_truncate(value, self._truncate_decimals)
        if (isinstance(value, int) or isinstance(value, float)) and value >= 0:
            self._original_value = value

    id = property(_get_id, _set_id)
    value = property(_get_value, _set_value)
    original_value = property(_get_original_value, _set_original_value)

    def __init__(self, id: int, value: Union[int,float], valid_ids: tuple, \
            class_reference, truncate_decimals: int = None) -> None:
        """Init Basic Game Entity with specified id, value and valid_ids for id.
        
            valid_ids is a tuple taken from battlesimulation._GGP.types_...
            id is a valid id from valid_ids, value is for example damage value for child class Damage.
            truncate_decimals if set to positive int, will always truncate self.value.
        """

        self._id = 1
        self._value = 0
        self._original_value = 0
        self._valid_ids = valid_ids
        self._class_reference = class_reference
        if isinstance(truncate_decimals, int) and truncate_decimals > 0:
            self._truncate_decimals = truncate_decimals
        else:
            self._truncate_decimals = None
        if id not in self._valid_ids:
            raise ValueError(f"Invalid Id {id}.")
        self._set_id(id)
        self._set_value(value)
        self._set_original_value(value)

    def _reset_value(self, value: Union[int,float], original_value: Union[int,float] = None) -> None:
        """Set self.value with given and set self.original_value with original_value (if specified) or just value."""

        self._set_value(value)
        if original_value is not None:
            self._set_original_value(original_value)
        else:
            self._set_original_value(value)

    def _reset_value_to_original(self) -> None:
        """Reset current value with the original one."""

        self._value = self._original_value

    def _reset_original_value(self) -> None:
        """Reset self.original_value with self.value."""

        self._set_original_value(self.value)

    def _add_value(self, value: Union[int,float]) -> Union[int,float]:
        """Add value to self."""

        if (isinstance(value, int) or isinstance(value, float)) and value >= 0:
            self._set_value(self.value + value)
        return self._value
        
    def _subtract_value(self, value: Union[int,float], default_float: bool = False) -> Union[int,float]:
        """Subtrack value from self and return 0.
        
            If new_value is negative, set value to 0 and return abs(new_value).
            If default_float is specified, return or set values of zero will be either 0.0 or 0.
        """

        new_value = None
        if (isinstance(value, int) or isinstance(value, float)) and value >= 0:
            new_value = self.value - value
        if new_value is not None:
            if new_value < 0:
                if default_float:
                    self._set_value(0.0)
                else:
                    self._set_value(0)
                return abs(new_value)
            self._set_value(new_value)
            if default_float:
                return 0.0
            else:
                return 0
    
    def _multiply_value(self, value: Union[int,float]) -> None:
        """Multiply self.value by a given value."""

        if (isinstance(value, int) or isinstance(value, float)) and value >= 0:
            new_value = self.value * value
            self._set_value(new_value)

    def make_a_copy_of_self(self, copy_original_value: bool = True):
        """Make and return a new self._class_reference instance with the same attributes."""

        new_instance = self._class_reference(self._id, self._value)
        if copy_original_value:
            new_instance._set_original_value(self._original_value)
        return new_instance

    def __repr__(self) -> str:
        """Return short string with self attributes. "/" means current value (left value) of original value."""

        return f"Basic Game Entity: id = {self._id}, value = {self._value}/{self._original_value}"

##############################################

class _BasicGameEntityArray():
    """Basic Array (fixed length) of Game Entities of the same type.

        Instantiating Array creates new corresponding Entities with default attributes.
        It is iterable, have some general methods for children to use.
        It contains Entities inside a dictionary of fixed length and fixed key - value by id Entities.
        Although it's a dict it iterates: for item in list.
    """

    def __init__(self, valid_ids: tuple, class_reference, self_class_reference) -> None:
        """Init Basic Game Entity Array with corresponding Basic Game Entities in it.

            valid_ids is a tuple taken from battlesimulation._GGP.types_... for items in Array.
            class_reference is for Basic Entities, for example Damage class.
            self_class_reference if for self Array Class, for example DamageArray class.
        """

        self._array = {}
        self._valid_ids = valid_ids
        self._class_reference = class_reference
        self._self_class_reference = self_class_reference
        for id in self._valid_ids:
            self._array.update({id:self._class_reference(id)})

    def _reinit(self) -> None:
        """Checks if _array and it's contents are still valid, if not makes it valid; and resets value and original value of items in array to 0."""

        if tuple(self._array.keys()) == self._valid_ids:
            for id in self._array:
                if not isinstance(self._array[id], self._class_reference):
                    self._array[id] == self._class_reference(id)
                elif isinstance(self._array[id], self._class_reference) and self._array[id].id != id:
                    self._array[id] == self._class_reference(id)
                self._array[id]._reset_value(0)
        else:
            self._array.clear()
            for id in self._valid_ids:
                self._array.update({id:self._class_reference(id)})
    
    def set_whole_array(self, data: Union[list,tuple,dict]) -> bool:
        """Resets _array contents with value 0 and then sets them (contents) to the given data. Returns True only if setting all items succeeded.
        
            Passed data can be list or tuple, containing list, tuple or corresponding (to self.class_reference) instance.
            Nested lists or tuples must be of length 2, 0 index is id, 1 index is value.
            Passed data can also be a dict where key is id and value is value or corresponding instance.
            Data may contain not all elements for array. Omitted ones will not change corresponding items in _array.

            For example for DamageArray: data = [(5, 1300), (2, 4000)] will change only two Damage items (2 and 5) in _array to the given values.
        """

        result = True
        semi_result = None
        self._reinit()
        if isinstance(data, list) or isinstance(data, tuple):
            for item in data:
                semi_result = self.set_item_of_array(item)
                # if result == True, then change it to returned bool. If result is already False, don't change it
                if result:
                    result = semi_result
        elif isinstance(data, dict):
            for key in data:
                item = data[key]
                if isinstance(item, self._class_reference):
                    semi_result = self.set_item_of_array(item)
                    # if result == True, then change it to returned bool. If result is already False, don't change it
                    if result:
                        result = semi_result
                elif (isinstance(item, int) or isinstance(item, float)) and len(item) > 0:
                    semi_result = self.set_item_of_array((key, item))
                    # if result == True, then change it to returned bool. If result is already False, don't change it
                    if result:
                        result = semi_result
        # if there were no inner semi_results, then change result to False
        if semi_result is None:
            result = False
        return result

    def set_item_of_array(self, item: Union[list,tuple,dict]) -> bool:
        """Without reseting whole Array, sets corresponding item to the given data. Returns True if successful.

            Passed data can be list or a tuple, must be of length 2, 0 index is id, 1 index is value.
            Passed data can also be a dict of length 1 where key is id and value is value.
            Or just an instance of corresponding (to self.class_reference) instance.

            For example for DamageArray: data = (5, 1300) will change item's 5 value to 1300.
        """

        result = False
        if isinstance(item, self._class_reference) and item.id in self._array and \
                isinstance(self._array[item.id], self._class_reference) and self._array[item.id].id == item.id:
            self._array[item.id]._reset_value(item.value)
            result = True
        elif (isinstance(item, list) or isinstance(item, tuple)) and len(item) == 2:
            id, value = item
            if id in self._array and isinstance(self._array[id], self._class_reference) and self._array[id].id == id:
                self._array[id]._reset_value(value)
                result = True
        elif isinstance(item, dict) and len(item) == 1:
            for id in item:
                value = item[id]
                if id in self._array and isinstance(self._array[id], self._class_reference) and self._array[id].id == id:
                    self._array[id]._reset_value(value)
                    result = True
        return result

    def _get_item_of_array_by_id(self, id: int):
        """Returns item from self with the corresponding id."""

        if id in self._array:
            return self._array[id]

    def _add_value(self, instance) -> None:
        """Pass correct instance and add it's value to corresponding self item's value."""

        if isinstance(instance, self._class_reference):
            if instance.id in self._array and isinstance(self._array[instance.id], self._class_reference) and \
                    self._array[instance.id].id == instance.id:
                self._array[instance.id]._add_value(instance.value)

    def _subtract_value(self, instance, default_float: bool = False) -> Union[int,float]:
        """Pass correct instance and subtract it's value from corresponding self item's value.
        
            default_float is used to pass it to those items that can have float values (Damage for example).
            Returns 0 or 0.0 if the difference is >= 0 and returns abs(of difference) if otherwise.
        """

        if isinstance(instance, self._class_reference):
            if instance.id in self._array and isinstance(self._array[instance.id], self._class_reference) and \
                    self._array[instance.id].id == instance.id:
                return self._array[instance.id]._subtract_value(instance.value, default_float)

    def _multiply_value(self, instance) -> None:
        """Pass correct instance and multiply it's value to corresponding self item's value."""

        if isinstance(instance, self._class_reference):
            if instance.id in self._array and isinstance(self._array[instance.id], self._class_reference) and \
                    self._array[instance.id].id == instance.id:
                self._array[instance.id]._multiply_value(instance.value)

    def _reset_value(self, items_array) -> None:
        """Reset self item values to the given values of items in the same Array Class instance."""

        if isinstance(items_array, self._self_class_reference):
            for item in items_array:
                if isinstance(item, self._class_reference):
                    id = item.id
                    if id in self._array and isinstance(self._array[id], self._class_reference) and \
                            self._array[id].id == id:
                        self._array[id]._reset_value(item.value, item.original_value)

    def reset_values_to_original(self) -> None:
        """Reset all current values to original values of all items of Array."""

        for item in self:
            if isinstance(item, self._class_reference):
                item._reset_value_to_original()

    def reset_original_values(self) -> None:
        """Reset all original values to current values of all items of Array."""

        for item in self:
            if isinstance(item, self._class_reference):
                item._reset_original_value()

    def set_to_zero(self) -> None:
        """Reset all items values to zero without changing original values."""

        for item in self:
            if isinstance(item, self._class_reference):
                item._set_value(0)

    def make_a_copy_of_self(self, copy_original_value: bool = True):
        """Returns new self._self_class_reference Array instance with the same items (being a new instance each) in Array.
        
            DO NOT call this on _BasicGameEntityArray.
        """

        new_instance = self._self_class_reference()
        for item in self:
            if isinstance(item, self._class_reference):
                new_instance.set_item_of_array(item)
        if copy_original_value:
            for item in new_instance:
                item._set_original_value(self._array[item.id]._original_value)
        return new_instance

    def __iter__(self) -> iter:
        """Iterates over self._array[key] via iter()."""

        return iter(self._array.values())

    def __len__(self) -> int:
        """Returns length of self._array."""

        return len(self._array)

    @property
    def filtered_str(self) -> str:
        """Makes a string of items in Array which value is above zero."""

        text = "["
        for item in self:
            if isinstance(item, self._class_reference) and item.value > 0:
                text += f"{item}, "
        if len(text) > 2:
            text = text[:-2]
        text += "]"
        if text == "[]":
            text = "[empty]"
        return text

    def __repr__(self) -> str:
        """Makes a string of items in Array regardless of value."""

        text = "["
        for item in self:
            text += f"{item}, "
        if len(text) > 2:
            text = text[:-2]
            text += "]"
        else:
            text = ""
        return text

##############################################