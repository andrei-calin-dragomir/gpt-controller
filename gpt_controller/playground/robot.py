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
        for attribute in {k:v for (k,v) in attributes.items() if v == True}:
            if attribute == "ee_location": robot_status += "End effector location (x,y,z): ({},{},{})".format(self.actuator.ee_location_x, 
                                                                                                              self.actuator.ee_location_y, 
                                                                                                              self.actuator.ee_location_z)
            robot_status += "{} : {}".format(attribute, 'unknown' if getattr(self, attribute) is None else getattr(self, attribute))
        return
    
    def _generate_function_calls(self):
        function_calls = {}
        for method in dir(self):
            if not method.startswith('_') and callable(getattr(self, method)):
                function_calls[method] = getattr(self, method)
        return function_calls
    
    def verbose_description(self, attributes: list[str]=None):
        object_description : str = "Robot Status:" + "\n"
        if attributes is None:
            attributes = [attribute for attribute in dir(self) if not attribute.startswith('_') and not callable(getattr(self, attribute))]

        for attribute in attributes:
            value = getattr(self, attribute)
            if isinstance(value, Object):
                object_description += "Currently holding : {}".format(value.name)
            elif isinstance(value, float):
                object_description += "{} : {}".format(attribute, value)
            elif isinstance(value, set):
                object_description += "{} : {}".format(attribute, ", ".join([capability.value for capability in value]))
            elif isinstance(value, list):
                continue
            elif isinstance(value, str):
                object_description += "{} : '{}'".format(attribute, value)
            elif isinstance(value, dict):
                continue
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

    x : int = 0 # m
    y : int = 0 # m
    z : int = 0 # m

    def __init__(self, environment: Environment):
        self.environment = environment
        self.function_calls = self._generate_function_calls()

        self.navigation_schemas = [
            {
                "name": "move_to_object",
                "description": "Move to a point of interest.",
                "parameters": {
                    "type" : "object",
                    "properties": {
                        "name": {
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
            self.x = point_of_interest.x
            self.y = point_of_interest.y
            self.z = point_of_interest.z
            return "I moved to the {}.".format(name)
        else:
            return "Error: I could not find the {}.".format(name)

class Manipulator(Robot):

    # Gripper Information
    ee_location_x : float = 0 # m
    ee_location_y : float = 0 # m
    ee_location_z : float = 0 # m
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
                "description": "Cut an object using the object equipped in the gripper. Fails if the object is too far away or the object is not cuttable.",
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
                "description": "Open an object to make its contents available. Fails if the container is too far away or already open.",
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
        if not self.in_reach(object_name, support_surface):
            return "Error: Target location too far away"
        target_location = self.environment.get_object(support_surface)
        if target_location is not None:
            if self.object_held is not None:
                self.object_held.x = target_location.x
                self.object_held.y = target_location.y
                self.object_held.z = target_location.z
                self.object_held = None
                return "Object {} placed on {}".format(object_name, support_surface)
            else:
                return "Error: No object held"
        else:
            return "Error: Target location not found"

    def pick_up_object(self, object_name:str):
        try:
            if not self.in_reach(object_name):
                return "Error: Target object is too far away"
            object_of_interest = self.environment.get_object(object_name)
            if object_of_interest is not None:
                if self.object_held is None:
                    if object_of_interest.check_capability(Capability.FIXED):
                        return "Error: The {} is not movable".format(object_of_interest.name)
                    elif object_of_interest.check_capability(Capability.VISIBLE):
                        self.object_held = object_of_interest
                        self.ee_location_x = object_of_interest.x
                        self.ee_location_y = object_of_interest.y
                        self.ee_location_z = object_of_interest.z
                        return "Object {} picked up".format(object_name)
                    else:
                        return "Error: The {} is not accessible because its in {}".format(object_of_interest.name, object_of_interest.container)
                else:
                    return "Error: You are currently holding {}".format(self.object_held.name)
            else:
                return "Error: Object not found"
        except AttributeError as e:
            print("Error: {}".format(e))
        
    def cut_object(self, object_name:str):
        if not self.in_reach(object_name):
            return "Error: Target object is too far away"
        object_of_interest = self.environment.get_object(object_name)
        if object_of_interest is not None:
            if object_of_interest.check_capability(Capability.CUTTABLE):
                if self.object_held is not None:
                    return "Object {} has been cut".format(object_name)  
                else:
                    return "Error: You have nothing to cut with in your hand."
            return "Error: Object not cuttable"
        else:
            return "Error: Object not found"
        
    def put_object_in_container(self, container_name:str):
        if not self.in_reach(container_name):
            return "Error: Target container is too far away"
        container_of_interest = self.environment.get_object(container_name)
        if container_of_interest is not None:
            if container_of_interest.check_capability(Capability.CONTAINER):
                if self.object_held is not None:
                    return_string = "Object {} has been placed in {}".format(self.object_held.name, container_name)
                    container_of_interest.contains.append(self.object_held.name)
                    self.object_held.x = container_of_interest.x
                    self.object_held.y = container_of_interest.y
                    self.object_held.z = container_of_interest.z
                    self.object_held.container = container_of_interest.name
                    self.object_held = None
                    return return_string
                else:
                    return "Error: You are not holding the object you want to place in {}.".format(container_name)
            return "Error: {} is not a container.".format(container_name)
        else:
            return "Error: Container not found"
        
    def open_container(self, container_name:str):
        if not self.in_reach(container_name):
            return "Error: Target container is too far away"
        container_of_interest = self.environment.get_object(container_name)
        if container_of_interest is not None:
            if container_of_interest.check_capability(Capability.CONTAINER):
                for contained_obj in container_of_interest.contains:
                    self.environment.get_object(contained_obj).capabilities.add(Capability.VISIBLE)
                return "Container {} has been opened.".format(container_name)
            return "Error: {} is not a container.".format(container_name)
        else:
            return "Error: Container not found"
        
    def in_reach(self, object_name:str, target_location:str=None):
        object = self.environment.get_object(object_name)
        if target_location is None:
            if math.dist([self.ee_location_x,
                          self.ee_location_y,
                          self.ee_location_z],
                            [object.x,
                             object.y,
                             object.z]) > self.max_reach_distance:
                return False
        else:
            target = self.environment.get_object(target_location)
            if math.dist([object.x,
                          object.y,
                          object.z],
                            [target.x,
                             target.y,
                             target.z]) > self.max_reach_distance:
                return False
        return True
