class CompletionError(Exception):
    """Raised when a completion request fails.

    Attributes:
        prompt -- input prompt which caused the error
        error -- explanation of the error
    """

    def __init__(self, prompt, response):
        message = "Processing '{}' failed.\n Output: {}".format(prompt, response)
        super().__init__(message)

class ParsingError(Exception):
    """Raised when a completion request fails.

    Attributes:
        from_type -- input type
        to_type -- expected output type
    """

    def __init__(self, from_type, to_type):
        message = "Parsing from {} to {} failed.".format(from_type, to_type)
        super().__init__(message)

class PromptingError(Exception):
    "Raised when the user input fails."

    def __init__(self, file_name, file_path):
        message = "'{}' on path '{}' doesn't exist.".format(file_name, file_path)
        super().__init__(message)
    
    def __init__(self, file_name):
        message = "'{}' does not end with .txt".format(file_name)
        super().__init__(message)
