import math
from gpt_controller.util.models import *
from gpt_controller.playground.environment import Environment

class Robot():
    def __init__(self, environment: Environment):
        self.actuator = Manipulator(environment)
        self.vision = Vision(environment)
        self.navigator = Navigator(environment)

    def __str__(self, attributes: dict[str, bool]):
        robot_status : str = ""
        for attribute, value in {k:v for (k,v) in attributes.items() if v == True}:
            if attribute == "ee_location": robot_status += "End effector location: {}".format(self.ee_location)
            robot_status += "{} : {}".format(attribute, 'unknown' if getattr(self, attribute) is None else getattr(self, attribute))
        return
    
    def _generate_function_calls(self):
        function_calls = {}
        for method in dir(self):
            if not method.startswith('_') and callable(getattr(self, method)):
                function_calls[method] = getattr(self, method)
        return function_calls
    
    def verbose_description(self, attributes: list[str]=None):
        object_description : str = "Robot : {} \n".format(self.name)
        if attributes is None:
            attributes = [attribute for attribute in dir(self) if not attribute.startswith('_') and not callable(getattr(self, attribute))]

        for attribute in attributes:
            if attribute == 'name': continue
            else:
                value = getattr(self, attribute)
                if isinstance(value, Object):
                    object_description += "{} : {}".format(attribute, value.name)
                elif isinstance(value, Coordinates | Dimensions):
                    object_description += "{} : {}".format(attribute, value)
                elif isinstance(value, set):
                    object_description += "{} : {}".format(attribute, ", ".join([capability.value for capability in value]))
                elif isinstance(value, list):
                    object_description += "{} : {}".format(attribute, ", ".join(value))
                elif isinstance(value, str):
                    object_description += "{} : '{}'".format(attribute, value)
        return object_description
    
class Vision(Robot):

    def __init__(self, environment: Environment):
        self.environment = environment
        self.function_calls = self._generate_function_calls()

        self.vision_schemas = [
            {
                "name": "look_around_for_object",
                "description": "Look around you for an object.",
                "parameters": {
                    "type" : "object",
                    "properties": {
                        "object_name": {
                            "type": "string",
                            "description": "The name of the object you are looking for."
                        }
                    }
                }
            },
            {
                "name": "search_in_container",
                "description": "Search in a container for an object.",
                "parameters": {
                    "type" : "object",
                    "properties": {
                        "container_name": {
                            "type": "string",
                            "description": "The name of the container you are looking in."
                        },
                        "object_name": {
                            "type": "string",
                            "description": "The name of the object you are looking for."
                        }
                    }
                }
            }
        ]

    def look_around_for_object(self, object_name:str):
        for obj in self.environment.get_visible_objects(self.head_orientation):
            if obj.name == object_name:
                return "I see the {}. Its on the {}".format(object_name, obj.support_surface)
        return "I don't see the around me {}.".format(object_name)
    
    def search_in_container(self, container_name:str, object_name:str):
        for obj in self.environment.get_object(container_name).contains:
            if obj.name == object_name:
                return "I have found the {}. Its in the {}".format(object_name, container_name)

class Navigator(Robot):

    location : Coordinates = None # m

    def __init__(self, environment: Environment):
        self.environment = environment
        self.location = Coordinates({'x' : 0.0, 'y' : 0.0, 'z' : 0.0})
        self.function_calls = self._generate_function_calls()

        self.navigation_schemas = [
            {
                "name": "move_to_object",
                "description": "Move to a point of interest.",
                "parameters": {
                    "type" : "object",
                    "properties": {
                        "point_of_interest": {
                            "type": "string",
                            "description": "The name of the object to move to."
                        }
                    }
                }
            }
        ]

    def move_to_object(self, name:str):
        point_of_interest = self.environment.get_object(name)
        if point_of_interest is not None:
            self.location = point_of_interest.location
            return True
        else:
            return False

class Manipulator(Robot):

    # Gripper Information
    ee_location : Coordinates = Coordinates({'x' : 0, 'y' : 0, 'z' : 0}) # m
    ee_gripper_width : float = 0.0 # m

    max_reach_distance : float = 2.0 # m

    # Object Information
    object_held : Object = None

    def __init__(self, environment: Environment):
        self.environment = environment
        self.function_calls = self._generate_function_calls()

        self.manipulation_schemas = [
            {
                "name": "pick_up_object",
                "description": "Pick up an object. Fails if the object is too heavy or too far away.",
                "parameters": {
                    "type" : "object",
                    "properties": {
                        "object_name": {
                            "type": "string",
                            "description": "The name of the object to pick up."
                        }
                    }
                }
            },
            {
                "name": "place_object",
                "description": "Place an object on a support surface. Fails if the object is too far away.",
                "parameters": {
                    "type" : "object",
                    "properties": {
                        "object_name": {
                            "type": "string",
                            "description": "The name of the object to place."
                        },
                        "support_surface": {
                            "type": "string",
                            "description": "The name of the support surface to place the object on."
                        }
                    }
                }
            },
            {
                "name": "cut_object",
                "description": "Cut an object. Fails if the object is too far away or not cuttable.",
                "parameters": {
                    "type" : "object",
                    "properties": {
                        "object_name": {
                            "type": "string",
                            "description": "The name of the object to cut."
                        }
                    }
                }
            },
            {
                "name": "put_object_in_container",
                "description": "Put an object in a container. Fails if the object is too far away or the container is full/not a container.",
                "parameters": {
                    "type" : "object",
                    "properties": {
                        "object_name": {
                            "type": "string",
                            "description": "The name of the object to put in the container."
                        },
                        "container_name": {
                            "type": "string",
                            "description": "The name of the container to put the object in."
                        }
                    }
                }
            },
            {
                "name": "open_container",
                "description": "Open a container. Fails if the container is too far away or already open.",
                "parameters": {
                    "type" : "object",
                    "properties": {
                        "container_name": {
                            "type": "string",
                        }
                    }
                }
            }
        ]

    def place_object(self, object_name:str, support_surface:str):
        if math.dist(self.ee_location, self.environment.get_object(support_surface).location) > self.max_reach_distance:
            return "Error: Target location too far away"
        target_location = self.environment.get_object(support_surface)
        if target_location is not None:
            if self.object_held is not None:
                self.object_held.location = target_location.location
                self.object_held = None
                return "Object {} placed on {}".format(object_name, support_surface)
            else:
                return "Error: No object held"

    def pick_up_object(self, object_name:str):
        try:
            if math.dist(self.ee_location, self.environment.get_object(object_name).location) > self.max_reach_distance:
                return "Error: Target object is too far away"
            object_of_interest = self.environment.get_object(object_name)
            print(object_of_interest)
            if object_of_interest is not None:
                if self.object_held is None:
                    if object_of_interest.check_capability(Capability.FIXED):
                        return "Error: The object cannot be moved - {}".format(object_of_interest.name)
                    self.object_held = object_of_interest
                    self.ee_gripper_width = object_of_interest.dimensions.width
                    self.ee_location = object_of_interest.location
                    return "Object {} picked up".format(object_name)
                else:
                    return "Error: You are already holding an object - {}".format(self.object_held.name)
            else:
                return "Error: Object not found"
        except AttributeError as e:
            print("Error: {}".format(e))
        
    def cut_object(self, object_name:str):
        if math.dist(self.ee_location, self.environment.get_object(object_name).location) > self.max_reach_distance:
            return "Error: Target object is too far away"
        object_of_interest = self.environment.get_object(object_name)
        if object_of_interest is not None:
            if object_of_interest.check_capability(Capability.CUTTABLE):
                if self.object_held is not None:
                    self.environment.remove_object(object_name)
                    self.environment.create_object_slices(object_name)
                else:
                    return "Error: You have nothing to cut with in your hand."
                return "Object {} has been cut".format(object_name)  
            return "Error: Object not cuttable"
        else:
            return "Error: Object not found"
        
    def put_object_in_container(self, container_name:str):
        if math.dist(self.ee_location, self.environment.get_object(container_name).location) > self.max_reach_distance:
            return "Error: Target container is too far away"
        container_of_interest = self.environment.get_object(container_name)
        if container_of_interest is not None:
            if container_of_interest.check_capability(Capability.CONTAINER):
                if self.object_held is not None:
                    return_string = "Object {} has been placed in {}".format(self.object_held.name, container_name)
                    self.object_held = None
                    return return_string
                else:
                    return "Error: You are not holding the object you want to place in {}.".format(container_name)
            return "Error: {} is not a container.".format(container_name)
        else:
            return "Error: Container not found"
        
    def open_container(self, container_name:str):
        if math.dist(self.ee_location, self.environment.get_object(container_name).location) > self.max_reach_distance:
            return "Error: Target container is too far away"
        container_of_interest = self.environment.get_object(container_name)
        if container_of_interest is not None:
            if container_of_interest.check_capability(Capability.CONTAINER):
                return "Container {} has been opened.".format(container_name)
            return "Error: {} is not a container.".format(container_name)
        else:
            return "Error: Container not found"
