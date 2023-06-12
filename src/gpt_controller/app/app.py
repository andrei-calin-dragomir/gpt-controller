import threading
from gpt_controller.cognition import machine
from gpt_controller.chat_gpt_interface import api_tools
from gpt_controller.app.util import triggers
from gpt_controller.util import exceptions


def input_listener(instance):
    while True:
        user_input = input("Enter a command: ")

        input_type = api_tools.request_completion('user_input_flagging.txt', [user_input])
        instance.add_input(user_input)
        
        raise triggers.UserInputTrigger()

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