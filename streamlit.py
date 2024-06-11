import asyncio
import json
import random
import time

from PIL import Image

import streamlit as st
from executor import WorkflowExecutor
from lifebloom import (execute_simulation, initialize_thread_state,
                       thread_completion)
from ontology import ontology

im = Image.open("favicon.ico")
logo = Image.open("lifebloom-colorlogo-whitetype.png")

st.set_page_config(
    page_icon=im,
    layout="wide",
    page_title="Lifebloom AI",
)

hide_streamlit_style = """
<style>
header {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display: none;}
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
    padding-left: 5rem;
    padding-right: 5rem;
}
[data-testid="stMetricValue"] {
    font-size: 24px;
}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)
header_col1, header_col2 = st.columns(2)


def initialize_state_variables():
    # Initialize st session state variables
    if "thread" not in st.session_state:
        st.session_state.thread = []

    if "selected_thread_state_id" not in st.session_state:
        st.session_state.selected_thread_state_id = ""

    if "thread_state_id_history" not in st.session_state:
        st.session_state.thread_state_id_history = {}

    if "current_scenario_name" not in st.session_state:
        st.session_state.current_scenario_name = ""

    if "current_persona_name" not in st.session_state:
        st.session_state.current_persona_name = ""

    if "current_workflow_name" not in st.session_state:
        st.session_state.current_workflow_name = ""

    if "ontology" not in st.session_state:
        st.session_state.ontology = ontology

    if "executor" not in st.session_state:
        st.session_state.executor = WorkflowExecutor()


initialize_state_variables()

# Setup the header columns
with header_col1:
    st.image(logo, width=300, output_format="png")

# Layout for chatbox and interaction box
col1, col2 = st.columns(2)

with col1:
    chatbox_container = st.container(border=False, height=740)
    chat_input = st.chat_input("Enter your message here...")

with col2:
    interaction_container = st.container(border=True, height=800)
    if (
        st.session_state.selected_thread_state_id
        in st.session_state.thread_state_id_history
    ):
        interaction_container.json(
            st.session_state.thread_state_id_history[
                st.session_state.selected_thread_state_id
            ]
        )


def select_thread_state(thread_state_id, *args):
    st.session_state.selected_thread_state_id = thread_state_id


async def simulate_scenario(workflow_name, scenario_name, persona_object):
    # GET SCENARIO DEFINITION
    scenario_defintion = st.session_state.ontology["examples"][scenario_name]

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


def trigger_scenario():

    persona_object = {"name": st.session_state.current_persona_name, "uid": "default"}
    scenario_name = st.session_state.current_scenario_name
    scenario_definition = st.session_state.ontology["examples"][scenario_name]
    workflow_name = st.session_state.current_workflow_name

    print(
        f"\nTest Scenario: {scenario_name}\n\nScenario details: {scenario_definition}\n\nInitial Input: {input}\n\nPersona: {persona_object['name']}\n"
    )

    final_thread_state = asyncio.run(
        simulate_scenario(workflow_name, scenario_name, persona_object)
    )

    for stage_run in final_thread_state["thread_history"]:
        completion = {
            "stage_name": stage_run["stage_name"],
            "thread_state_id": str(random.randint(1, 10000000)),
            "is_selected": False,
        }
        st.session_state.thread.append(completion)
        st.session_state.thread_state_id_history[completion["thread_state_id"]] = (
            stage_run
        )

    final_thread_completion = {
        "stage_name": "Scenario Completed",
        "thread_state_id": "final",
        "is_selected": False,
        "full_thread_state": final_thread_state,
    }

    st.session_state.thread.append(final_thread_completion)
    st.session_state.thread_state_id_history[
        final_thread_completion["thread_state_id"]
    ] = final_thread_completion


def get_stage_execution_box(thread_state_id: str, is_selected: bool):
    """
    "thread_state" = {
        "workflow_name": workflow_name,
        "persona": persona,
        "thread_id": uuid.uuid4(),
        "original_thread_input": initial_inputs,
        "additional_thread_input": []
        "number_of_completions": 0
    }

    "actions_context": [
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
            "response": {
            "user_response": "Because I found abc"
            }
        },
    ]
    """
    st.write(
        "Stage Name:",
        st.session_state.thread_state_id_history[thread_state_id]["stage_name"],
    )
    st.button(
        "More details",
        on_click=select_thread_state,
        args=[str(thread_state_id)],
        type="primary" if is_selected else "secondary",
        disabled=is_selected,
        key=thread_state_id,
    )


def show_scenario():
    st.session_state.selected_thread_state_id = ""
    interaction_container.json(
        st.session_state.ontology["examples"][st.session_state.current_scenario_name]
    )


def display_thread_chat():

    if not st.session_state.thread:

        with chatbox_container.chat_message("lifebloom", avatar="🌱"):

            all_workflows = st.session_state.ontology["workflows"]
            st.session_state.current_workflow_name = st.selectbox(
                "Select a Workflow", all_workflows.keys()
            )

            all_scenarios = st.session_state.ontology["examples"]
            all_scenario_names = all_scenarios.keys()
            st.session_state.current_scenario_name = st.selectbox(
                "Select a Scenario", all_scenario_names
            )

            all_personas = all_scenarios[st.session_state.current_scenario_name][
                "personae"
            ]
            st.session_state.current_persona_name = st.selectbox(
                "Select a Persona", all_personas
            )
            st.button("Run Scenario", on_click=trigger_scenario)
    else:
        with chatbox_container.chat_message("lifebloom", avatar="🌱"):
            st.write(f"Running Scenario: {st.session_state.current_scenario_name}")
            st.write(f"For Persona: {st.session_state.current_persona_name}")
            st.button("Show Scenario Details", on_click=show_scenario)

        # Display chat messages from history on app rerun
        for completion in st.session_state.thread:

            avatar = "🌱"
            with chatbox_container.chat_message("lifebloom", avatar=avatar):
                get_stage_execution_box(
                    thread_state_id=completion["thread_state_id"],
                    is_selected=completion["is_selected"],
                )


display_thread_chat()

### Button Functions


def start_over():
    st.session_state.thread = []
    chatbox_container.empty()
    st.session_state.selected_thread_state_id = ""


def show_ontology():
    st.session_state.selected_thread_state_id = ""
    interaction_container.json(st.session_state.ontology)


subheader_col1, subheader_col2, subheader_col3, subheader_col4 = header_col2.columns(
    [1, 2, 2, 2]
)

subheader_col1.button("Reset", on_click=start_over)
subheader_col2.button("View Ontology", on_click=show_ontology)
