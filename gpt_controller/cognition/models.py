from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4


class Shape(Enum):
    CYLYNDRICAL = 1
    SPHERICAL = 2
    RECTANGULAR = 3
    CONICAL = 4
    
class Coordinates:
    x : int
    y : int
    z : int
    
class Dimensions:
    length : int
    width : int
    height : int
    
class Capability(Enum):
    FIXED = 1
    CONTAINER = 2
    LIFTABLE = 3

@dataclass
class Object:
    
    # Identifiers
    id : int = uuid4
    name : str
    color : str = None
    shape : Shape = None
    
    # Dimensions
    dimensions : Dimensions = None
    
    # Location
    coordinates : Coordinates = Coordinates(0, 0, 0)
    support_frame : str = 'world'
    
    # Capabilities
    capabilities : set[Capability] = set()
    
    # Inventory
    contains: list[int]
    
    def __init__(self, name:str, color:str = None, shape:Shape=None, material:str=None):
        self.name = name
        self.color = color
        self.shape = shape
        self.material = material