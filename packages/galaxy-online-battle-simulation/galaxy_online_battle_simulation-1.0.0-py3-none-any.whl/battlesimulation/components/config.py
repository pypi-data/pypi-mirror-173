from __future__ import annotations
from genericpath import isfile
import os
import json
from turtle import update
import battlesimulation

# Built-in data of game

##############################################

_data = {
    "Types": {
        "Damage": (1,2,3,4,5),                        # ids
        "Spaceship": (1,2,3,4,5,6,7,8,9),             # ids
        "Rocket": (1,2,3,4),                          # ids
        "Planet_type": (1,2,3,4,5,6,7,9,12,15),       # 1:7 - ordinary planets, 9,12,15(?) Space Stations [Resource, Production, Trade]
        "Planet_size": (0,1,2),                       # Mines: 0 -> 3 mines, 1 -> 4 mines, 2 -> 5 mines
        "Attack_type": (1,2,3),                       # for rockets: 1 - blockade, 2 - attack, 3 - both
        "Building": (1,2,3,4,5,6,7,8,9,10),           # ids
        "Module": (1,2,3,4,5,6,7,8,9,10),
        "Valid_targets" : (1,3,4,5,6,7,8,9)              # default valid targets for rockets, that have no valid targets specified
    },                                                  # Loki spaceships are not targeted by rockets at all
    "Spaceships": {
        1: {
            "id": 1,
            "name": "Геркулес",
            "name_en": "Hercules",
            "damage_type_id": 2,
            "attack": 25,
            "defense": 275,
            "defenses": { 1: 330, 2: 275, 3: 220, 4: 248, 5: 303 },
            "weight": 10,
            "attack_priority": 250,
            "defense_priority": 250,
            "speed": 5,
            "calc_speed": 2.56,
            "price": 500,
            "build_time": 300,
            "cargohold": 100,
            "radar": 0,
            "accuracy": 80
        },
        2: {
            "id": 2,
            "name": "Локи",
            "name_en": "Loki",
            "damage_type_id": 3,
            "attack": 20,
            "defense": 20,
            "defenses": { 1: 22, 2: 24, 3: 20, 4: 16, 5: 18 },
            "weight": 1,
            "attack_priority": 250,
            "defense_priority": 100,
            "speed": 10,
            "calc_speed": 5.12,
            "price": 300,
            "build_time": 120,
            "cargohold": 0,
            "radar": 25,
            "accuracy": 80
        },
        3: {
            "id": 3,
            "name": "Раптор",
            "name_en": "Raptor",
            "damage_type_id": 3,
            "attack": 150,
            "defense": 150,
            "defenses": { 1: 180, 2: 210, 3: 150, 4: 90, 5: 120 },
            "weight": 6,
            "attack_priority": 1000,
            "defense_priority": 3000,
            "speed": 6,
            "calc_speed": 3.072,
            "price": 1500,
            "build_time": 720,
            "cargohold": 20,
            "radar": 0,
            "accuracy": 80
        },
        4: {
            "id": 4,
            "name": "Хорнет",
            "name_en": "Hornet",
            "damage_type_id": 2,
            "attack": 110,
            "defense": 90,
            "defenses": { 1: 126, 2: 90, 3: 54, 4: 72, 5: 108 },
            "weight": 4,
            "attack_priority": 1000,
            "defense_priority": 3000,
            "speed": 7,
            "calc_speed": 3.584,
            "price": 1000,
            "build_time": 528,
            "cargohold": 10,
            "radar": 0,
            "accuracy": 80
        },
        5: {
            "id": 5,
            "name": "Джавелин",
            "name_en": "Javelin",
            "damage_type_id": 1,
            "attack": 45,
            "defense": 55,
            "defenses": { 1: 55, 2: 33, 3: 44, 4: 66, 5: 77 },
            "weight": 2,
            "attack_priority": 1000,
            "defense_priority": 3000,
            "speed": 8,
            "calc_speed": 4.096,
            "price": 500,
            "build_time": 264,
            "cargohold": 20,
            "radar": 0,
            "accuracy": 80
        },
        6: {
            "id": 6,
            "name": "Экскалибр",
            "name_en": "Excalibur",
            "damage_type_id": 4,
            "attack": 225,
            "defense": 275,
            "defenses": { 1: 220, 2: 330, 3: 385, 4: 275, 5: 165 },
            "weight": 10,
            "attack_priority": 1000,
            "defense_priority": 3000,
            "speed": 5,
            "calc_speed": 2.56,
            "price": 2750,
            "build_time": 1200,
            "cargohold": 10,
            "radar": 0,
            "accuracy": 80
        },
        7: {
            "id": 7,
            "name": "Валькирия",
            "name_en": "Valkyrie",
            "damage_type_id": 4,
            "attack": 50,
            "defense": 100,
            "defenses": { 1: 90, 2: 110, 3: 120, 4: 100, 5: 80 },
            "weight": 8,
            "attack_priority": 5000,
            "defense_priority": 250,
            "speed": 3,
            "calc_speed": 1.536,
            "price": 5000,
            "build_time": 2400,
            "cargohold": 10,
            "radar": 0,
            "accuracy": 80
        },
        8: {
            "id": 8,
            "name": "Титан",
            "name_en": "Titan",
            "damage_type_id": 5,
            "attack": 100,
            "defense": 900,
            "defenses": { 1: 720, 2: 810, 3: 990, 4: 1080, 5: 900 },
            "weight": 100,
            "attack_priority": 100,
            "defense_priority": 100,
            "speed": 3,
            "calc_speed": 1.536,
            "price": 32000,
            "build_time": 5400,
            "cargohold": 10,
            "radar": 0,
            "accuracy": 80
        },
        9: {
            "id": 9,
            "name": "Абаддон",
            "name_en": "Abaddon",
            "damage_type_id": 5,
            "attack": 440,
            "defense": 360,
            "defenses": { 1: 216, 2: 288, 3: 432, 4: 504, 5: 360 },
            "weight": 16,
            "attack_priority": 1000,
            "defense_priority": 3000,
            "speed": 4,
            "calc_speed": 2.048,
            "price": 4400,
            "build_time": 1800,
            "cargohold": 0,
            "radar": 0,
            "accuracy": 80
        }
    },
    "Damages": {
        1: { "id": 1, "name": "Плазма", "name_en": "Plasma" },
        2: { "id": 2, "name": "Лазер", "name_en": "Laser" },
        3: { "id": 3, "name": "Кинетика", "name_en": "Kinetic" },
        4: { "id": 4, "name": "Ракета", "name_en": "Rocket" },
        5: { "id": 5, "name": "Рельса", "name_en": "Rail" }
    },
    "Planetary_coefs": {                                        # keys are "planet_id"+"planet_size"
        "10": 0.80, "11": 1.00, "12": 1.20,                     # Type 5 planet with 4 mines (planet_size=1)
        "20": 1.00, "21": 1.25, "22": 1.50,                     # key is "51" and value is 2.00
        "30": 1.20, "31": 1.50, "32": 1.80,
        "40": 1.40, "41": 1.75, "42": 2.10,
        "50": 1.60, "51": 2.00, "52": 2.40,
        "60": 2.00, "61": 2.50, "62": 3.00,
        "70": 2.40, "71": 3.00, "72": 3.60,
        "90": 3.00, "91": 3.00, "92": 3.00,
        "120": 3.00, "121": 3.00, "122": 3.00,
        "150": 3.00, "151": 3.00, "152": 3.00
    },
    "Rockets": {
        1: {"id":1,"name":"Sticks-XL","name_en":"Sticks-XL","warheads":1,"damage":50,"price":100,"build_time":45,"damage_type_id":4,"attack_type":1},
        2: {"id":2,"name":"Кобра-М1","name_en":"Cobra-M1","warheads":1,"damage":150,"price":250,"build_time":90,"damage_type_id":4,"attack_type":2},
        3: {"id":3,"name":"Аврора","name_en":"Aurora","warheads":4,"damage":75,"price":600,"build_time":180,"damage_type_id":4,"attack_type":3},
        4: {"id":4,"name":"X-Ray","name_en":"X-Ray","warheads":1,"damage":100,"price":3000,"build_time":300,"damage_type_id":4,"attack_type":2,"valid_targets":(7,)}
    },
    "Buildings": {
        1: {"id":1,"name":"Командный центр","name_en":"Command Center","defense":700,"max_buildings":1},
        2: {"id":2,"name":"Шахта","name_en":"Mine","defense":500,"max_buildings":5},
        3: {"id":3,"name":"Склад","name_en":"Warehouse","defense":250,"max_buildings":21},
        4: {"id":4,"name":"Торговый центр","name_en":"Trade Office","defense":400,"max_buildings":1},
        5: {"id":5,"name":"Космопорт","name_en":"Cosmodrome","defense":450,"max_buildings":9},
        6: {"id":6,"name":"Завод космолётов","name_en":"Spacecraft Plant","defense":550,"max_buildings":5},
        7: {"id":7,"name":"Энергостанция","name_en":"Power Plant","defense":300,"max_buildings":1},
        8: {"id":8,"name":"Станция обнаружения","name_en":"Detection Station","defense":350,"max_buildings":1},
        9: {"id":9,"name":"Ракетная башня","name_en":"Missile Turret","defense":650,"max_buildings":20},
        10: {"id":10,"name":"Генератор щита","name_en":"Shield Generator","defense":750,"max_buildings":1}
    },
    "Modules": {
        1: {"id":1,"name":"Дезинтегратор","name_en":"Disintegrator","attack":25,"defense":0,"speed":0,"price":10000,"solarium":1,"build_time":129},
        2: {"id":2,"name":"Форсажный Блок","name_en":"Afterburner","attack":0,"defense":0,"speed":50,"price":7000,"solarium":1,"build_time":90},
        3: {"id":3,"name":"Усилитель Щита","name_en":"Shield Booster","attack":0,"defense":30,"speed":0,"price":13000,"solarium":1,"build_time":168},
        4: {"id":4,"name":"Комплекс Бастион","name_en":"Complex Bastion","attack":20,"defense":25,"speed":0,"price":23000,"solarium":1,"build_time":298},
        5: {"id":5,"name":"Комплекс Луч","name_en":"Complex Luch","attack":20,"defense":0,"speed":50,"price":17000,"solarium":1,"build_time":220},
        6: {"id":6,"name":"Комплекс Ореол","name_en":"Complex Halo","attack":0,"defense":25,"speed":50,"price":20000,"solarium":1,"build_time":259},
        7: {"id":7,"name":"Комплекс Страж","name_en":"Complex Guardian","attack":15,"defense":20,"speed":40,"price":30000,"solarium":1,"build_time":388},
        8: {"id":8,"name":"Спутник Соляриум","name_en":"Satellite Solarium","attack":0,"defense":0,"speed":0,"price":12000,"solarium":0,"build_time":155},
        9: {"id":9,"name":"Спутник Энергия","name_en":"Satellite Energy","attack":0,"defense":0,"speed":0,"price":10000,"solarium":0,"build_time":129},
        10: {"id":10,"name":"Комплекс Абордаж","name_en":"Complex Boarding","attack":0,"defense":0,"speed":0,"price":5000,"solarium":1,"build_time":64}
    },
    "Globals": {
        "turret_damage": 100,
        "turret_damage_type_id": 5,
        "shield_damage_type_id": 2,
        "shield_max_coef": 0.5,
        "thold_per": 0.125,
        "thold_max": 1.5,
        "thold_max_bonus": 50,
        "threshold": 0.5,
        "accuracy": 80,
        "max_speed_bonus": 2.0,
        "max_building_level": 30
    }
}

##############################################

class _GlobalGameParameters():
    def __init__(self, data: dict) -> None:
        self.types_damage = tuple(data["Types"]["Damage"])
        self.types_spaceship = tuple(data["Types"]["Spaceship"])
        self.types_rocket = tuple(data["Types"]["Rocket"])
        self.types_planet_type = tuple(data["Types"]["Planet_type"])
        self.types_planet_size = tuple(data["Types"]["Planet_size"])
        self.types_attack = tuple(data["Types"]["Attack_type"])
        self.types_building = tuple(data["Types"]["Building"])
        self.types_module = tuple(data["Types"]["Module"])
        self.types_valid_targets = tuple(data["Types"]["Valid_targets"])
        spaceships = {}
        for key in data["Spaceships"]:
            spaceships.update({int(key): data["Spaceships"][key]})
            raw_defenses = data["Spaceships"][key]["defenses"]
            defenses = {}
            for d_key in raw_defenses:
                defenses.update({int(d_key): raw_defenses[d_key]})
            spaceships[int(key)].update({"defenses": defenses})
        self.spaceships = spaceships
        damages = {}
        for key in data["Damages"]:
            damages.update({int(key): data["Damages"][key]})
        self.damages = damages
        self.planetary_coefs = data["Planetary_coefs"]
        rockets = {}
        for key in data["Rockets"]:
            rockets.update({int(key): data["Rockets"][key]})
            if "valid_targets" in rockets[int(key)]:
                rockets[int(key)]["valid_targets"] = tuple(rockets[int(key)]["valid_targets"])
        self.rockets = rockets
        buildings = {}
        for key in data["Buildings"]:
            buildings.update({int(key): data["Buildings"][key]})
        self.buildings = buildings
        modules = {}
        for key in data["Modules"]:
            modules.update({int(key): data["Modules"][key]})
        self.modules = modules
        #self.spaceships = data["Spaceships"]
        #self.damages = data["Damages"]
        #self.rockets = data["Rockets"]
        #self.buildings = data["Buildings"]
        #self.modules = data["Modules"]
        self.globals = data["Globals"]
        self.thold_per = data["Globals"]["thold_per"]
        self.thold_max = data["Globals"]["thold_max"]
        self.thold_max_bonus = data["Globals"]["thold_max_bonus"]
        self.accuracy = data["Globals"]["accuracy"]
        self.threshold = data["Globals"]["threshold"]
        self.assert_self_data()
        for key in self.rockets:
            valid_targets = self.rockets[key].get("valid_targets")
            if valid_targets is None:
                self.rockets[key].update({"valid_targets": self.types_valid_targets})
            else:
                assert type(valid_targets) == tuple
        for key in self.buildings:
            max_building_level = self.buildings[key].get("max_building_level")
            if max_building_level is None:
                self.buildings[key].update({"max_building_level": self.globals["max_building_level"]})
            else:
                assert type(max_building_level) == int
                assert max_building_level > 0

    def assert_self_data(self) -> None:
        assert type(self.types_damage) == tuple
        assert type(self.types_spaceship) == tuple
        assert type(self.types_rocket) == tuple
        assert type(self.types_planet_type) == tuple
        assert type(self.types_planet_size) == tuple
        assert type(self.types_attack) == tuple
        assert type(self.types_building) == tuple
        assert type(self.types_module) == tuple
        assert type(self.types_valid_targets) == tuple
        assert type(self.spaceships) == dict
        assert type(self.damages) == dict
        assert type(self.planetary_coefs) == dict
        assert type(self.rockets) == dict
        assert type(self.buildings) == dict
        assert type(self.modules) == dict
        assert type(self.globals) == dict
        assert len(self.types_damage) > 0
        assert len(self.types_spaceship) > 0
        assert len(self.types_rocket) > 0
        assert len(self.types_planet_type) > 0
        assert len(self.types_planet_size) > 0
        assert len(self.types_attack) > 0
        assert len(self.types_building) > 0
        assert len(self.types_module) > 0
        assert len(self.spaceships) > 0
        assert len(self.damages) > 0
        assert len(self.planetary_coefs) > 0
        assert len(self.rockets) > 0
        assert len(self.buildings) > 0
        assert len(self.modules) > 0
        assert len(self.globals) > 0
        assert self.types_damage == tuple(self.damages.keys())
        assert self.types_spaceship == tuple(self.spaceships.keys())
        assert self.types_rocket == tuple(self.rockets.keys())
        assert self.types_building == tuple(self.buildings.keys())
        assert self.types_module == tuple(self.modules.keys())
        assert type(self.thold_per) == float
        assert type(self.thold_max) == float
        assert type(self.thold_max_bonus) == int
        assert type(self.planetary_coefs) == dict
        assert type(self.accuracy) == int
        assert type(self.threshold) == float
        assert self.globals["turret_damage_type_id"] in self.types_damage
        assert self.globals["shield_damage_type_id"] in self.types_damage
        assert type(self.globals["max_building_level"]) == int
        assert self.thold_per > 0
        assert self.thold_max >= 1.0
        assert self.thold_max_bonus >= 0
        assert self.accuracy > 0
        assert self.accuracy <= 100
        assert self.threshold >= 0
        assert self.globals["max_building_level"] > 0
        for ss_id in self.types_valid_targets:
            assert ss_id in self.types_spaceship

##############################################

class _SpaceshipAssert():
    def __init__(self, id: int, name: str, name_en: str, damage_type_id: int, attack: int,\
                defense: int, defenses: dict, weight: int, attack_priority: int, \
                defense_priority: int, speed: int, calc_speed: float, price: int, \
                build_time: int, cargohold: int, radar: int, accuracy: float, ggp: _GlobalGameParameters) -> None:
        assert id in ggp.types_spaceship
        assert type(name) == str
        assert type(name_en) == str
        assert damage_type_id in ggp.types_damage
        assert type(attack) == int
        assert type(defense) == int
        assert type(defenses) == dict
        assert ggp.types_damage == tuple(defenses.keys())
        for key in defenses:
            assert type(defenses[key]) == int
            assert defenses[key] > 0
        assert type(weight) == int
        assert type(attack_priority) == int
        assert type(defense_priority) == int
        assert type(speed) == int
        assert type(calc_speed) == float
        assert type(price) == int
        assert type(build_time) == int
        assert type(cargohold) == int
        assert type(radar) == int
        assert type(accuracy) == int
        assert attack > 0
        assert defense > 0
        assert weight > 0
        assert attack_priority > 0
        assert defense_priority > 0
        assert speed > 0
        assert calc_speed > 0
        assert price > 0
        assert build_time > 0
        assert cargohold >= 0
        assert radar >= 0
        assert accuracy > 0
        assert accuracy <= 100

##############################################

class _RocketAssert():
    def __init__(self, id: int, name: str, name_en: str, warheads: int, damage: int, price: int, build_time: int, \
                damage_type_id: int, attack_type: int, valid_targets: tuple, ggp: _GlobalGameParameters) -> None:
        assert id in ggp.types_rocket
        assert type(name) == str
        assert type(name_en) == str
        assert type(warheads) == int
        assert warheads > 0
        assert type(damage) == int
        assert damage > 0
        assert type(price) == int
        assert price > 0
        assert type(build_time) == int
        assert build_time > 0
        assert damage_type_id in ggp.types_damage
        assert attack_type in ggp.types_attack
        assert type(valid_targets) == tuple

##############################################

def load_global_game_parameters(data: dict = _data) -> bool:
    """When you import this module (battlesimulation) all data is loaded, no need to call this func.
        But if you need to use custom data, you can call this and pass your data.
        If your data is invalid an Exception will be raised."""
    _ggp = _GlobalGameParameters(data)
    for i in _ggp.types_spaceship:
        spaceships = _SpaceshipAssert(**_ggp.spaceships.get(i), ggp=_ggp)
        assert type(spaceships) == _SpaceshipAssert
    for i in _ggp.types_rocket:
        rockets = _RocketAssert(**_ggp.rockets.get(i), ggp=_ggp)
        assert type(rockets) == _RocketAssert
    battlesimulation._GGP = _ggp
    return True
    #result = True
    #if result:
    #return result
    #try:
    #except:
    #    result = False
    #else:
    #    raise Exception("data passed is not fully valid.")
