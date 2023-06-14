from gpt_controller.chat_gpt_interface import api_tools

perception_tasks =[
    {
      "task_id": 1,
      "task_name": "Image Classification",
      "description": "Classifying images into different predefined categories or labels."
    },
    {
      "task_id": 2,
      "task_name": "Object Detection",
      "description": "Detecting and localizing objects within an image."
    },
    {
      "task_id": 4,
      "task_name": "Instance Segmentation",
      "description": "Segmenting individual objects within an image and assigning a unique label to each instance."
    },
    {
      "task_id": 5,
      "task_name": "Pose Estimation",
      "description": "Estimating the pose (position and orientation) of objects or humans in an image."
    },
    {
      "task_id": 6,
      "task_name": "Optical Character Recognition (OCR)",
      "description": "Recognizing and extracting text from images or scanned documents."
    },
    {
      "task_id": 7,
      "task_name": "Speech Recognition",
      "description": "Converting spoken language into written text."
    },
    {
      "task_id": 9,
      "task_name": "Emotion Recognition",
      "description": "Detecting and classifying human emotions from facial expressions or voice recordings."
    },
    {
      "task_id": 10,
      "task_name": "Gesture Recognition",
      "description": "Recognizing and interpreting hand or body gestures for human-computer interaction."
    },
    {
        "task_id": 11,
        "task_name": "Object Tracking",
        "description": "Tracking the movement of objects or humans in a video sequence."
    },
    {
        "task_id": 12,
        "task_name": "Action Recognition",
        "description": "Recognizing and classifying human actions from video sequences."
    },
    {
        "task_id": 13,
        "task_name": "Feature Extraction",
        "description": "Extracting features about targets for further processing."
    }
  ]


# Self-assessment goal generation
def generate_goal(self, task):
  
  task['description']
  task['label']

  packaged_task = None

  completion = api_tools.request_completion()
