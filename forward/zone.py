from ..utils.type_check import CheckValueTypeWithList
from enum import Enum

class Level(Enum):
    kWorld = 0
    kContinent = 1
    kIDC = 2
    kMachine = 3
    kService = 4
    kZoneMax = 5

kLevelMaxSuperNode = [20, 2, 2, 2, 1]

class Zone:
    def __init__(self, level:int, father, name:str):
        CheckValueTypeWithList([
            [level, int],
            [name, str]
        ])
        self.level = level
        self.father = father
        self.name = name
        self.enabled_services = {}  # xor result to sid
        self.disable_services = {}  # xor result to sid
        self.children = {}  # zone_key -> Zone
        self.super_nodes = {}  # service_id -> machine_id