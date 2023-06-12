# Path to database (default: ./db.sqlite3)
LONG_MEM_URL = 'sqlite:///:memory:' 
SHORT_MEM_URL = 'sqlite:///memory.db'


# API configuration
OPENAI_API_KEY = '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'
CHATGPT_MODEL = 'gpt-3.5-turbo'

# Whether to let chatGPT generate its own environments based on context provided by user
SELF_TRAIN = False 

# Used in SELF_TRAIN mode, to determine if, once reaching the idle state, the environment should be reset or not
PERSISTENT_ENVIRONMENTS = False

# TOKEN_LIMIT: Maximum number of tokens to use in one run of SELF_TRAIN mode
# If the number of tokens exceeds this limit, the machine will memorize its output and close.
# This is not a hard limit, but rather a soft one, as the machine will try to finish its current task set before closing.
TOKEN_LIMIT = 100000

# Number of retries if a completion fails (eg. wrong/broken format) (default: 3)
RETRIES_TO_ABORT='3'

# Path to prompt files (default: ./prompts/)
PROMPT_PATH = './prompts/'
