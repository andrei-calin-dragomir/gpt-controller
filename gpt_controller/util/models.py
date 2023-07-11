from dataclasses import dataclass, field
from gpt_controller.config import *
from gpt_controller.util.labels import *
from colorama import Fore, Style
from enum import Enum
from uuid import uuid4
from datetime import datetime, timedelta
import json

class Shape(Enum):
    CYLINDRICAL = 'cylindrical'
    SPHERICAL   = 'spherical'
    CUBOIDAL    = 'cuboidal'
    CONICAL     = 'conical'
    OTHER       = 'complex'
    
class Capability(Enum):
    FIXED = 'fixed'
    CONTAINER = 'container'
    EQUIPPABLE = 'equippable'
    USABLE = 'usable'
    VISIBLE = 'visible'
    CUTTABLE = 'cuttable'

class Coordinates:
    x : int
    y : int
    z : int

    def __init__(self, values:dict[str, int]):
        self.x = values['x']
        self.y = values['y']
        self.z = values['z']

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __str__(self):
        return "x: {} | y: {} | z: {}".format(self.x, self.y, self.z)
    
class Dimensions:
    length : int
    width : int
    height : int

    def __init__(self, values:dict[str, int]):
        self.length = values['length']
        self.width = values['width']
        self.height = values['height']

    def __str__(self):
        representation : str = "length: {}".format(self.length)
        if self.width is not None:
            representation += " | width: {}".format(self.width)
        if self.height is not None:
            representation += " | height: {}".format(self.height)
        return representation
    
class Material(Enum):
    WOOD    = 'wood'
    METAL   = 'metal'
    PLASTIC = 'plastic'
    CERAMIC = 'ceramic'
    GLASS   = 'glass'
    PAPER   = 'paper'
    ORGANIC = 'organic'
    OTHER   = 'other'

@dataclass
class Object:
    
    # Identifiers
    name : str
    id : int = uuid4
    color : str = None
    shape : Shape = None
    material : Material = None

    
    # Dimensions
    dimensions : Dimensions = None
    
    # Location
    location : Coordinates = Coordinates({'x': 0, 'y': 0, 'z': 0})
    support_surface : str = 'ground'
    
    # Capabilities
    capabilities : set[Capability] = field(default_factory=set)
    
    # Inventory
    contains: list[str] = field(default_factory=list)
    
    def __init__(self, attributes: dict[str, any]):
        self.contains = []
        self.capabilities = set()
        for attribute, value in attributes.items():
            if attribute == 'name':
                setattr(self, attribute, value)
            elif attribute == 'shape':
                setattr(self, attribute, Shape(value))
            elif attribute == 'material':
                setattr(self, attribute, Material(value))
            elif attribute == 'dimensions':
                setattr(self, attribute, Dimensions(value))
            elif attribute == 'location':
                setattr(self, attribute, Coordinates(value))
            elif attribute == 'capabilities':
                setattr(self, attribute, set([Capability(capability) for capability in json.loads(value)]))
            elif attribute == 'contains':
                setattr(self, attribute, json.loads(value))
            else:
                setattr(self, attribute, value)

    def verbose_description(self, attributes: list[str]):
        object_description : str = "Object name: {} \n".format(self.name)
        for attribute in attributes:
            if attribute == 'name': continue
            else:
                value = getattr(self, attribute)
                if isinstance(value, Enum):
                    object_description += "{} : {}".format(attribute, value.value)
                elif isinstance(value, Coordinates | Dimensions):
                    object_description += "{} : {}".format(attribute, value)
                elif isinstance(value, set):
                    object_description += "{} : {}".format(attribute, ", ".join([capability.value for capability in value]))
                elif isinstance(value, list):
                    object_description += "{} : {}".format(attribute, ", ".join(value))
                elif isinstance(value, str):
                    object_description += "{} : '{}'".format(attribute, value)
        return object_description
    
    def add_capability(self, capability:Capability):
        self.capabilities.add(capability)
    
    def check_capability(self, capability:Capability):
        for capability in self.capabilities:
            if capability == capability:
                return True
        return False
    
    def __repr__(self):
        return self.name

class Role(Enum):
    USER                    = "user"
    SYSTEM                  = "system"
    ASSISTANT               = "assistant"
    ASSISTANT_FUNCTION_CALL = "assistant"
    FUNCTION                = "function"

@dataclass
class Message:
    role : Role
    content : json
    timestamp : datetime = None

    def __init__(self, role:Role, content:str | dict):
        self.role = role
        self.timestamp = datetime.now()
        if isinstance(content, str):
            self.content = {"role": self.role.value, "content": content}
        else:
            self.content = content

class ConversationType(Enum):
    CHAT = "Chat"
    UNDERSTANDING = "Understanding"
    LABELLING = "Labelling"
    RECALLING = "Recalling"
    DECIDING = "Deciding"
    MEMORIZING = "Memorizing"
    ACTING = "Acting"

@dataclass
class Conversation:
    type : ConversationType
    id : int = uuid4
    messages : list[Message] = field(default_factory=list)
    start_time : datetime = None
    finish_time : datetime = None
    total_time : timedelta = None

    token_quota : int = 0
    
    def __init__(self, type:ConversationType):
        self.type = type
        self.messages = []
        self.start_time = datetime.now()
    
    def finish(self):
        self.finish_time = datetime.now()
        self.total_time = self.finish_time - self.start_time
    
    def get_messages(self):
        return self.messages

@dataclass
class Advice:
    type : AdviceLabel
    id : int = uuid4
    content : str = None
    timestamp : datetime = None

    def __init__(self, label : str | AdviceLabel, content : str):
        if isinstance(label, str) : self.type = getattr(AdviceLabel, label)
        else : self.type = label
        self.content = content
        self.timestamp = datetime.now()

    def get_context(self):
        return self.content


class TaskStatus(Enum):
    NEW = "New"
    PAUSED      = "Paused"
    IN_PROGRESS = "In Progress"
    COMPLETED   = "Completed"
    FAILED      = "Failed"

@dataclass
class Task:
    goal : str
    type : TaskLabel
    id : int = uuid4
    goal_predicates : dict[TaskLabel | str] = field(default_factory=dict)

    conclusion : str = None
    status : TaskStatus = TaskStatus.NEW

    function_name : str = None
    function_content : str = None
    
    start_time : datetime = datetime.now()
    stop_time : datetime = None
    total_time : timedelta = timedelta(seconds=0)

    # ID's of subtasks that happened during this task
    sub_tasks : list[int] = field(default_factory=list)

    def __init__(self, label : str | TaskLabel, goal : str):
        self.goal_predicates = {}
        if isinstance(label, str) : self.type = getattr(TaskLabel, label)
        else: self.type = label
        self.goal = goal


    def start(self, goal_predicates:list[str]=None):
        if goal_predicates: self.goal_predicates = goal_predicates
        if self.status == TaskStatus.NEW:
            self.start_time = datetime.now()
        else:
            self.total_time = datetime.now() - self.stop_time
        self.status = TaskStatus.IN_PROGRESS
    
    def pause(self):
        self.status = TaskStatus.PAUSED
        self.stop_time = datetime.now()
        self.total_time += self.stop_time - self.start_time

    def complete(self, conclusion:str, status:bool):
        if status: self.status = TaskStatus.COMPLETED
        else: self.status = TaskStatus.FAILED
        self.conclusion = conclusion
        self.stop_time = datetime.now()
        self.total_time += self.stop_time - self.start_time

    def get_context(self):
        if self.type == TaskLabel.USER_INPUT:
            return "User: {}".format(self.goal)
        else:
            return "{} Action: {}\nConclusion: {}\nStatus {}".format(self.type, 
                                                                    self.goal, 
                                                                    self.conclusion,
                                                                    self.status.value)

    def print_conclusion(self):
        if self.status:
            print(Fore.GREEN + "Robot: {}".format(self.conclusion))
        else:
            print(Fore.RED + "Robot: {}".format(self.conclusion))
        print(Style.RESET_ALL)

@dataclass
class Function:
    type : TaskLabel
    goal : str
    goal_predicates : dict[TaskLabel | str] = field(default_factory=dict)

    id : int = uuid4
    start_time : datetime = datetime.now()

    learned_sequence : list[Task] = field(default_factory=list)

    def __init__(self, type : TaskLabel, goal : str, goal_predicates : dict[TaskLabel | str] = None):
        if goal_predicates: self.goal_predicates = goal_predicates
        else: self.goal_predicates = {}
        self.type = type
        self.goal = goal
        self.start_time = datetime.now()

    def memorize_function(self, tasks : list[Task]):
        for task in tasks:
            self.learned_sequence.append(task)

