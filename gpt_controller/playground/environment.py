from gpt_controller.util.models import *
import math

class Environment:
    objects : list[Object] = []

    def __init__(self, scene:str):
        self.create_object({"name" : "ground", "color" : "brown", "shape" : Shape.CUBOIDAL, "material" : Material.WOOD, "location" : {"x" : 0, "y" : 0, "z" : 0}})

        if scene == "kitchen":
            self.load_kitchen()
        elif scene == "workstation":
            self.load_workstation()
        else:
            raise Exception("Scene not found")
        
    def create_object(self, name:str, color:str = None, shape:Shape=None, material:str=None):
        obj = Object(name, color, shape, material)
        pass

    # Store an object in another object
    # The container object must exist and must have the container value set to True
    def put_object_in(self, object_name:str, container_name:str):
        container = self.get_object(container_name)
        container.contains.append(self.get_object(object_name))
        self.remove_object(object_name)
    
    # Place an object on another object
    # Both objects must exist
    def place_object_on(self, object_name:str, support_name:str):
        for obj in self.objects:
            if obj.name == object_name:
                obj.support_surface = support_name
                return True

    def get_visible_objects(self, location:Coordinates):
        objects_in_view = []
        for obj in self.objects:
            if math.dist(location, obj.location) < 2:
                objects_in_view.append(obj)

        return objects_in_view

    # Get object instance by name
    def get_object(self, name:str):
        for obj in self.objects:
            if obj.name == name:
                return obj
            else:
                if obj.contains is not None:
                    for contained_object in obj.contains:
                        if contained_object.name == name:
                            return contained_object
        return None
    
    def remove_object(self, name:str):
        for obj in self.objects:
            if obj.name == name:
                self.objects.remove(obj)
                return True
            else:
                for contained_object in obj.contains:
                    if contained_object.name == name:
                        obj.contains.remove(contained_object)
                        return True
        return False

    def create_object(self, object_attributes:dict):
        self.objects.append(Object(object_attributes))
        return "I have memorized this object." 
    
    def create_object_slices(self, object_name:str):
        object = self.get_object(object_name)
        new_object = Object({
            "name" : "part of" + object.name,
            "color" : object.color,
            "shape" : object.shape,
            "material" : object.material,
            "dimensions" : Dimensions(object.dimensions.length/2, object.dimensions.width/2, object.dimensions.height/2),
            "location" : object.location,
            "support_surface" : object.support_surface,
            "capabilities" : object.capabilities,
            "contains" : object.contains
        })
        self.remove_object(object_name)
        self.objects.append(new_object)
        self.objects.append(Object(self.get_object(object_name)))

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
        self.create_object({"name" : "fridge", "color" : "white", "shape" : Shape.CUBOIDAL, "material" : Material.METAL})
        self.create_object({"name" : "base_cabinet", "color" : "brown", "shape" : Shape.CUBOIDAL, "material" : Material.WOOD, "location" : {"x" : 5, "y" : 10, "z" : 5}})
        self.create_object({"name" : "wall_cabinet", "color" : "brown", "shape" : Shape.CUBOIDAL, "material" : Material.WOOD})

        self.get_object("base_cabinet").add_capability(Capability.CONTAINER)
        self.put_object_in("plate", "base_cabinet")
        self.put_object_in("cup", "base_cabinet")
        self.put_object_in("bowl", "base_cabinet")
        self.put_object_in("pan", "base_cabinet")
        self.put_object_in("pot", "base_cabinet")

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

        self.get_object("fridge").add_capability(Capability.CONTAINER)
        self.put_object_in("egg", "fridge")
        self.put_object_in("milk", "fridge")
        self.put_object_in("apple", "fridge")
        self.put_object_in("orange", "fridge")

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