from enum import Enum

class UserInputLabel(Enum):
    TASK                        : 1 # New task to be completed (e.g. "Pick up the tomato.")
    QUESTION_ENV_KNOWLEDGE      : 2 # Question to be answered about the environment of the robot (e.g. "What is the color of the table?")
    QUESTION_GEN_KNOWLEDGE      : 3 # Question to be answered about general knowledge (e.g. "How heavy is a tomato on average?")
    ADVICE                      : 4 # Advice on how to complete a task (e.g. "You should pick up the tomato from above.")
    ABORT                       : 5 # Abort the current task (e.g. "Stop what you're doing.")
    PAUSE                       : 6 # Pause the current task but don't abort it (e.g. "Wait a moment.")
    UNCERTAIN                   : 7 # None of the above tags apply (e.g. "I think cats are cute.")

    def __repr__(self):
        return self.__class__.__members__.keys()

class Label(Enum):

    def __repr__(self):
        return self.__class__.__members__.keys()

class ActionLabel(Label):
    PERCEIVE                    : 1 # Perception actions regarding the surrounding environment (e.g. "Detect the tomatoes.")
    REASONING                   : 2 # Reasoning (e.g. "Which tomato should I pick up?")
    MANIPULATION                : 3 # Manipulation (e.g. "Pick up the tomato.")
    WAITING                     : 4 # Waiting (e.g. "Wait until user tells me to place the tomato.")
    LOOP                        : 5 # Loop (e.g. "Repeat until all tomatoes are placed.")


    
class PerceptionLabel(Enum):
    ENVIRONMENT_LABELLING           : 1 # Classifying environment (e.g. "Analyze your surroundings.")
    INSTANCE_SEGMENTATION           : 3 # Segmenting individual objects within the environment and assigning a unique label to each instance. (e.g. "Scan what is on the table.")
    OPTICAL_CHARACTER_RECOGNITION   : 5 # Recognizing and extracting text from images or scanned documents. (e.g. "Read the label on the tomato.")
    EMOTION_RECOGNITION             : 6 # Detecting and classifying human emotions from facial expressions or voice recordings.
    GESTURE_RECOGNITION             : 7 # Recognizing and interpreting hand or body gestures for human-computer interaction.
    ACTION_RECOGNITION              : 9 # Recognizing and classifying human actions from video sequences.
    OBJECT_DETECTION                : 2 # Detecting and localizing objects within the environment. (e.g. "Detect the tomatoes.")
    OBJECT_TRACKING                 : 8 # Tracking the movement of objects or humans in a video sequence.
    OBJECT_FEATURE_EXTRACTION       : 10 # Extracting features about target for further processing. (e.g. "What is the color of the tomato?")

    def __repr__(self):
        return self.__class__.__members__.keys()
    

# ActionLabel.PERCEIVE.value = [PerceptionLabel.ENVIRONMENT_LABELLING, PerceptionLabel.INSTANCE_SEGMENTATION, PerceptionLabel.OPTICAL_CHARACTER_RECOGNITION, PerceptionLabel.EMOTION_RECOGNITION, PerceptionLabel.GESTURE_RECOGNITION, PerceptionLabel.ACTION_RECOGNITION, PerceptionLabel.OBJECT_DETECTION, PerceptionLabel.OBJECT_TRACKING, PerceptionLabel.OBJECT_FEATURE_EXTRACTION]