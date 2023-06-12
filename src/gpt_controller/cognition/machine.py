import time
from statemachine import StateMachine, State
from gpt_controller.cognition import (
    manipulation,
    perception,
    querrying,
    reasoning,
)
from gpt_controller.chat_gpt_interface.api_tools import Flag, Action_label

# TODO #9 Implement state machine up to input entry and data access points
# State Machine for the GPT Controller  (GPTC):
class GPTControllerMachine(StateMachine):
    # Add the input processing at the end of each state. If there is no input, continue with task queue.
    # States
    idle = State("Idle", initial=True)
    processing = State("Processing") # We call this for processing user input
    communicating = State("Communicating")
    working = State("Working")
    memorizing = State("Memorizing")
    evaluating = State("Evaluating")
    error = State("Error")
    exit = State("Exit", final=True)

    # Transitions
    start = idle.to(communicating)
    input = communicating.to(processing)
    
    work =  working.to(working) | processing.to(working) | memorizing.to(working) | evaluating.to(working)
    evaluate = working.to(evaluating)
    
    speak = working.to(communicating) \
        | evaluating.to(communicating) \
        | error.to(communicating) \
        | communicating.to(communicating)
        
    error_raised = working.to(error) | memorizing.to(error)
    keep_in_mind = working.to(memorizing) | processing.to(memorizing)

    # finish = evaluating.to(idle, unless='is_unsatisfactory_outcome') | evaluating.to(memorizing) 
    finish = evaluating.to(idle) | evaluating.to(memorizing) 

    evaluate = evaluating.to(memorizing, idle)
    
    abort = processing.to(idle, unless='is_critical_state')
    resume = processing.to(working) | memorizing.to(working)

    shutdown = idle.to(exit)

    def __init__(self):
        self.system_start_time = time.time()
        self.task_queue = []
        self.input_queue = []
        self.long_term_engine = 
        super(GPTControllerMachine,self).__init__()

    def add_input(self, user_input):
        self.input_queue.append(user_input)

    #TODO #7 Implement self-training
    def self_train(self, environment):
        pass

    def is_critical_state(self):
        
        return False

def main():
    machine = GPTControllerMachine(StateMachine)

    while(machine.current_state != "Exit"):
        print(machine.current_state)
        if machine.current_state == "Idle":
            machine.start()
        elif machine.current_state == "Communicating":
            machine.speak()
        elif machine.current_state == "Working":
            machine.work()
        elif machine.current_state == "Memorizing":
            machine.keep_in_mind()
        elif machine.current_state == "Evaluating":
            machine.evaluate()
        elif machine.current_state == "Error":
            machine.error_raised()
        elif machine.current_state == "Exit":
            machine.shutdown()
        else:
            print("Error: Invalid State")
    print(machine.current_state)