import time
from statemachine import StateMachine, State
from gpt_controller.cognition import (
    manipulation,
    perception,
    querrying,
    reasoning,
)
# TODO #15 Fix the imports from util
# from gpt_controller.util.labels import User_Input_Label, Action_label

# TODO #9 Implement state machine up to input entry and data access points
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
    process_input = idle.to(decision_making, cond='is_input') \
                | idle.to.itself()
    

    # Decide processes user input if available and then takes a task from the task queue.
    decide = decision_making.to(loading_functionality, cond='is_task') \
            | decision_making.to(communicating, cond=["is_dialogue"]) \
            | decision_making.to(waiting, cond='is_pause') \
            | decision_making.to(memorizing, cond='is_abort') \
            | decision_making.to(evaluating, cond='is_task')
    
    resume = waiting.to(decision_making)
    
    # Act loads the required functionality (first checking short-term memory, then long-term memory) and then performs the task.
    act = loading_functionality.to(manipulating, cond=["is_manipulation_action"]) \
            | loading_functionality.to(perceiving, cond=["is_perception_action"]) \
            | loading_functionality.to(reasoning, cond=["is_reasoning_action"]) \
    

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
    troubleshoot = perceiving.to(error_handling, cond=['goal_predicates_unsatisfied']) \
                | manipulating.to(error_handling, cond=['goal_predicates_unsatisfied'])
    
    # If the system has found a potential solution to try, it tries it.
    retry_action = error_handling.to(decision_making)
    
    # Once a task or subtask is completed, the system evaluates its performance.
    self_reflect = reasoning.to(evaluating) \
            | perceiving.to(evaluating) \
            | manipulating.to(evaluating) \
            
    memorize = evaluating.to(memorizing) \
            | idle.to(memorizing, cond=['no_task_queue']) # If the system is idle, it memorizes the data in short-term memory.
    
    sleep = memorizing.to(idle)

    # The system shuts down if there is no input from the user for IDLE_TIMEOUT seconds.
    shutdown = idle.to(shutting_down, cond=["idle_timeout"])

    def __init__(self):
        self.task_history = []
        self.task_queue = []
        self.input_queue = []
        super().__init__()

    def before_transition(self, event, state):

        print(f"Before '{event}', on the '{state.id}' state.")

        return "before_transition_return"


    def on_transition(self, event, state):

        print(f"On '{event}', on the '{state.id}' state.")

        return "on_transition_return"


    def on_exit_state(self, event, state):

        print(f"Exiting '{state.id}' state from '{event}' event.")


    def on_enter_state(self, event, state):

        print(f"Entering '{state.id}' state from '{event}' event.")


    def after_transition(self, event, state):

        print(f"After '{event}', on the '{state.id}' state.")

    #TODO #7 Implement self-training
    def self_train(self, environment):
        pass

    def is_critical_state(self):
        
        return False
    
    def is_input(self):
        pass

    def is_task(self):
        pass

    def is_dialogue(self):
        pass

    def is_pause(self):
        pass

    def is_abort(self):
        pass

    def is_manipulation_action(self):
        pass

    def is_perception_action(self):
        pass

    def is_reasoning_action(self):
        pass

    def goal_predicates_unsatisfied(self):
        pass

    def no_task_queue(self):
        pass

    def idle_timeout(self):
        pass

    def run(self):
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