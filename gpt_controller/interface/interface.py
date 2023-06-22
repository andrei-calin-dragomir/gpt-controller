import threading
from gpt_controller.cognition import machine
from gpt_controller.chat_gpt_interface import api_tools
from gpt_controller.interface.util import triggers
from gpt_controller.util import exceptions


from colorama import Fore, Style

# Printing in different colors
print(Fore.RED + "This text is red.")
print(Fore.GREEN + "This text is green.")
print(Fore.YELLOW + "This text is yellow.")
print(Fore.BLUE + "This text is blue.")
print(Fore.MAGENTA + "This text is magenta.")
print(Fore.CYAN + "This text is cyan.")

# Resetting the color
print(Style.RESET_ALL + "This text is back to the default color.")

def main():

    machine_instance = machine.GPTControllerMachine()
    
    # Start the input listener in a separate thread
    # TODO #3 Make this thread work on loop
    input_thread = threading.Thread(target=input_listener, args=(machine_instance))
    input_thread.daemon = True
    input_thread.start()

    machine_instance.main()

if __name__ == "__main__": 
    main()