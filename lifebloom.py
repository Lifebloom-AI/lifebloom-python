import uuid
import logging


logger = logging.getLogger(__name__)

# To handle Exit errors that should not be hit but could be hit as we iterate MVP
def ExitHandlerError(Exception):
    pass


# Python function to call internally or use in FastAPI endpoint
def thread_completion(
    thread_input: dict,
    actions_context: list = [], # Can be empty on first completion
    thread_state: dict = {} # Can be empty on first completion
    ):
    
    if not thread_state:
        # Thread state is empty on first completion
        if actions_context:
            raise ValueError(f"actions_context should be empty on first thread completion: {actions_context}")
    
        # Initialize thread state
        thread_state = {
            "thread_id": uuid.uuid4(),
            "original_thread_input": thread_input,
            "previous_stage": None,
            "number_of_completions": 0
        }
        logger.debug(f"Initializing thread state:\n{thread_input}")
        
    
    return {}

# ...Lots more functions for auth, configurations, LLM chat completions, internal function calls to ontology, etc.
