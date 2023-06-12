from enum import Enum

class User_Input_Label(Enum):
    TASK                        : 1 # New task to be completed (e.g. "Pick up the tomato.")
    QUESTION_ENV_KNOWLEDGE      : 2 # Question to be answered about the environment of the robot (e.g. "What is the color of the table?")
    QUESTION_GEN_KNOWLEDGE      : 3 # Question to be answered about general knowledge (e.g. "How heavy is a tomato on average?")
    ADVICE                      : 4 # Advice on how to complete a task (e.g. "You should pick up the tomato from above.")
    ABORT                       : 5 # Abort the current task (e.g. "Stop what you're doing.")
    PAUSE                       : 6 # Pause the current task but don't abort it (e.g. "Wait a moment.")
    UNCERTAIN                   : 7 # None of the above tags apply (e.g. "I think cats are cute.")

    def __repr__(self):
        return self.__class__.__members__.keys()


class Action_label(Enum):
    PERCEIVE                    : 1 # Perceive the environment (e.g. "Detect the tomatoes.")
    REASONING                   : 2 # Reasoning (e.g. "Which tomato should I pick up?")
    MANIPULATION                : 3 # Manipulation (e.g. "Pick up the tomato.")
    WAITING                     : 4 # Waiting (e.g. "Wait until user tells me to place the tomato.")
    LOOP                        : 5 # Loop (e.g. "Repeat until all tomatoes are placed.")

    def __repr__(self):
        return self.__class__.__members__.keys()