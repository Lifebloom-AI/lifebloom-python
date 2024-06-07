import asyncio
import random
import time
import json

import streamlit as st
from PIL import Image

from ontology import ontology
from executor import WorkflowExecutor


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
    if st.session_state.selected_thread_state_id in st.session_state.thread_state_id_history:
        interaction_container.json(st.session_state.thread_state_id_history[st.session_state.selected_thread_state_id])
    

def select_thread_state(thread_state_id, *args):
    st.session_state.selected_thread_state_id = thread_state_id

    
def fake_execute(scenario):
    return {
            "thread_state":{
                "random1": random.randint(1, 100),
                "random2": random.randint(1, 100),
                "workflow_name": scenario["workflow_name"],
                },
            "actions_context": [str(i) for i in range(random.randint(1, 6))],
            }
            
def run_scenario():

    scenario_example = {}
    for scenario_iter in st.session_state.ontology["examples"]:
        if scenario_iter["scenario"]["short_description"] == st.session_state.current_scenario_name:
            scenario_example = scenario_iter["scenario"]
            break
        
    persona_example = {'name':ontology['examples'][0]['scenario']['personae'][0],'uid':"default"}
    
    # SCENARIO SHORT_DESCRIPTION
    short_description = scenario_example['short_description']

    # SCENARIO
    scenario = scenario_example['description']

    # INITIAL INPUT
    input = scenario_example['input']

    # PERSONA
    persona = persona_example
    
    # PERSONA DESCRIPTION
    persona_description = ontology['personae'][st.session_state.current_persona_name]['description']

    # PERSONA QUALITIES
    persona_qualities = ontology['personae'][st.session_state.current_persona_name]['preferences']
    
    print(f"Test Scenario: {short_description}\n\nScenario details: {scenario}\n\nInitial Input: {input}\n\nPersona: {st.session_state.current_persona_name}\n\nPersona Description: {persona_description}\n\nPersona Qualities: {persona_qualities}\n\n")
    
    output_dict, full_thread_output = asyncio.run(st.session_state.executor.run_workflow('security_finding_investigation', persona, input, mode='precision', scenario=scenario_example))
    
    
    for thread_run in full_thread_output:
        completion = {
            "title": thread_run["function_name"],
            "description": "",
            "thread_state_id": str(random.randint(1, 10000000)),
            "is_selected": False,
        }
        st.session_state.thread.append(completion)
        st.session_state.thread_state_id_history[completion["thread_state_id"]] = thread_run
    
    completion = {
            "title": "Final Recommendation",
            "description": "",
            "thread_state_id": "final",
            "is_selected": False,
        }
    
    st.session_state.thread.append(completion)
    st.session_state.thread_state_id_history["final"] = completion["content"] = output_dict
    

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
    st.write("Stage Name:", st.session_state.thread_state_id_history[thread_state_id]["function_name"])
    st.button("More details", on_click=select_thread_state, args=[str(thread_state_id)], type="primary" if is_selected else "secondary", disabled=is_selected, key=thread_state_id)


def show_scenario():
    st.session_state.selected_thread_state_id = ""
    scenerio_object = {}
    for obj in  st.session_state.ontology["examples"]:
        if obj["scenario"]["short_description"] == st.session_state.current_scenario_name:
            scenerio_object = obj
            break
    interaction_container.json(scenerio_object)

def display_thread_chat():
    
    if not st.session_state.thread:
        
        with chatbox_container.chat_message("lifebloom", avatar="🌱"):
            all_scenarios = st.session_state.ontology["examples"]
            
            all_scenario_names = [scenario["scenario"]["short_description"] for scenario in all_scenarios]
            
            st.session_state.current_scenario_name = st.selectbox("Select a Scenario", all_scenario_names)
            
            all_personas = []
            for scenario in all_scenarios:
                if scenario["scenario"]["short_description"] == st.session_state.current_scenario_name:
                    all_personas = scenario["scenario"]["personae"]
                    break

            st.session_state.current_persona_name = st.selectbox("Select a Persona", all_personas)
            st.button("Run Scenario", on_click=run_scenario)
        
    else:
        
        with chatbox_container.chat_message("lifebloom", avatar="🌱"):
            st.write(f"Running Scenario: {st.session_state.current_scenario_name}")
            st.write(f"For Persona: {st.session_state.current_persona_name}")
            st.button("Show Scenario Details", on_click=show_scenario)

        # Display chat messages from history on app rerun
        for completion in st.session_state.thread:
            
            avatar = "🌱"
            with chatbox_container.chat_message("lifebloom", avatar=avatar):
                if completion["thread_state_id"] != "final":
                    get_stage_execution_box(thread_state_id=completion["thread_state_id"], is_selected=completion["is_selected"])
                    
                else:
                    st.write("Final Recommendations")
                    st.button("Click here for more details", on_click=select_thread_state, args=["final"], type="primary" if completion["is_selected"] else "secondary", disabled=completion["is_selected"], key="final")


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