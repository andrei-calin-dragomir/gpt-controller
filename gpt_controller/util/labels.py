from enum import Enum

class Label(Enum):

    def __repr__(self):
        return self.name
    
    @classmethod
    def get_prompt_content(cls):
        prompt_content = "Labels:\n"
        for label in cls.__members__.keys():
            prompt_content += "{}: {}\n".format(label, cls.__members__[label].value)
        return prompt_content
    
class UserInputLabel(Label):
    TASK                        = "New task to be completed (e.g. 'Pick up the tomato.', 'Open the drawer.', 'Cut the tomato.')"
    QUESTION_ENV_KNOWLEDGE      = "Question to be answered about the environment of the robot (e.g. 'What is the color of the table?')"
    QUESTION_GEN_KNOWLEDGE      = "Question to be answered about general knowledge (e.g. 'How heavy is a tomato on average?', 'What is the size of the Eiffel Tower?')"
    METHODOLOGY                 = "Advice related to the method in which you can fulfill a task (e.g. 'You can pick up the tomato by grasping it from above.', 'You can open drawers by pulling them outwards.')"
    LIMITATION                  = "Input related to what limitations you have when fulfilling a task (e.g. 'You must only use a knife to cut a tomato', 'You must only use tomatoes from the fridge.', 'You must cut the tomato on a cutting board.')"
    OBJECT_INFORMATION          = "Advice related to the information of an object (e.g. 'The tomato is in the fridge.', 'The tomato is in the drawer.', 'The tomato is on the table.', 'The tomato is red.', 'The tomato is 100 grams.')"
    ABORT                       = "Abort the current task (e.g. 'Stop what you're doing.')"
    UNCERTAIN                   = "None of the above tags apply (e.g. 'I think cats are cute.')"

class AdviceLabel(Label):
    METHODOLOGY         = UserInputLabel.METHODOLOGY
    LIMITATION          = UserInputLabel.LIMITATION
    OBJECT_INFORMATION  = UserInputLabel.OBJECT_INFORMATION

class TaskLabel(Label):
    USER_INPUT                  = "User input. You should not use this label because it is used internally and automatically assigned by another function (e.g. 'Pick up the tomato.', 'What is the color of the table?', 'How heavy is a tomato on average?')"
    INQUIRY                     = "Inquiry for advice, input or confirmation from the user (e.g. 'Ask the user where the tomato is.', 'Ask the user how to pick up the tomato.', 'Ask the user if the tomato on the cutting board is the one they were reffering to.')"
    NAVIGATION                  = "Navigating through the environment (e.g. 'Go to the kitchen.', 'Go to the table.', 'Go to the fridge.')"
    MANIPULATION                = "Manipulating objects (e.g. 'Pick up the tomato.', 'Place the tomato on the table.', 'Open the drawer.')"
    PERCEPTION                  = "Perception actions regarding the surrounding environment (e.g. 'Detect the tomatoes.', 'Find the cutting board', 'Look at the table.')"
    COGNITION                   = "Cognitive actions such as recalling from memory, memorization or reasoning to generate a plan or estimation (e.g. 'Recall the location of the tomato.', 'Estimate the weight of the tomato.', 'Reason about how to pick up the tomato.')"


    
