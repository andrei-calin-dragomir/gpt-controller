import os
import signal
import time
from statemachine import StateMachine, State
from gpt_controller.cognition import (
    manipulation,
    perception,
    querrying,
    reasoning,
)
from queue import Queue
# TODO #15 Fix the imports from util
from gpt_controller.util.labels import UserInputLabel, ActionLabel
from gpt_controller.chat_gpt_interface import api_tools


# State Machine for the GPT Controller  (GPTC):
class GPTControllerMachine(StateMachine):
    # Add the input processing at the end of each state. If there is no input, continue with task queue.
    # States
    idle = State("Idle", initial=True)
    decision_making = State("Decision Making") # We call this for processing user input or taking a task from the task queue.
    communicating = State("Communicating")
    loading_functionality = State("Loading Functionality")
    manipulating = State("Manipulating")
    perceiving = State("Perceiving")
    reasoning = State("Reasoning")
    keeping_in_mind = State("Keeping in Mind") # Store data in short-term memory.
    evaluating = State("Evaluating")
    waiting = State("Waiting")
    error_handling = State("Error Handling")
    memorizing = State("Memorizing") # Transfer data to long-term memory.
    shutting_down = State("Shutting Down", final=True)

    # Transitions
    # Process user input if available.
    process_input = idle.to(decision_making) \
                | idle.to.itself()
    

    # Decide processes user input if available and then takes a task from the task queue.
    decide = decision_making.to(loading_functionality) \
            | decision_making.to(communicating) \
            | decision_making.to(waiting) \
            | decision_making.to(memorizing) \
            | decision_making.to(evaluating)
    
    resume = waiting.to(decision_making)
    
    # Act loads the required functionality (first checking short-term memory, then long-term memory) and then performs the task.
    act = loading_functionality.to(manipulating)
    see = loading_functionality.to(perceiving)
    think = loading_functionality.to(reasoning)
    

    # From any acting state, if the functionality received as being closest to a solution requires extra information from the user,
    # a transition is triggered to the communicating state to ask the user and then waits for the user's feedback.
    ask_for_advice = reasoning.to(communicating) \
                | perceiving.to(communicating) \
                | manipulating.to(communicating) \
                | error_handling.to(communicating) # If the system doesn't know how to fix a system error, ask for advice.
    
    # Wait for user feedback.
    wait_for_advice = communicating.to(decision_making)

    # General event for when the system is gathering new data from the environment to be stored in short-term memory.
    acknowledge = perceiving.to(keeping_in_mind) \
                | manipulating.to(keeping_in_mind) \
                | reasoning.to(keeping_in_mind) \
                | decision_making.to(keeping_in_mind) # If user offered advice, store it in short-term memory.
    
    # If an implementation error happened, try to fix it for MAX_RETRIES times.
    troubleshoot = perceiving.to(error_handling) \
                | manipulating.to(error_handling)
    
    # If the system has found a potential solution to try, it tries it.
    retry_action = error_handling.to(decision_making)
    
    # Once a task or subtask is completed, the system evaluates its performance.
    self_reflect = reasoning.to(evaluating) \
            | perceiving.to(evaluating) \
            | manipulating.to(evaluating) \
            
    memorize = evaluating.to(memorizing) \
            | idle.to(memorizing) # If the system is idle, it memorizes the data in short-term memory.
    
    sleep = memorizing.to(idle)

    # The system shuts down if there is no input from the user for IDLE_TIMEOUT seconds.
    shutdown = idle.to(shutting_down)

    def __init__(self, StateMachine):
        self.task_history = []
        self.task_queue = []
        self.input_queue = Queue()
        super().__init__()

    #TODO #7 Implement self-training
    def self_train(self, environment):
        pass

    def run(self):
        machine = GPTControllerMachine(StateMachine)
        session_start = time.time()

        pid = os.fork()

        if pid == 0:
            while(machine.current_state != "Shutting Down"):
                print(machine.current_state.name)
                if machine.current_state == "Idle":
                    if not machine.input_queue.empty():
                        user_input = machine.input_queue.get()
                        if machine.input_queue.get() == "q":
                            machine.current_state = "Shutting Down"
                            machine.send('shutdown')
                        else:
                            output = api_tools.request_completion('task_segmentation.txt', None, user_input, 'string')
                            print(output)
                    pass
                elif machine.current_state == "Decision Making":
                    pass
                elif machine.current_state == "Communicating":
                    pass
                elif machine.current_state == "Loading Functionality":
                    pass
                elif machine.current_state == "Manipulating":
                    pass
                elif machine.current_state == "Perceiving":
                    pass
                elif machine.current_state == "Reasoning":
                    pass
                elif machine.current_state == "Keeping in Mind":
                    pass
                elif machine.current_state == "Evaluating":
                    pass
                elif machine.current_state == "Waiting":
                    pass
                elif machine.current_state == "Error Handling":
                    pass
                elif machine.current_state == "Memorizing":
                    pass
                else:
                    print("Error: Invalid State")
                    break
        
        else:
            print("This is the interface for the robot. Enter 'q' or Ctrl+D to quit.")
            try:
                while True:
                    user_input = input("Enter your input: ")
                    if user_input == "q":
                        print("Quitting...")
                        break
                    print("You entered:", user_input)
            except EOFError:
                os.kill(pid, signal.SIGTERM)
                return

        session_end = time.time()
        session_duration = session_end - session_start
        print(f"Session duration: {session_duration} seconds.")


if __name__ == "__main__":
    gpt_controller = GPTControllerMachine(StateMachine)
    gpt_controller.run()