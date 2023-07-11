import random
from colorama import Fore, Style
from gpt_controller.cognition.machine import Machine
from gpt_controller.playground.environment import Environment

if __name__ == "__main__":
    environment = Environment('kitchen')
    machine = Machine(environment)

    # You can change the information that the machine should start with in mind by setting basic_knowledge
    machine.fill_memory_with_objects(random.sample(environment.objects, random.randint(5, len(environment.objects))), basic_knowledge=True)

    try:
        while True:
            user_input = input("Enter command (for help functions type '--help') or press Enter to skip:")
            if user_input.startswith("--"):
                if user_input == "--objects_known":
                    for object in machine.object_knowledge:
                        print(object)
                elif user_input == "--objects_unknown":
                    objects = [object.name for object in machine.object_knowledge]
                    for object in environment.objects:
                        if object.name not in objects:
                            print(object)
                elif user_input == "--objects_in_environment":
                    for object in environment.objects:
                        print(object)
                elif user_input == "--tasks":
                    for task in machine.task_stack:
                        print(task)
                elif user_input == "--help":
                    print("Available commands:")
                    print("--objects_known: list all objects")
                    print("--objects_unknown: list all objects that are not known to the machine")
                    print("--objects_in_environment: list all objects in the environment")
                    print("--tasks: list all tasks")
                continue
            else:
                if user_input != "":
                    print(Fore.CYAN + "User: {}".format(user_input))
                    machine.parse_user_input(user_input)
                machine.step()
                if machine.task_stack: machine.task_stack[-1].print_conclusion()

    except EOFError:
        print(Fore.RED + "\nExiting...")
        print(Style.RESET_ALL)