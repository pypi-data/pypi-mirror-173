from __future__ import annotations
from typing import Union
import battlesimulation
from battlesimulation import debug_print, _BasicGameEntity, _BasicGameEntityArray

##############################################

class Building(_BasicGameEntity):
    """Building class representing building from game.

        Level cannot be above maximum in Game (30 level) unless _debug_limit_variables is disabled for testing.
    """

    def _get_level(self) -> int:
        return self._value

    def _set_level(self, value: int) -> None:
        if isinstance(value, int) and value >= 0:
            if battlesimulation._debug_limit_variables and value <= self.max_level:
                self._value = value
            else:
                self._value = value

    def _get_original_level(self) -> int:
        return self._original_value

    def _set_original_level(self, value: int) -> None:
        if isinstance(value, int) and value >= 0:
            if battlesimulation._debug_limit_variables and value <= self.max_level:
                self._original_value = value
            else:
                self._value = value

    level = property(_get_level, _set_level)
    original_level = property(_get_original_level, _set_original_level)

    def __init__(self, id: int, level: int = 1) -> None:
        """New instance of Building class.

            Default ids: 1 - Command Center, 2 - Mine, 3 - Warehouse, 4 - Trade Office, 5 - Cosmodrome,
            6 - Spacecraft Plant, 7 - Power Plant, 8 - Detection Station, 9 - Missile Turret, 10 - Shield Generator.
        """

        if not isinstance(level, int):
            raise ValueError("Level of building is not int")
        if isinstance(level, int) and level < 0:
            level = 1
        super().__init__(id, level, battlesimulation._GGP.types_building, Building, None)

        self.name = battlesimulation._GGP.buildings[id]["name"]
        self.name_en = battlesimulation._GGP.buildings[id]["name_en"]
        self.defense = battlesimulation._GGP.buildings[id]["defense"]
        self.max_level = battlesimulation._GGP.buildings[id]["max_building_level"]

    def reset_level(self, level: int, original_level: int) -> None:
        """Set self.level with given and set self.original_level with original_level (if specified) or just level."""

        if isinstance(level, int) and level >= 0 and \
                ((isinstance(original_level, int) and original_level >= 0) or original_level is None):
            self._reset_value(level, original_level)

    def reset_original_level(self) -> None:
        """Reset self.original_level with self.level."""

        self._reset_original_value()

    def _add_value(self, *args, **kwargs) -> None:
        return

    def _subtract_value(self, *args, **kwargs) -> None:
        return

    def _multiply_value(self, *args, **kwargs) -> None:
        return

    @property
    def filtered_str_original(self) -> str:
        """Different short string of self original attributes."""

        return f"{self.name_en} of level {self.original_level}"

    @property
    def filtered_str(self) -> str:
        """Different short string of self attributes."""

        return f"{self.name_en} of level {self.level}/{self.original_level}"

    def __repr__(self) -> str:
        """Short string of self attributes."""

        return f"<Building>: {self.name_en} of level {self.level}/{self.original_level}"

##############################################

class BuildingArray(_BasicGameEntityArray):
    """BuildingArray with Buildings as elements.

        Heavy on redefining parent's methods and some logic.
        With fixed max length (25 buildings on the Planet, unless _debug_limit_variables is disabled for testing) and empty when instantiated.
    """

    def __init__(self) -> None:
        """New instance of BuildingArray class with empty contents."""

        super().__init__(battlesimulation._GGP.types_building, Building, BuildingArray)
        self._reinit()

    def _reinit(self) -> None:
        """Clears itself of all buildings."""

        self._array.clear()

    def count_number_of_buildings(self, building_id: int) -> int:
        """Counts and returns number of buildings of specified Id."""

        counter = 0
        for building in self:
            if isinstance(building, Building):
                if building.id == building_id:
                    counter += 1
        return counter

    def get_available_primary_key(self, first_call_of_recurse_primary_key: int = 1) -> int:
        """Finds first available primary key in self._array."""

        primary_key = first_call_of_recurse_primary_key
        for key in self._array:
            if key == primary_key:
                primary_key += 1

        if primary_key in self._array:
            primary_key = self.get_available_primary_key(primary_key)

        return primary_key

    def set_whole_array(self, data: Union[list,tuple]) -> bool:
        """Clears all buildings in self and sets contents to given data. Returns True only if setting all buildings succeeded.

            Passed data can be list or tuple, containing list, tuple or Building instance.
            Nested lists or tuples must be of length 2, 0 index is id, 1 index is level.

            Checks and limits number of buildings to Game limits, unless _debug_limit_variables is disabled for testing.
            Each building limits self level to Game limit (level 30), if passed level is above 30, default level 1 will be used.

            Default ids: 1 - Command Center, 2 - Mine, 3 - Warehouse, 4 - Trade Office, 5 - Cosmodrome,
            6 - Spacecraft Plant, 7 - Power Plant, 8 - Detection Station, 9 - Missile Turret, 10 - Shield Generator.

            For example: data = [(1, 15), (2, 15), (2, 14), (2, 14), (10, 12)] will add the following buildings:
            Command Center lvl 15, Three Mines of levels 14, 14 and 15 and a Shield Generator of lvl 12.

            After that if no Command Center and at least 3 mines were added (unless _debug_limit_variables is disabled for testing)
            the missing buildings will be added anyway.
        """

        result = True
        primary_key = 1
        # if _debug_limit_variables is enabled, we need to search for basic minumal buildings first
        # and then add them to self
        # None or False is purely for identifing _debug_limit_variables
        if battlesimulation._debug_limit_variables:
            command_center = None
            mine_1 = None
            mine_2 = None
            mine_3 = None
        else:
            command_center = False
            mine_1 = False
            mine_2 = False
            mine_3 = False

        self._reinit()

        if isinstance(data, list) or isinstance(data, tuple):
            new_data = []
            for item in data:
                if (isinstance(item, list) or isinstance(item, tuple)) and len(item) == 2:
                    if item[0] == 1 and command_center is None:
                        command_center = item
                    elif item[0] == 2 and mine_1 is None:
                        mine_1 = item
                    elif item[0] == 2 and mine_2 is None:
                        mine_2 = item
                    elif item[0] == 2 and mine_3 is None:
                        mine_3 = item
                    else:
                        if isinstance(item, list):
                            new_data.append(item.copy())
                        else:
                            new_data.append(item)
                elif isinstance(item, Building):
                    if item.id == 1 and command_center is None:
                        command_center = item
                    elif item.id == 2 and mine_1 is None:
                        mine_1 = item
                    elif item.id == 2 and mine_2 is None:
                        mine_2 = item
                    elif item.id == 2 and mine_3 is None:
                        mine_3 = item
                    else:
                        new_data.append(item)
        
        # if they are not found we make them default level 1
        if battlesimulation._debug_limit_variables:
            if command_center is None:
                command_center = (1,1)
            if mine_1 is None:
                mine_1 = (2,0)
            if mine_2 is None:
                mine_2 = (2,0)
            if mine_3 is None:
                mine_3 = (2,0)
            # and add them to self
            # if result == True, then change it to returned bool. If result is already False, don't change it
            semi_result = self.set_item_of_array(command_center, 1)
            if result:
                result = semi_result
            semi_result = self.set_item_of_array(mine_1, 2)
            if result:
                result = semi_result
            semi_result = self.set_item_of_array(mine_2, 3)
            if result:
                result = semi_result
            semi_result = self.set_item_of_array(mine_3, 4)
            if result:
                result = semi_result
            primary_key = 5

        # in new_data there are no buildings that we caught and added to self just now
        data = new_data
        # then we iterate over the rest of data and add it to self
        if isinstance(data, list) or isinstance(data, tuple):
            for item in data:
                if ((isinstance(item, list) or isinstance(item, tuple)) and len(item) == 2) or isinstance(item, Building):
                    semi_result = self.set_item_of_array(item, primary_key)
                    primary_key += 1
                    # if result == True, then change it to returned bool. If result is already False, don't change it
                    if result:
                        result = semi_result
        return result

    def set_item_of_array(self, item: Union[list,tuple,dict,Building], primary_key: int = None) -> bool:
        """Without reseting whole BuildingArray, sets corresponding building to the given data. Returns True if successful.

            Passing primary_key is not needed, it's for internal use.
            Passed data can be list or a tuple, must be of length 2, 0 index is id, 1 index is level.
            Passed data can also be a dict of length 1 where key is id and value is level.
            Or just a Building instance.

            Default ids: 1 - Command Center, 2 - Mine, 3 - Warehouse, 4 - Trade Office, 5 - Cosmodrome,
            6 - Spacecraft Plant, 7 - Power Plant, 8 - Detection Station, 9 - Missile Turret, 10 - Shield Generator.
        """

        if primary_key is None:
            primary_key = self.get_available_primary_key()

        result = False
        building = None
        if isinstance(item, Building):
            building = item
        elif (isinstance(item, list) or isinstance(item, tuple)) and len(item) == 2:
            building = Building(*item)
        elif isinstance(item, dict) and len(item) == 1:
            for id in item:
                if isinstance(item[id], Building):
                    building = item[id]
                else:
                    building = Building(id, item[id])

        if building is not None:
            if battlesimulation._debug_limit_variables:
                # we limit buildings on the Planet with the following ways:
                # 1. Building level cannot be above 30, it was already checked when building was instantiated.
                # 2. Number of certain buildings don't go over their max quantity.
                # 3. Maximum number of buildings on the Planet is 25.
                # 4. On each Planet there is always one Command Center and at least three mines.
                # N.B. in game Building cannot be upgraded to higher level than the level of Command Center
                #      however, there are ways for buildings to exist with higher levels than of CC,
                #      so we don't limit it here.
                #
                # 2.
                number_of_buildings = self.count_number_of_buildings(building.id)
                maximum_number = battlesimulation._GGP.buildings[building.id]["max_buildings"]
                if number_of_buildings + 1 > maximum_number:
                    return result
                # 3.
                total_buildings = len(self._array)
                if total_buildings >= 25:
                    return result
                # 4.
                free_space = 25 - total_buildings
                min_free_space_needed_for_mines = 3
                # subtract Mines that are already in self
                min_free_space_needed_for_mines -= self.count_number_of_buildings(2)
                # if there are more than 3 Mines already we set min_free_space_needed_for_mines to zero
                if min_free_space_needed_for_mines < 0:
                    min_free_space_needed_for_mines = 0
                min_free_space_needed_for_CC = 1
                # subtract CC if there is one already
                min_free_space_needed_for_CC -= self.count_number_of_buildings(1)
                # subtract from free_space we have that what we need
                free_space -= (min_free_space_needed_for_CC + min_free_space_needed_for_mines)
                # if the passed building is one of CC or Mine then we don't need to reserve space for it
                if building.id in (1,2):
                    free_space += 1
                # after that, if free_space is above zero, we add the building to self
                if free_space > 0:
                    self._array.update({primary_key: building.make_a_copy_of_self()})
                    result = True
            else:
                self._array.update({primary_key: building.make_a_copy_of_self()})
                result = True
        return result

    def _get_item_of_array_by_id(self, *args, **kwargs) -> None:
        return

    def _add_value(self, *args, **kwargs) -> None:
        return

    def _subtract_value(self, *args, **kwargs) -> None:
        return

    def _multiply_value(self, *args, **kwargs) -> None:
        return

    def _reset_value(self, *args, **kwargs) -> None:
        return

    def _total_defense_up_to_level(self, level_cap: int) -> int:
        """Returns sum of defenses of all buildings capped at specified level."""

        total_defense = 0
        for building in self:
            if isinstance(building, Building):
                level = level_cap if building.level > level_cap else building.level
                total_defense += level * building.defense
        return total_defense

    def reset_original_values(self, *args, **kwargs) -> None:
        return

    def set_to_zero(self, *args, **kwargs) -> None:
        return

    def make_a_copy_of_self(self, copy_original_value: bool = True) -> BuildingArray:
        new_instance = BuildingArray()
        for key in self._array:
            new_instance._array.update({key: Building(self._array[key]._id, self._array[key]._value)})
            if copy_original_value:
                new_instance._array[key].reset_level(self._array[key]._value, self._array[key]._original_value)
        return new_instance

    @property
    def total_turrets_level(self) -> int:
        """Returns sum of levels of all Turrets."""

        total_level = 0
        for building in self:
            if isinstance(building, Building) and building.id == 9:
                total_level += building.level
        return total_level

    @property
    def filtered_str_original(self) -> str:
        """Different short string of self original attributes."""

        text = "Buildings: ["
        for building in self:
            if isinstance(building, Building):
                text += f"{building.filtered_str_original}, "
        if text != "Buildings: [":
            text = text[:-2]
        text += "]"
        if text == "Buildings: []":
            text = "Buildings: [empty]"
        return text

    @property
    def filtered_str(self) -> str:
        """Different short string of self attributes."""

        text = "Buildings: ["
        for building in self:
            if isinstance(building, Building):
                text += f"{building.filtered_str}, "
        if text != "Buildings: [":
            text = text[:-2]
        text += "]"
        if text == "Buildings: []":
            text = "Buildings: [empty]"
        return text

    @property
    def filtered_pretty_str(self) -> str:
        """Pretty string of self attributes."""

        spacing = 0
        text = "Buildings:\n"
        buildings_meta_data = {}
        for building in self:
            if isinstance(building, Building):
                if building.id not in buildings_meta_data:
                    buildings_meta_data.update({building.id: []})
                buildings_meta_data[building.id].append(building.level)
        if len(buildings_meta_data) == 0:
            text = "Buildings: [empty]"
        else:
            for id in buildings_meta_data:
                new_spacing = len(buildings_meta_data[id]) * 4 - 2
                if new_spacing > spacing:
                    spacing = new_spacing
            spacing += 20
            for id in buildings_meta_data:
                name_en = battlesimulation._GGP.buildings[id]['name_en']
                level_string = ""
                for level in buildings_meta_data[id]:
                    level_string += f"{level}, "
                level_string = level_string[:-2]
                spacing_shift = spacing - len(name_en) - len(level_string)
                string = f"{name_en}:" + " " * spacing_shift + f"{level_string} | {len(buildings_meta_data[id])}"
                text += f"{string}\n"
            text += f"Total buildings: {len(self)}"
        return text

    @property
    def filtered_pretty_str_original(self) -> str:
        """Pretty string of self original attributes."""

        spacing = 0
        text = "Buildings:\n"
        buildings_meta_data = {}
        for building in self:
            if isinstance(building, Building):
                if building.id not in buildings_meta_data:
                    buildings_meta_data.update({building.id: []})
                buildings_meta_data[building.id].append(building.original_level)
        if len(buildings_meta_data) == 0:
            text = "Buildings: [empty]"
        else:
            for id in buildings_meta_data:
                new_spacing = len(buildings_meta_data[id]) * 4 - 2
                if new_spacing > spacing:
                    spacing = new_spacing
            spacing += 20
            for id in buildings_meta_data:
                name_en = battlesimulation._GGP.buildings[id]['name_en']
                level_string = ""
                for level in buildings_meta_data[id]:
                    level_string += f"{level}, "
                level_string = level_string[:-2]
                spacing_shift = spacing - len(name_en) - len(level_string)
                string = f"{name_en}:" + " " * spacing_shift + f"{level_string} | {len(buildings_meta_data[id])}"
                text += f"{string}\n"
            text += f"Total buildings: {len(self)}"
        return text

    def __repr__(self) -> str:
        """Short string of self attributes."""

        text = "<BuildingArray>: ["
        for building in self:
            if isinstance(building, Building):
                text += f"{building}, "
        if text != "<BuildingArray>: [":
            text = text[:-2]
        text += "]"
        if text == "<BuildingArray>: []":
            text = "<BuildingArray>: [empty]"
        return text

##############################################