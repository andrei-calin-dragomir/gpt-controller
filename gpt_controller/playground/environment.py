from gpt_controller.util.models import *
import math

class Environment:
    objects : list[Object] = []

    def __init__(self, scene:str):
        self.create_object({"name" : "floor", "color" : "brown", "shape" : Shape.CUBOIDAL, "material" : Material.WOOD, "x" : 0, "y" : 0, "z" : 0, "length" : 100, "width" : 100, "height" : 1, "capabilities" : Capability.FIXED, "support_surface" : None})

        if scene == "kitchen":
            self.load_kitchen()
        elif scene == "workstation":
            self.load_workstation()
        else:
            raise Exception("Scene not found")

    # Store an object in another object
    def put_object_in(self, object_name:str, container_name:str):
        container = self.get_object(container_name)
        object = self.get_object(object_name)
        object.capabilities.remove(Capability.VISIBLE)
        container.contains.append(object_name)
        self.place_object_on(object_name, container_name)
        object.container = container_name
    
    # Place an object on another object
    # Both objects must exist
    def place_object_on(self, object_name:str, support_name:str):
        support = self.get_object(support_name)
        for obj in self.objects:
            if obj.name == object_name:
                obj.x = support.x
                obj.y = support.y
                obj.z = support.z
                obj.support_surface = support_name
                return True

    # Get object instance by name
    def get_object(self, name:str):
        for obj in self.objects:
            if obj.name == name:
                return obj
        return None
    
    def remove_object(self, name:str):
        for obj in self.objects:
            if obj.name == name:
                self.objects.remove(obj)
                return True
        return False

    def create_object(self, object_attributes:dict):
        self.objects.append(Object(object_attributes))
        return "I have memorized this object." 
    
    def create_object_slices(self, object_name:str):
        object = self.get_object(object_name)
        new_object = Object({
            "name" : "slice of " + object.name,
            "color" : object.color,
            "shape" : object.shape,
            "material" : object.material,
            "length" : object.length/2,
            "x" : object.x - object.length/4,
            "support_surface" : object.support_surface,
            "capabilities" : object.capabilities,
            "contains" : object.contains
        })
        new_object_2 = Object({
            "name" : "slice of " + object.name,
            "color" : object.color,
            "shape" : object.shape,
            "material" : object.material,
            "length" : object.length/2,
            "x" : object.x + object.length/4,
            "support_surface" : object.support_surface,
            "capabilities" : object.capabilities,
            "contains" : object.contains
        })
        self.remove_object(object_name)
        self.objects.append(new_object)
        self.objects.append(new_object_2)

    # Load a kitchen environment
    def load_kitchen(self):


        # Create objects
        self.create_object({"name" : "knife", "color" : "silver", "shape" : Shape.OTHER, "material" : Material.METAL})
        self.create_object({"name" : "fork", "color" : "silver", "shape" : Shape.OTHER, "material" : Material.METAL})
        self.create_object({"name" : "spoon", "color" : "silver", "shape" : Shape.OTHER, "material" : Material.METAL})
        self.create_object({"name" : "plate", "color" : "white", "shape" : Shape.CYLINDRICAL, "material" : Material.CERAMIC})
        self.create_object({"name" : "cup", "color" : "white", "shape" : Shape.CYLINDRICAL, "material" : Material.CERAMIC})
        self.create_object({"name" : "bowl", "color" : "white", "shape" : Shape.CYLINDRICAL, "material" : Material.CERAMIC})
        self.create_object({"name" : "pan", "color" : "black", "shape" : Shape.CYLINDRICAL, "material" : Material.METAL})
        self.create_object({"name" : "pot", "color" : "black", "shape" : Shape.CYLINDRICAL, "material" : Material.METAL})
        self.create_object({"name" : "cutting board", "color" : "brown", "shape" : Shape.CUBOIDAL, "material" : Material.WOOD})

        # Create furniture
        self.create_object({"name" : "table", "color" : "brown", "shape" : Shape.CUBOIDAL, "material" : Material.WOOD})
        self.create_object({"name" : "chair", "color" : "brown", "shape" : Shape.CUBOIDAL, "material" : Material.WOOD})
        self.create_object({"name" : "stove", "color" : "black", "shape" : Shape.CUBOIDAL, "material" : Material.METAL})
        self.create_object({"name" : "sink", "color" : "white", "shape" : Shape.CUBOIDAL, "material" : Material.CERAMIC})
        self.create_object({"name" : "oven", "color" : "black", "shape" : Shape.CUBOIDAL, "material" : Material.METAL})
        self.create_object({"name" : "microwave", "color" : "black", "shape" : Shape.CUBOIDAL, "material" : Material.METAL})
        self.create_object({"name" : "fridge", "color" : "white", "shape" : Shape.CUBOIDAL, "material" : Material.METAL, "x" : 1, "y" : 0.5, "z" : 0.5})
        self.create_object({"name" : "base_cabinet", "color" : "brown", "shape" : Shape.CUBOIDAL, "material" : Material.WOOD, "x" : 0.5, "y" : 0.5, "z" : 0.5})
        self.create_object({"name" : "wall_cabinet", "color" : "brown", "shape" : Shape.CUBOIDAL, "material" : Material.WOOD})

        self.place_object_on("table", "floor")
        self.get_object("base_cabinet").add_capability(Capability.CONTAINER)
        self.put_object_in("plate", "base_cabinet")
        self.put_object_in("cup", "base_cabinet")
        self.put_object_in("bowl", "base_cabinet")
        self.put_object_in("pan", "base_cabinet")
        self.put_object_in("pot", "base_cabinet")

        self.place_object_on("microwave", "base_cabinet")

        self.place_object_on("cutting_board", "table")
        self.place_object_on("knife", "table")
        self.place_object_on("fork", "table")
        self.place_object_on("spoon", "table")

        # Create food
        self.create_object({"name" : "egg", "color" : "white", "shape" : Shape.SPHERICAL, "material" : Material.OTHER})
        self.create_object({"name" : "milk", "color" : "white", "shape" : Shape.CYLINDRICAL, "material" : Material.OTHER})
        self.create_object({"name" : "flour", "color" : "white", "shape" : Shape.OTHER, "material" : Material.OTHER})
        self.create_object({"name" : "apple", "color" : "red", "shape" : Shape.SPHERICAL, "material" : Material.OTHER})
        self.create_object({"name" : "banana", "color" : "yellow", "shape" : Shape.CYLINDRICAL, "material" : Material.OTHER})
        self.create_object({"name" : "orange", "color" : "orange", "shape" : Shape.SPHERICAL, "material" : Material.OTHER})
        self.create_object({"name" : "tomato", "color" : "red", "shape" : Shape.SPHERICAL, "material" : Material.OTHER})
        self.create_object({"name" : "potato", "color" : "brown", "shape" : Shape.SPHERICAL, "material" : Material.OTHER})
        self.create_object({"name" : "onion", "color" : "white", "shape" : Shape.SPHERICAL, "material" : Material.OTHER})
        self.create_object({"name" : "cucumber", "color" : "green", "shape" : Shape.CYLINDRICAL, "material" : Material.OTHER})
        self.create_object({"name" : "carrot", "color" : "orange", "shape" : Shape.CYLINDRICAL, "material" : Material.OTHER})
        self.create_object({"name" : "lettuce", "color" : "green", "shape" : Shape.OTHER, "material" : Material.OTHER})

        self.get_object("fridge").add_capability(Capability.CONTAINER)
        self.put_object_in("egg", "fridge")
        self.put_object_in("milk", "fridge")
        self.put_object_in("apple", "fridge")
        self.put_object_in("orange", "fridge")
        self.put_object_in("onion", "fridge")
        self.put_object_in("cucumber", "fridge")
        self.put_object_in("carrot", "fridge")
        self.put_object_in("lettuce", "fridge")

        self.get_object("wall_cabinet").add_capability(Capability.CONTAINER)
        self.put_object_in("banana", "wall_cabinet")
        self.put_object_in("flour", "wall_cabinet")

        self.place_object_on("tomato", "table")
        self.place_object_on("potato", "table")

        for obj in self.objects:
            if obj.material == Material.OTHER:
                obj.add_capability(Capability.CUTTABLE)

    def load_workstation(self):
        
        # Create furniture
        self.create_object({"name" : "table", "color" : "brown", "shape" : Shape.CUBOIDAL, "material" : Material.WOOD})
        self.create_object({"name" : "storage unit", "color" : "brown", "shape" : Shape.CUBOIDAL, "material" : Material.WOOD})

        # Create objects
        self.create_object({"name" : "screwdriver", "color" : "silver", "shape" : Shape.OTHER, "material" : Material.METAL})
        self.create_object({"name" : "hammer", "color" : "silver", "shape" : Shape.OTHER, "material" : Material.METAL})
        self.create_object({"name" : "wrench", "color" : "silver", "shape" : Shape.OTHER, "material" : Material.METAL})
        self.create_object({"name" : "pliers", "color" : "silver", "shape" : Shape.OTHER, "material" : Material.METAL})
        self.create_object({"name" : "screwbox", "color" : "red", "shape" : Shape.CUBOIDAL, "material" : Material.PLASTIC})

        # Create contained objects
        self.create_object({"name" : "screw_1", "color" : "silver", "shape" : Shape.OTHER, "material" : Material.METAL})
        self.create_object({"name" : "screw_2", "color" : "silver", "shape" : Shape.OTHER, "material" : Material.METAL})
        self.create_object({"name" : "screw_3", "color" : "silver", "shape" : Shape.OTHER, "material" : Material.METAL})
        self.create_object({"name" : "screw_4", "color" : "silver", "shape" : Shape.OTHER, "material" : Material.METAL})
        self.create_object({"name" : "screw_5", "color" : "silver", "shape" : Shape.OTHER, "material" : Material.METAL})
        pass