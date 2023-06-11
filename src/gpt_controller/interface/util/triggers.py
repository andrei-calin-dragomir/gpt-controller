class UserInputTrigger(Exception):
    """Raised when a completion request fails.

    Attributes:
        from_type -- input type
        to_type -- expected output type
    """

    def __init__(self, label):
        message = "An input of type {} was received.".format(label)
        print(message)