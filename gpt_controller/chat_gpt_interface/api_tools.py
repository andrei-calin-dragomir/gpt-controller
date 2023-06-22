import os
import openai
import tiktoken
import json
from enum import Enum
from gpt_controller.util.exceptions import PromptingError
from gpt_controller.config import *
from gpt_controller.util import exceptions

openai.api_key = OPENAI_API_KEY

# Function to request a completion from the OpenAI API
# Returns a JSON object or a string depending on the expected output type
def request_completion(instruction_name, instruction_path, user_request=None):
    message_history = []
    if instruction_name:
        instruction_location = instruction_path + str(instruction_name)
        try:
            with open(instruction_location, "r") as f:
                prompt = f.read()
                f.flush()
            message_history.append({"role": "system", "content": prompt})
        except OSError:
            raise exceptions.PromptingError(instruction_name, instruction_location)
    
    if user_request:
        message_history.append({"role": "user", "content": user_request})
        
    for _ in range(int(MAX_RETRIES)):
        completion = openai.ChatCompletion.create(
            model=CHATGPT_MODEL,
            temperature=0,
            messages=message_history
        )
        if completion.choices[0].finish_reason == "stop":
            message_history = []
            return completion.choices[0].message.content
    
    raise exceptions.CompletionError(message_history[0], message_history[-1])

# Function to get prompt deck from the prompt directory as a dictionary
# Returns a dictionary of prompt names and prompts
def get_prompt_deck():
    try:
        instruction_list = os.walk(PROMPT_PATH).__next__()[2] # Get all files in

        for instruction_name in instruction_list:
            if not instruction_name.endswith(".txt"):
                raise PromptingError(instruction_name, PROMPT_PATH)
        prompt_deck = {}
        for instruction_name in instruction_list:
            instruction_path = PROMPT_PATH + instruction_name
            try:
                with open(instruction_path, "r") as f:
                    prompt = f.read()
                    prompt_deck[instruction_name] = prompt
                    f.flush()
            except OSError:
                raise PromptingError(instruction_name, PROMPT_PATH)
        return prompt_deck
    
    except PromptingError as e:
        print(e)

def get_environment_deck():
    try:
        environment_list = os.walk(ENV_PROMPT_PATH).__next__()[2] # Get all files in
        for environment_name in environment_list:
            if not environment_name.endswith(".txt"):
                raise PromptingError(environment_name, ENV_PROMPT_PATH)
        environment_deck = {}
        for environment_name in environment_list:
            environment_path = ENV_PROMPT_PATH + environment_name
            try:
                with open(environment_path, "r") as f:
                    environment = f.read()
                    environment_deck[environment_name] = environment
                    f.flush()
            except OSError:
                raise PromptingError(environment_name, environment_path)
        return environment_deck
    
    except PromptingError as e:
        print(e)

def num_tokens_prompt(prompt):
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(CHATGPT_MODEL)
    num_tokens = len(encoding.encode(prompt))
    return num_tokens

def get_contents_from_file(self, file_path):
    pass

def completion_to_json(input_string : str) -> dict:
    try:
        json_object = json.loads(input_string)
        return json_object
    except json.JSONDecodeError as e:
        raise exceptions.ParsingError('str','json')


class PromptBuilder(): 

    def gen_goal_predicates(self, task : json):
        pass
