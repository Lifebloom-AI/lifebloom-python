import asyncio
import json
import logging
import uuid
from typing import Dict, List

from executor import WorkflowExecutor
from prompt import AISDKPrompt, PromptMessage

logger = logging.getLogger(__name__)


# To handle Exit errors that should not be hit but could be hit as we iterate MVP
def ExitHandlerError(Exception):
    pass


# Python function to call internally or use in FastAPI endpoint
async def thread_completion(thread_state: dict, actions_response: List[Dict] = []):

    print("\n\nACTION RESPONSES: ", actions_response)

    # Initialize the workflow executor
    workflow_executor = WorkflowExecutor()

    # Add the actions response to the workflow executor
    new_actions_context = list(thread_state["actions_context"])
    for action_response in actions_response:
        new_actions_context.append(action_response)

    thread_state["actions_context"] = new_actions_context

    MAX_INTERNAL_COMPLETIONS = 20
    current_completion_i = 0

    # Continously loop through the internal completions until an external action needs to be taken
    while current_completion_i <= MAX_INTERNAL_COMPLETIONS:
        actions_to_take, thread_state = (
            await workflow_executor.internal_thread_completion(thread_state)
        )
        if actions_to_take or thread_state["is_exit"]:
            return actions_to_take, thread_state
        else:
            current_completion_i += 1

    raise ExitHandlerError(
        "Internal completions exceeded the maximum number of completions allowed."
    )


# ...Lots more functions for auth, configurations, LLM chat completions, internal function calls to ontology, etc.


def initialize_thread_state(
    thread_input: dict,
    workflow_name: str,
    mode: str = "precision",
    persona_object: dict = None,
) -> dict:
    """
    Intialize thread state for a new thread.

    Original input is the input that the user provided to start the thread. It can be in any format.
    """
    if mode not in ("precision", "speed", "training"):
        raise ValueError(
            f"mode should be one of 'precision', 'speed', 'training': {mode}"
        )

    if not persona_object:
        persona_object["name"] = "default"
        persona_object["uid"] = "default"

    new_thread_state = {
        "thread_id": str(uuid.uuid4()),
        "original_thread_input": thread_input,
        "previous_stage_index": None,
        "number_of_completions": 0,
        "mode": mode,
        "persona_object": persona_object,
        "next_stage_index": 0,
        "workflow_name": workflow_name,
        "thread_history": [],
        "actions_context": [],
        "is_exit": False,
        "exit_output": None,
    }

    return new_thread_state


async def execute_simulation(
    scenario_definition,
    original_input,
    actions_context,
    action,
    actions_path="function.action",
):
    workflow_executor = WorkflowExecutor()

    scenario = scenario_definition["description"]

    try:
        print("SIMULATING ACTION: ", [action["action"]])
        attribute_filter = {"name": [action["action"]]}
        action_attributes = workflow_executor.filter_taxonomy_objects(
            workflow_executor.ontology, actions_path, attribute_filter
        )[0]
        action_attributes["name"] = action_attributes["name"].replace(" ", "_")
        # print(action_attributes)

        # get_item_attributes(data=ontology, target=actions_path)[action['action']]

        system_prompt = "You are a simulation example generator who focuses on high-quality, authentic example generation based on the scenario description and the current context."

        user_prompt = f"""Given this specific scenario, defined as: {scenario}\n\nYou have the current context so far: {original_input} {actions_context}
    Generate an authentic response from this action: {action}, described as {action_attributes["description"]}.
    The action has this output schema for a response: {str(action_attributes['output'])}.

    Your output response should be a simulated example of the response of the use of the function. It should return results consistent with the described scenario and the description of what the action does.
    The described action is effectively an API call which will be executed, and your simulated response will provide a very thoughtful example of what would return from that API call.

    Explain how the response to this API call would look given the scenario and current context. Describe how you can make this authentic as it pertains to the expected data which would be returned as a real response, explain how the details connect to the overall scenario, and the existing context."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        messages = [
            PromptMessage(role="system", content=system_prompt),
            PromptMessage(role="user", content=user_prompt),
        ]

        chat_response = await workflow_executor.prompt_client.execute_prompt(
            AISDKPrompt(messages=messages)
        )

        # completion
        tools_to_use = [
            {
                "type": "function",
                "function": {
                    "name": action_attributes["name"],
                    "description": action_attributes["description"],
                    "parameters": action_attributes["output"],
                },
            }
        ]
        tool_choice = {
            "type": "function",
            "function": {"name": action_attributes["name"]},
        }
        # print(tools_to_use)

        system_prompt += "\n You provide responses in JSON format consistent with the schema the function would provide."

        messages = [
            PromptMessage(role="system", content=system_prompt),
            PromptMessage(role="user", content=user_prompt),
            PromptMessage(role="assistant", content=chat_response["message"].content),
            PromptMessage(
                role="user",
                content="Now write the response you have described into the JSON format provided.",
            ),
        ]

        chat_response = await workflow_executor.prompt_client.execute_prompt(
            AISDKPrompt(messages=messages, tools=tools_to_use, tool_choice=tool_choice)
        )

        action_result = json.loads(
            chat_response["message"].tool_calls[0].function.arguments
        )

        action["action_result"] = action_result
    except:  # Action doesn't exist, simulation failure
        action["action_result"] = "Failure"

    return action


async def simulate_scenario(workflow_name, scenario_name, persona_object):
    # GET SCENARIO DEFINITION
    ### YOU WOULD NOT NEED THIS
    workflow_executor = WorkflowExecutor()
    scenario_defintion = workflow_executor.ontology["examples"][scenario_name]

    # INTIALIZE THREAD STATE
    thread_state = initialize_thread_state(
        thread_input=scenario_defintion["input"],
        workflow_name=workflow_name,
        mode="precision",
        persona_object=persona_object,
    )

    actions_response = []
    exit_condition_met = False

    while exit_condition_met is False:
        actions, thread_state = await thread_completion(thread_state, actions_response)
        exit_condition_met = thread_state["is_exit"]

        routines = []
        for action in actions:
            print("\n\nSIMULATING ACTION: ", action)
            routines.append(
                execute_simulation(
                    scenario_defintion,
                    thread_state["original_thread_input"],
                    thread_state["actions_context"],
                    dict(action),
                )
            )
        actions_response = await asyncio.gather(*routines)

    return thread_state
