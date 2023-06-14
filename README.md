## GPT Controller

This python package integrates chatGPT in the cognitive process of a robotic system.

## Prerequisites

- Python 3.10
- `poetry` package manager (`pip install poetry`)
- `graphviz` for graph generation (`sudo apt install graphviz`) 

## Installation

1. Clone the repository:

```bash
git clone https://github.com/andrei-calin-dragomir/gpt-controller.git
```

2. Navigate to the project directory:

```bash
cd gpt-controller
```

3. Install system project dependencies:

Optional: The following package is required only for visualisations in the `evaluation_interface.ipynb` file.
```bash
sudo apt-get install graphviz
```

**Disclaimer:** Don't install dependencies manually. Use poetry instead:

```bash
poetry install
```
4. Configure project:

    Open the `config.py` file in the root directory and fill all the entries with the required information.

5. Future ideas:
    - UPDATE: chatGPT3.5 got upgraded to different context memory sizes and also improved _function calling_
        - For 8k tokens: 0.0015$/1k tokens. "chatGPT3.5-turbo16"
        - For 16k tokens: 0.003$/1k tokens.
        This implies that for some states of the system, the larger model should be used.
        Use case example: whenever trying to provide enough context for API descriptions of libraries, if the input requires more than x tokens, use model 
    - IMPORTANT: Save all interactions with timestamps to be previewed in the notebook.
    - Long-term memory for the controller:
        - This is an in-memory `SQLite` database driven by `SQLAlchemy` that stores:
            - Tables for each type of action that the system can perform:
                - [ ] `help` table: stores the functions that the system can perform.
                - [ ] `manipulation` table: stores the manipulation actions that the system can perform.
                - [ ] `navigation` table: stores the navigation actions that the system can perform.
                - [ ] `perception` table: stores the perception actions that the system can perform.
                - [ ] `planning` table: stores the planning actions that the system can perform.
                - [ ] `speech` table: stores the speech actions that the system can perform.
                - [ ] `vision` table: stores the vision actions that the system can perform.
            - Tables for each type of object that the system can interact with:
                - [ ] `objects` table: stores the objects that the system can interact with.
                - [ ] `object_attributes` table: stores the attributes of the objects that the system can interact with.
        - Long-term memory flushing to disk is either triggered by:
            - The user: can trigger flushing by saying "forget everything" or "forget the last thing I said".
            - The system can trigger flushing based on the `ATTENTION_SPAN` parameter found in the `config.py` file.
                - If the system is in an idle state, the system will flush the long-term memory.
                - If the `ATTENTION_SPAN` is set to a low value and a process is still happening during that period, the system will pause outside of a critical state and flush the long-term memory that is not related to the current process.
        - When long-term memory is flushed to disk any derivates of the tables are updated and processed.
            - ManipulationFunctions -> Manipulation.
            - PerceptionObjects -> ObjectBasedQuerryingWeights.
                - This table is used to determine the order in which the system should querry the objects.
                - When querrying, the system generates a table
        - The memorizing policy is as follows:
            - Check for each task used during the session if it has been completed and store a success value based on an equation calculated as follows:
                - `success = (number of times the task was completed) / (number of times the task was attempted)`
                Completion of a task is determined by the system checking if the goal predicates have been satisfied.
                - Extract a list of objects that have been used during the session.
                - For each task that involves an object, store an unique id for the object to avoid memory duplication.
                - For each task that was retreived from long-term memory, evaluate if the task was significantly more successful than previous values of the same function.
                    - If the task completion scores higher, replace it with the new task completion tree OR add the new task completion tree to the list of task completion trees.
                    - If the task completion scores lower, keep the old task completion tree so that in another run, the task will be rerun potentially scoring higher.
            - For all tasks completed, save each entry and sub-entry with a timestamp.

            - We compress the descriptions of the tasks that completed actions by removing the object names and replacing them with 'MASK'.
            - We compress the object separately by creating a table that stores an entry for each different object the same action has been done on.
                - Each entry has a list of all combinations of traits that the objects store.


    By compressing the vector representation, you can achieve more efficient storage and potentially faster processing without sacrificing the ability to find similar structures accurately. However, it's important to note that compression may involve a trade-off between storage size and information loss, as some compression techniques discard or approximate certain details of the original vector representation.
        
    - Short-term memory for the controller:
        - This is an in-memory `SQLite` database driven by `SQLAlchemy` that stores the most recent user inputs, system outputs, and other internal data.
        - Short-term memory flushing to long-term memory is either triggered by:
            - The user: can trigger flushing by saying "forget everything" or "forget the last thing I said".
            - The system can trigger flushing based on the `ATTENTION_SPAN` parameter found in the `config.py` file.
                - If the system is in an idle state, the system will flush the short-term memory.
                - If the `ATTENTION_SPAN` is set to a low value and a process is still happening during that period, the system will pause outside of a critical state and flush the short-term memory that is not related to the current process.

    - Querrying:
        - Functionality tables:
            - Types of querrying:
                - For long-term memory using `ManipulationCompressed` and `PerceptionCompressed` and `ReasoningCompressed` tables:
                    - Task summary querrying: Filter the set of all functions based on a slot-filled list of attributes that match the attributes extracted for the current task.
                        - Take the label assigned to the current task to branch down to the tables of either manipulation, perception, or reasoning.
                        - Slot fill the current task entries (entries differ based on the type of task) with either type that is given in the json template.
                        Slot fill json templates are stored in the prompts directory under the `slot-fills` folder.
                    The attributes of a task are:
                        -  
                    - Object based querrying: the system querries the long-term memory for objects that match the querry. 
                        - Check what object has been used the most for a certain function.
                        - Filter functionality based on the object attributes.
                        - For each object, the similarity of attributes is computed as follows:
                            - `similarity = (number of attributes known about current object to be interacted with) / (number of total possible attributes)`
                            - 
            - For manipulation and perception functions  in terms of access time can be improved by querrying the database in a different way.
            - For object based querrying, we compress a new table when saving information about # TODO: finish this
        - For example,
    
    - Make pipeline for refactoring functions
        - If a function exists that seems close to the one we expect to have, we call chatGPT to refactor it and then we deploy the function at runtime.
        - At the end of the function, determine if function should be stored in the long-term memory depending on the success rate of the goal predicates that it is used for.
    - Make pipeline for generating new functions
        - If there is no function that can be used askChatGPT to create an empty handler for the required function with all the information about it.
            - If the global variable `IS_CREATIVE` is set to 'True' in the `config.py` file, the function will be generated by chatGPT.
            - Else the function will be generated by a template and stored in long-term memory in the `help` table.
    - Make pipeline for generating new goals

6. Improvements
    - Make the system more safe to colaborate:
        - [ ] Parallelize the system so that it can run an event listener that processes input and handles `flag.PAUSE` or `flag.ABORT`.
        - [ ] Add a new label to each task which represents one of the following importance values:
            - `CRITICAL`        : the task is critical to the system and should not be interrupted.
            - `INTERRUPTIBLE`   : the task is not critical to the system and can be interrupted by special commands.
            - `LOOSE`           : the task is not critical to the system and can be interrupted by any command.
        - [ ] Make event handler based on the `flag` enum and importance values.
    - Fine-tune slot filling models to increase accuracy.
    - Port prompts from `.txt` to `.json` files.
        - [ ] Create a script that converts the `.txt` files to `.json` files.
        - [ ] Construct the table that stores the prompts in the database.
        - [ ] Add an entry in the notebook where the user can load/remove prompts.
        - [ ] Add a function that shows which prompts are mandatory to exist for the system to run.

