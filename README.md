## GPT Controller

This python project is meant to integrate chatGPT in the process of controlling a robot in order to achieve zero-shot planning and control. The project is part of my bachelor's thesis.

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

3. Install project dependencies:

```bash
poetry install
```

4. Configure project:

    Open the `config.py` file in the root directory and fill all the entries with the required information.

## Usage
To run the project, execute the following command:

```bash
poetry run python -m run.py
```

Upon running, you will be prompted to enter a message. After entering a message, the program will generate a response and print it to the console.
You have access to utility functions in order to get a view on the knowledge of the system as well as other information about the system.
To access them you can type `--help` in the console and you will be presented with a list of available commands.

## Evaluation
The evaluation of the system's performance is done within the manual.ipynb notebook. The notebook contains a set of tests that can be run in order to evaluate the system's prompting accuracy, conversation length and other metrics.

