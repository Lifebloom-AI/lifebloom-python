"""
Definitions:

Workflow: The definition of the stages, its exit conditions, and function calls
Thread: The process of using a workflow to resolve a use case


Example thread:

                New Alert
                    |
              First Completion
             |       |        |
         action_1    |     action_3 --> e.g Grab data from external API
             |    action_2    |
             |       |        |
              Second Completion
              |               |
          action_4          action_5 --> e.g Message user
              |               |
              |               |
              Third Completion
                      |
                  action_6
                      |
                     exit


Here, an action could be external calls to get more information or ask a user a question and await answer.
All actions need to be completed before calling the next completion.
For example: action_1, action_2, action_3 needs to be completed before calling "Second Completetion" with the response from all the actions

There are N number of completions that could happen dynamically based on the context and exit criteria for a playbook. Could be as long as 15 completions (Need to be capped).

Each completion is a "stage" where there are multiple internal calls (LLM + static functions) on Lifebloom's codebase occur.
Each stage composes of an "input" and "output" where "output" is some action that lifebloom's code cannot take, e.g external API calls to grab data or message user.

Once the responses are gather from all the actions, add the responses to the input of the next completion call.
Think of the "workflow_completion" function similar to the "chat_completion" in OpenAI SDK in how you interact.

The thread will complete when the completion outputs "exit: True". Execute the last outputted actions and stop the completetions going forward.
The actions when exit=True could be unique:
For example, an action could be ESCALATE_TO_OPERATOR because a human is required either due to user not coperating or maxed out on retries without resolving the issue
"""

### Random functions for placeholder

def get_latest_alert():
    return {
        "id": "123",
        "security_findings": "SQL Injection",
        "findings_context": "User tried to login with SQL Injection",
        "user_id": "user_123"
    }

def get_relevant_alert_ids(alert_id):
    return ["123", "124", "125"]

def get_user_role(user_id):
    return "admin"

def async_execute_actions(actions):
    return {
        "action_1": "response1",
        "action_2": "response2",
        "action_3": "response3"
    }


### YOUR PRODUCT'S CODE

from lifebloom import workflow_completion, ExitHandlerError


# THREAD EXAMPLE FROM ABOVE

# This can be a push API endpoint to trigger this code (should be a function). Just sake of example, this is a pull
alert = get_latest_alert()

original_alert_id = alert["id"]
security_findings = alert["security_findings"]
findings_context = alert["findings_context"]
relevant_alert_ids = get_relevant_alert_ids(alert_id=alert["id"]) # This can become more sophisticated + become a stage of its own later
persona = get_user_role(user_id=alert["user_id"])

thread_input = {
    "original_alert_id": original_alert_id,
    "security_findings": security_findings,
    "findings_context": findings_context,
    "relevant_alert_ids": relevant_alert_ids,
    "persona": persona
}

actions_context = {}
thread_state = {}
met_exit_condition = False

# Just in case exit is not handled well (Should not hit be hit, but just in case)
max_loop = 20
loop_counter = 0

# This could technically be a for loop, but keeping it while loop for when we get rid of loop_counter later
while not met_exit_condition:

  completion_res = workflow_completion(
      thread_input=thread_input,
      actions_context=actions_context,
      thread_state=thread_state
  )

  actions_context = async_execute_actions(completion_res["actions"]) # Should async parallel execute actions
  thread_state = completion_res["thread_state"]

  """
  To execute linearly:

  actions_res = []
  for action in actions_to_take:
    res = execute_action(action)
    actions_res.append(res)
  """

  if completion_res["exit"] is True:
    met_exit_condition = True # This thread is now completed and process will end
  elif loop_counter >= max_loop:
    raise ExitHandlerError("Exit not handled gracefully. Escalate to an operator") # Just in case exit is not handled well. Catch this exception and have human step in
  else:
    loop_counter+=1




# Example completions input

input = {
  "thread_input": {
    "original_alert_id" : "123_abc",
    "security_findings" : {...},
    "findings_context" : {...},
    "relevant_alert_ids": {...}, # Other alerts from this user / is relevent
    "persona": "example_marketing_analyst"
    },

  "actions_context": [
    # This is empty on first completion. If there are items, they are responses from a previous stage's action guidance
    {
      "action_name": "GET_USER_LAST_LOGIN",
      "args": {
        "user_id": "123xyz",
        "timeframe_hours": 24
      },
      "response": {
          "last_login_epoch": "2024-05-25T21:37:04"
      }
    },
    {
        "action_name": "MESSAGE_TO_USER_AWAIT",
        "args": {
          "message_body": "Why did you do xyz?",
          "wait_limit_hours": 48
        },
        "response": "Because I found abc"
    },
  ],
  "thread_state": {...} # Empty on first completion. Only used for keeping workflow state, no need to read or modify.
}



# Example completions output

output = {
  "actions": [
    {
      "action_name": "GET_USER_LAST_LOGIN",
      "args": {
        "user_id": "123xyz",
        "timeframe_hours": 24
      }
    },
    {
      "action_name": "MESSAGE_TO_USER_AWAIT",
      "args": {
        "message_body": "What is the answer to xyz?",
        "wait_limit_hours": 48
      }
    },
    {
      "action_name": "RESTART_SERVER",
      "args": {
        "server_id": "i-54fdsafd",
      }
    }
  ],
  "exit": True | False,
  "thread_state": {...}, # Memorize and pass to next call in thread
}

# List of actions that can happen when exit is True.
exit_actions = [
    "ESCALATE_TO_OPERATOR",
    "MESSAGE_USER",
    "NO_ACTION"
    # +all external calls for clean up if needed
]