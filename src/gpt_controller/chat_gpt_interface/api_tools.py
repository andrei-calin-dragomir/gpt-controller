import os
import openai
import tiktoken
import json
from enum import Enum
from gpt_controller.chat_gpt_interface import exceptions, api_tools
from gpt_controller.config import OPENAI_API_KEY, RETRIES_TO_ABORT, PROMPT_PATH, CHATGPT_MODEL

openai.api_key = OPENAI_API_KEY

class Flag(Enum):
    TASK                        : 1 # New task to be completed (e.g. "Pick up the tomato.")
    QUESTION_ENV_KNOWLEDGE      : 2 # Question to be answered about the environment of the robot (e.g. "What is the color of the table?")
    QUESTION_GEN_KNOWLEDGE      : 3 # Question to be answered about general knowledge (e.g. "How heavy is a tomato on average?")
    ADVICE                      : 4 # Advice on how to complete a task (e.g. "You should pick up the tomato from above.")
    ABORT                       : 5 # Abort the current task (e.g. "Stop what you're doing.")
    PAUSE                       : 6 # Pause the current task but don't abort it (e.g. "Wait a moment.")
    UNCERTAIN                   : 7 # None of the above tags apply (e.g. "I think cats are cute.")


class Action_label(Enum):
    PERCEIVE                    : 1 # Perceive the environment (e.g. "Detect the tomatoes.")
    REASONING                   : 2 # Reasoning (e.g. "Which tomato should I pick up?")
    MANIPULATION                : 3 # Manipulation (e.g. "Pick up the tomato.")
    WAITING                     : 4 # Waiting (e.g. "Wait until user tells me to place the tomato.")
    LOOP                        : 5 # Loop (e.g. "Repeat until all tomatoes are placed.")

# Function to request a completion from the OpenAI API
# Returns a JSON object or a string depending on the expected output type
def request_completion(prompt_name=None, message_history=[], user_request=None, expected_output_type="string"):
    if prompt_name:
        prompt_file = PROMPT_PATH + str(prompt_name)
        try:
            with open(prompt_file, "r") as f:
                prompt = f.read()
            message_history.append({"role": "system", "content": prompt})
        except OSError:
            raise exceptions.PromptingError(prompt_name, prompt_file)
    
    if user_request:
        message_history.append({"role": "user", "content": user_request})
        
    for _ in range(int(RETRIES_TO_ABORT)):
        completion = openai.ChatCompletion.create(
            model=CHATGPT_MODEL,
            temperature=0,
            messages=message_history
        )
        if completion.choices[0].finish_reason == "stop":
            print(completion.choices[0].message.content)
            if expected_output_type == "json":
                return api_tools.string_to_json(completion.choices[0].message.content)
            else:
                return completion.choices[0].message.content
     
    raise exceptions.CompletionError(message_history[0], message_history[-1])

# Function to get prompt deck from the prompt directory as a dictionary
# Returns a dictionary of prompt names and prompts
# Prompt names are the file names with or without the ".txt" extension
def get_prompt_deck(prompt_list=None):
    if not prompt_list:
        prompt_list = os.listdir(PROMPT_PATH)
    else:
        for prompt_name in prompt_list:
            if not prompt_name.endswith(".txt"):
                prompt_name += ".txt"
    prompt_deck = {}
    for prompt_name in prompt_list:
        prompt_file = PROMPT_PATH + prompt_name
        try:
            with open(prompt_file, "r") as f:
                prompt = f.read()
                prompt_deck[prompt_name] = prompt
        except OSError:
            print(f"Error: Could not open file {prompt_file}")
    return prompt_deck

def num_tokens_prompt(prompt):
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(CHATGPT_MODEL)
    num_tokens = len(encoding.encode(prompt))
    return num_tokens

def string_to_json(input_string : str) -> dict:
    try:
        json_object = json.loads(input_string)
        return json_object
    except json.JSONDecodeError as e:
        raise exceptions.ParsingError('str','json')