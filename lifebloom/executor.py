### V2 Ontology Build Script

import asyncio
import json

from ontology import ontology
from prompt import AISDKPrompt, ModelCompletion, PromptMessage


class WorkflowExecutor:

    def __init__(self):
        self.ontology = ontology
        self.prompt_client = ModelCompletion()

    def get_item_attributes(self, ontology_subset: dict, location: str):
        """
        Get all attributes of the subset defined in the ontology. The subset could be the whole Ontology itself
        """
        path_parts = location.split(".")
        segment = ontology_subset
        for part in path_parts:
            segment = segment[part]
        return segment

    def filter_taxonomy_objects(self, ontology_subset, location, attribute_filter):
        """

        location = 'functions.native'
        attribute_filter = {
            'disabled': [0],
            'impact': None,
            'name': ['Get Alert Analytics'],
            'service': None,
            'type': None,
            'input': None,
            'output': None
        }

        """
        matching_taxonomy_objects = []
        ontology_branch = self.get_item_attributes(ontology_subset, location)
        for obj in ontology_branch:
            keep = True
            for attribute in attribute_filter:
                if attribute_filter[attribute]:
                    if obj[attribute] not in attribute_filter[attribute]:
                        keep = False
            if keep:
                matching_taxonomy_objects.append(obj)
        return matching_taxonomy_objects

    async def execute_inference_function(
        self,
        function_definition: dict,
        function_input: dict,
        persona_object: dict,
        mode: str,
    ):

        function_name = function_definition["name"]

        # GET INFERENCE FUNCTION DEFINITION FROM ONTOLOGY

        # print(function_definition['prompt'])
        # SYSTEM
        system = function_definition["prompt"]["system"]["value"]

        # COGNITION
        cognition = function_definition["prompt"]["cognition"]["value"]

        persona = persona_object

        # IF PERSONA IS NOT DEFAULT, SET DEFAULT CONFIGS
        if persona["name"] != "default":
            system = ontology["personae"][persona["name"]]["functions"][function_name][
                "default"
            ]["system"]
            cognition = ontology["personae"][persona["name"]]["functions"][
                function_name
            ]["default"]["cognition"]

            # IF PERSONA UID IS DEFINED IN PERSONAE TAXONOMY FOR THIS FUNCTION
            if (
                persona["uid"]
                in ontology["personae"][persona["name"]]["functions"][function_name]
            ):

                # IF PERSONA UID FOR THIS FUNCTION HAS SYSTEM
                if (
                    ontology["personae"][persona["name"]]["functions"][function_name][
                        persona["uid"]
                    ]["system"]
                    != ""
                ):
                    system = ontology["personae"][persona["name"]]["functions"][
                        function_name
                    ]["default"]["system"]

                # IF PERSONA UID FOR THIS FUNCTION HAS COGNITION
                if (
                    ontology["personae"][persona["name"]]["functions"][function_name][
                        persona["uid"]
                    ]["cognition"]
                    != ""
                ):
                    cognition = ontology["personae"][persona["name"]]["functions"][
                        function_name
                    ]["default"]["cognition"]

        # CONTEXT
        context_attributes = function_definition["prompt"]["context"]["attributes"]
        context_dict = {attr: function_input[attr] for attr in context_attributes}
        context = function_definition["prompt"]["context"]["value"].format(
            **context_dict
        )

        # INSTRUCTIONS
        instructions_attributes = function_definition["prompt"]["instructions"][
            "attributes"
        ]
        instructions_dict = {
            attr: function_input[attr] for attr in instructions_attributes
        }
        instructions = function_definition["prompt"]["instructions"]["value"].format(
            **instructions_dict
        )

        # DYNAMIC STRUCTURED OUTPUT
        dynamic_structured_outputs = function_definition.get(
            "dynamic_structured_outputs", {}
        )

        # REFERENTIAL DYNAMIC OUTPUTS
        referential_outputs = dynamic_structured_outputs.get("referential", [])
        for dynamic_config in referential_outputs:

            # COLLECT IN-SCOPE REFERENCES
            options = self.filter_taxonomy_objects(
                self.ontology,
                dynamic_config["ontology_path"],
                dynamic_config["filter_attributes"],
            )

            # SET ATTRIBUTES
            fetch_attributes = dynamic_config["fetch_attributes"]
            output_schema_description = {}
            output_enums = []

            # GET ALL NAMES, ATTRIBUTES
            for option in options:
                output_schema_description[option["name"]] = {}
                output_enums.append(option["name"])
                for attribute in fetch_attributes:
                    output_schema_description[option["name"]][attribute] = option[
                        attribute
                    ]

            # SET STRUCTURED OUTPUTS IN FUNCTION_DEFINITION
            path_parts = dynamic_config["output_enum_path"].split(".")
            segment = function_definition["output"]
            for part in path_parts[:-1]:
                segment = segment[part]

            if len(output_enums) > 0:
                segment[path_parts[-1]]["enum"] = output_enums
                segment[path_parts[-1]]["description"] += (
                    "\n"
                    + f"This is the JSON dictionary which contains the different choices and the attributes which describe them. {str(output_schema_description)}"
                )

        # INPUT-BASED DYNAMIC OUTPUTS
        # THIS TAKES IN A DICTIONARY ARGUMENT AND FORMATS IT
        input_outputs = dynamic_structured_outputs.get("input", [])
        for dynamic_config in input_outputs:

            # COLLECT IN-SCOPE REFERENCES
            options = self.filter_taxonomy_objects(
                function_input,
                dynamic_config["input_argument_path"],
                dynamic_config["filter_attributes"],
            )

            # SET ATTRIBUTES
            fetch_attributes = dynamic_config["fetch_attributes"]
            output_schema_description = {}
            output_enums = []

            # GET ALL NAMES, ATTRIBUTES
            for option in options:
                if type(option) is list:
                    output_enums.append(option)
                    output_schema_description[option] = {}
                if type(option) is dict:
                    output_enums.append(option["name"])
                    output_schema_description[option["name"]] = {}
                else:
                    output_schema_description = {}

                for attribute in fetch_attributes:
                    output_schema_description[option["name"]][attribute] = option[
                        attribute
                    ]

            # SET STRUCTURED OUTPUTS IN FUNCTION_DEFINITION
            path_parts = dynamic_config["output_enum_path"].split(".")
            segment = function_definition["output"]
            for part in path_parts[:-1]:
                segment = segment[part]
            if len(output_enums) > 0:
                segment[path_parts[-1]]["enum"] = output_enums
                segment[path_parts[-1]]["description"] += (
                    "\n"
                    + f"This is the JSON dictionary which contains the different choices and the attributes which describe them. {str(output_schema_description)}"
                )

        # SET STRUCTURED OUTPUT DEFINITION, TOOLS
        output = function_definition["output"]

        tools_to_use = [
            {
                "type": "function",
                "function": {
                    "name": function_name,
                    "description": function_definition["description"],
                    "parameters": output,
                },
            }
        ]

        tool_choice = {"type": "function", "function": {"name": function_name}}

        # IF MODE IS SPEED, SKIP COGNITION
        if mode == "speed":
            # PAYLOAD TO COMPLETION ENDPOINT
            system_prompt = (
                system + "\nWrite your response in the JSON format provided."
            )
            user_prompt = context + "\n" + instructions
            messages = [
                PromptMessage(role="system", content=system_prompt),
                PromptMessage(role="user", content=user_prompt),
            ]

            chat_response = await self.prompt_client.execute_prompt(
                AISDKPrompt(
                    messages=messages, tools=tools_to_use, tool_choice=tool_choice
                )
            )
            return chat_response

        # IF MODE IS PRECISION, DO COGNITION CHAIN
        elif mode == "precision":

            # COGNITION PAYLOAD TO COMPLETION ENDPOINT
            system_prompt = system
            user_prompt = context + "\n" + cognition
            messages = [
                PromptMessage(role="system", content=system_prompt),
                PromptMessage(role="user", content=user_prompt),
            ]

            chat_response = await self.prompt_client.execute_prompt(
                AISDKPrompt(messages=messages)
            )

            cognition = chat_response["message"].content

            # STRUCTURED PAYLOAD TO COMPLETION ENDPOINT
            system_prompt = (
                system + "\nWrite your response in the JSON format provided."
            )

            messages = [
                PromptMessage(role="system", content=system_prompt),
                PromptMessage(role="user", content=user_prompt),
                PromptMessage(role="assistant", content=cognition),
                PromptMessage(role="user", content=instructions),
            ]

            chat_response = await self.prompt_client.execute_prompt(
                AISDKPrompt(
                    messages=messages, tools=tools_to_use, tool_choice=tool_choice
                )
            )
            return chat_response

        # IF MODE IS TRAINING, DO COGNITION CHAIN AND EXPLANATION CHAIN
        elif mode == "training":

            # COGNITION PAYLOAD TO COMPLETION ENDPOINT
            system_prompt = system
            user_prompt = context + "\n" + cognition

            messages = [
                PromptMessage(role="system", content=system),
                PromptMessage(role="user", content=user_prompt),
            ]

            chat_response = await self.prompt_client.execute_prompt(
                AISDKPrompt(messages=messages)
            )
            cognition = chat_response["message"].content

            # STRUCTURED PAYLOAD TO COMPLETION ENDPOINT
            system_prompt = (
                system + "\nWrite your response in the JSON format provided."
            )
            messages = [
                PromptMessage(role="system", content=system_prompt),
                PromptMessage(role="user", content=user_prompt),
                PromptMessage(role="assistant", content=cognition),
                PromptMessage(role="user", content=instructions),
            ]
            chat_response = await self.prompt_client.execute_prompt(
                AISDKPrompt(
                    messages=messages, tools=tools_to_use, tool_choice=tool_choice
                )
            )

            completion = json.loads(
                chat_response["message"].tool_calls[0].function.arguments
            )

            # STRUCTURED PAYLOAD TO COMPLETION ENDPOINT
            system_prompt = system

            messages = [
                PromptMessage(role="system", content=system_prompt),
                PromptMessage(role="user", content=user_prompt),
                PromptMessage(role="assistant", content=cognition),
                PromptMessage(role="user", content=instructions),
                PromptMessage(role="assistant", content=cognition),
                PromptMessage(role="user", content="Explain your answer."),
            ]

            chat_response = await self.prompt_client.execute_prompt(
                AISDKPrompt(messages=messages)
            )

            explanation = chat_response["message"].content

            completion[function_name + "_details"] = {
                "cognition": cognition,
                "explanation": explanation,
            }
            return completion

        else:
            raise ValueError(
                f"mode should be one of 'precision', 'speed', 'training': {mode}"
            )

    async def internal_thread_completion(self, thread_state):
        # UNPACK VARIABLES FROM THREAD STATE
        workflow = self.ontology["workflows"][thread_state["workflow_name"]]

        stage_input = thread_state["original_thread_input"].copy()
        stage_input["actions_context"] = thread_state["actions_context"]

        # EXECUTE NEXT STAGE
        stage_metadata = await self.execute_stage(
            workflow_name=thread_state["workflow_name"],
            stage_name=workflow["stages"][thread_state["next_stage_index"]]["name"],
            stage_input=stage_input,
            persona_object=thread_state["persona_object"],
            mode=thread_state["mode"],
            current_stage_index=thread_state["next_stage_index"],
        )

        filtered_actions = []
        # CHECK TO SEE IF ACTIONS HAVE ALREADY RUN
        if "actions_context" in stage_metadata["stage_output"]:
            for action in stage_metadata["stage_output"]["actions_context"]:
                if action not in thread_state["actions_context"]:
                    filtered_actions.append(action)

        # EXECUTE STAGE ROUTER
        await self.execute_stage_router(thread_state, stage_metadata)
        # This modifies the stage_metadata's next_stage_index in place


        # STORE THREAD HISTORY
        thread_state["thread_history"].append(stage_metadata)
        thread_state["next_stage_index"] = stage_metadata["next_stage_index"]
        thread_state["number_of_completions"] += 1

        if stage_metadata["is_exit"]:
            thread_state["is_exit"] = True
            thread_state["exit_output"] = stage_metadata["stage_output"]

        # OR RETURN ACTIONS TO EXECUTE
        return filtered_actions, thread_state

    async def execute_stage(
        self,
        workflow_name,
        stage_name,
        stage_input,
        persona_object,
        mode,
        current_stage_index,
    ):

        # TODO: INPUT VALIDATOR
        # TODO: IF INPUT IS NOT VALID, RETURN WITH STAGE ROUTER TO ANOTHER STAGE

        print(f"\n\nEXECUTING STAGE: {stage_name}")
        print(f"\n\nSTAGE INPUT: {stage_input}")
        filtered_taxonomy = self.filter_taxonomy_objects(
            self.ontology, "function.inference", {"name": stage_name}
        )
        function_definition = filtered_taxonomy[0]

        inference_response = await self.execute_inference_function(
            function_definition, stage_input, persona_object, mode
        )

        stage_metadata = {
            "stage_name": stage_name,
            "stage_input": stage_input,
            "persona_object": persona_object,
            "mode": mode,
            "is_exit": False,
        }

        actions_to_run = []

        stage_metadata["stage_output"] = json.loads(
            inference_response["message"].tool_calls[0].function.arguments
        )

        print("\n\nINFERENCE RESPONSE FROM STAGE: ", inference_response)
        print("\n\nACTIONS TO RUN FROM EXECUTE STAGE: ", actions_to_run)

        # TODO: STAGE ROUTER TO DETERMINE NEXT STAGE
        # TEMP INCREASE BY ONE AND EXIT CONDITION IS WHEN IT HITS END OF THE WORKFLOW
        stage_metadata["next_stage_index"] = current_stage_index + 1
        if stage_metadata["next_stage_index"] >= len(
            self.ontology["workflows"][workflow_name]["stages"]
        ):
            stage_metadata["is_exit"] = True

        return stage_metadata

    async def execute_stage_router(self, thread_state: dict, stage_metadata: dict) -> None:
        # STAGE ROUTER EXECUTION
        workflow = self.ontology["workflows"][thread_state["workflow_name"]]
        # WORKFLOW_NAME
        workflow_name = thread_state["workflow_name"]
        DEFAULT_MAX_RUNS = 5
        stage = workflow["stages"][thread_state["next_stage_index"]]
        stage_index = thread_state["next_stage_index"]

        # GET STAGE_ROUTER CONFIGS
        loopback_condition = stage['stage_router'].get('loopback_condition',False)
        max_runs = stage['stage_router'].get('max_runs', DEFAULT_MAX_RUNS)
        loopback_stages = stage['stage_router'].get('loopback_stages', [])

        # ADD NEXT STAGE, IF EXISTS
        if stage_index != len(workflow["stages"]) and stage_index not in loopback_stages:
            loopback_stages.append(stage_index)

        # VERIFY THREAD HAS NOT HAD MORE THAN MAX_RUNS OF THIS STAGE
        # COUNT STAGE RUNS
        stage_runs = 0
        for state in thread_state["thread_history"]:
            if stage['name'] == state['stage_name']:
                stage_runs += 1

        # CHECK TO SEE IF WE SHOULD RUN STAGE ROUTER
        if loopback_condition and stage_runs <= max_runs:
            
            # CREATE STAGE_CHOICES INPUT VARIABLE
            stage_choices = []

            # FROM ALL ELLIGIBLE LOOPBACK STAGES
            for loopback_stage_index in loopback_stages:

                # GET THE INFERENCE FUNCTION CONFIG
                for inference_function in ontology['function']['inference']:
                    if inference_function['name'] == ontology['workflows'][workflow_name]['stages'][loopback_stage_index]['name']:

                        # ADD TO STAGE_CHOICES NAME/DESCRIPTION VALUES
                        stage_choices.append({'name':inference_function['name'], 'description': inference_function['description']})
        
            # CREATE WORKFLOW_DEFINITION INPUT VARIABLE
            workflow_definition = {
                'name': workflow_name,
                'description': ontology['workflows'][workflow_name].get('description',''),
                'input': ontology['workflows'][workflow_name].get('input', ''),
                'stages': [],
                'output': ontology['workflows'][workflow_name].get('output','')
            }

            # GET INFERENCE FUNCTION CONFIG FOR EACH STAGE
            for config_stage in ontology['workflows'][workflow_name]['stages']:
                for inference_function in ontology['function']['inference']:
                    if inference_function['name'] == config_stage['name']:
                        workflow_definition['stages'].append({
                            'name': inference_function['name'],
                            'input': inference_function['input'],
                            'output': inference_function['output'],
                            'description': inference_function['description']
                            })
                        # print("Workflow Definition\n",workflow_definition)

            # CREATE CURRENT_CONTEXT INPUT VARIABLE
            current_context = ''

            # READ THROUGH ALL OF THREAD, PULLING NAME/INPUT/OUTPUT
            for state_index in range(len(thread_state["thread_history"])):
                state = thread_state["thread_history"][state_index]
                historical_stage_name = state['stage_name']
                historical_stage_input = state["stage_input"]
                historical_stage_output = state['stage_output']
                current_context += f'Step {str(state_index)}:\nStage executed: {historical_stage_name}\nInput to the stage: {historical_stage_input}\nOutput from the stage: {historical_stage_output}\n\n'
            
            # EXECUTE STAGE ROUTER
            stage_router_function_definition = self.filter_taxonomy_objects(
            self.ontology, "function.inference", {"name": 'stage_router'}
            )[0]
            stage_router_input = {'workflow_definition': workflow_definition, 'current_context': current_context, 'stage_choices': stage_choices}
            stage_router_response = await self.execute_inference_function(
                    stage_router_function_definition, stage_router_input, {'name':'default','uid':'-1'}, thread_state['mode']
                )
            
            # SET NEXT STAGE INDEX FROM RESPONSE
            stage_router_choice =  json.loads(stage_router_response["message"].tool_calls[0].function.arguments).get('next_stage', '')
            
            for stage_option_index in range(len(workflow["stages"])):
                if workflow["stages"][stage_option_index]['name'] == stage_router_choice:
                    stage_metadata["next_stage_index"] = stage_option_index
                    break