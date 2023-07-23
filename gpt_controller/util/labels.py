from enum import Enum

class Label(Enum):

    def __repr__(self):
        return self.name
    
    @classmethod
    def get_prompt_content(cls):
        prompt_content = "Labels:\n"
        for label in cls.__members__.keys():
            prompt_content += "{} = {}\n".format(label, cls.__members__[label].value)
        return prompt_content
    
class UserInputLabel(Label):
    TASK                        = "New task to be completed by the robot (example: 'Pick up object x', 'Go to location y', 'Take object x to location y', etc.)"
    QUESTION_ENV_KNOWLEDGE      = "Question to be answered about the surrounding environment of the robot such as objects and locations. It is formulated as a question that can be answered with a single word or a short phrase (example: 'Where is x?', 'What is the color of x?', 'What is the size of x?', etc.)"
    QUESTION_GEN_KNOWLEDGE      = "Question to be answered about non-situation specific knowledge. It is formulated as a question that can be answered with a single word or a short phrase (example: 'What is x?', 'What is the usual color of x?', 'What is the average size of x?', etc.)"
    METHODOLOGY                 = "Advice related to the method in which the robot can fulfill a certain action. It usually includes 'should' or 'could' but it is not limited to those words (example: 'You should pick up object x from the top.', 'You could use object x to do action y.', etc.))"
    LIMITATION                  = "Input related to what limitations the robot has when fulfilling a task from the user. It usually includes negative words such as 'cannot', 'should not', 'could not', etc. (example: 'You cannot use object x', 'You must not touch object x after you do actio y etc.)"
    OBJECT_INFORMATION          = "Attribute information regarding an object in the environment of the robot. It usually addresses a specific object, defining its attributes such as color, size, shape, etc. (example: 'Object x is red.', 'Object x is small.', 'There is an object x in location y.', etc.)"
    ABORT                       = "A request provided to the robot to abort the current task (example: 'Abort the current task.', 'Stop what you are doing.', 'Stop.', etc.)"
    UNCERTAIN                   = "None of the above tags apply to this input"

class AdviceLabel(Label):
    METHODOLOGY         = UserInputLabel.METHODOLOGY
    LIMITATION          = UserInputLabel.LIMITATION
    OBJECT_INFORMATION  = UserInputLabel.OBJECT_INFORMATION

class TaskLabel(Label):
    USER_INPUT                  = "User input. Do not use this label because it is used internally and automatically assigned by another function (examples: 'Pick up the tomato.', 'What is the color of the table?', 'How heavy is a tomato on average?')"
    INQUIRY                     = "Inquiry for advice, input or confirmation from the user (examples: 'Ask the user where the tomato is.', 'Ask the user how to pick up the tomato.', 'Ask the user if the tomato on the cutting board is the one they were reffering to.')"
    NAVIGATION                  = "Navigating through the environment (examples: 'Go to the kitchen.', 'Go to the table.', 'Go to the fridge.', 'Move to object.')"
    MANIPULATION                = "Interacting with objects in the environment (examples: 'Pick up the object.', 'Place the object on the table.', 'Open the object.', 'Close the object.', 'Cut the object.')"
    PERCEPTION                  = "Perception actions regarding the surrounding environment (examples: 'Detect the tomatoes.', 'Find the cutting board', 'Look at the table.')"
    COGNITION                   = "Cognitive actions such as recalling from memory, memorization or reasoning to generate a plan or estimation (examples: 'Recall the location of the tomato.', 'Estimate the weight of the tomato.', 'Reason about how to pick up the tomato.')"


    
