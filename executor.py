### V2 Ontology Build Script

from openai import OpenAI
from prompt import ModelCompletion, PromptMessage, AISDKPrompt
import json


class WorkflowExecutor:
    
    def __init__(self):
        pass
        self.ontology = {}
        self.prompt_client = ModelCompletion()
    
    
    def get_item_attributes(self, ontology_location: str):
        path_parts = ontology_location.split('.')
        segment = self.ontology
        for part in path_parts:
            segment = segment[part]
        return segment
    

    def filter_taxonomy_objects(self, attribute_filter, ontology_location='functions.native'):
        """
        
        ontology_location = 'functions.native'
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
        ontology_branch = self.get_item_attributes(ontology_location)
        for obj in ontology_branch:
            keep = True
            for attribute in attribute_filter:
                if attribute_filter[attribute]:
                    if obj[attribute] not in attribute_filter[attribute]:
                        keep = False
            if keep:
                matching_taxonomy_objects.append(obj)
        return matching_taxonomy_objects
    
    
    async def execute_inference_task(self, function_context):
        # FUNCTION_CONTEXT: INPUT_DATA, MODE, FUNCTION_NAME, PERSONA

        # UNPACK VARS
        input_data = function_context['input']
        mode = function_context['mode']
        function_name = function_context['function_name']

        # GET INFERENCE FUNCTION DEFINITION FROM ONTOLOGY
        function_definition = self.filter_taxonomy_objects('function.inference',{'name':function_name})

        # IF PERSONA, SET CONFIGS
        if 'persona' in function_context:
            persona = function_context['persona']

            # IF DEFAULT PERSONA, SET AS FUNCTION_DEFINITION
            if persona['name'] == 'default':
                function_definition = self.filter_taxonomy_objects('function.inference',{'name':function_name})

            # ELSE SET FUNCTION_DEFINITION BY PREFERENCE
            else:
                # SETTING THIS FOR NOW SINCE PERSONA NOT SETUP
                function_definition = self.filter_taxonomy_objects('function.inference',{'name':function_name})

                # GET PERSONA, UID CONFIGS
                # PRECEDENCE: GET UID CONFIGS, THEN PERSONA, THEN DEFAULT
                # GET UID CONFIGS
                # IF ANY KEYS EMPTY, GET PERSONA CONFIGS
                # IF ANY KEYS EMPTY, GET DEFAULT CONFIGS

        # SYSTEM PROMPT
        system_prompt = function_definition['prompt']['system']['value']

        # CONTEXT
        context_attributes = function_definition['prompt']['context']['attributes']
        context_dict = {attr: input_data[attr] for attr in context_attributes}
        context = function_definition['prompt']['context']['value'].format(**context_dict)

        # INSTRUCTIONS
        instructions_attributes = function_definition['prompt']['instructions']['attributes']
        instructions_dict = {attr: input_data[attr] for attr in instructions_attributes}
        instructions = function_definition['prompt']['instructions']['value'].format(**instructions_dict)

        # COGNITION
        if mode=='precision':
            cognition_attributes = function_definition['prompt']['cognition']['attributes']
            cognition_dict = {attr: input_data[attr] for attr in cognition_attributes}
            cognition = function_definition['prompt']['cognition']['value'].format(**cognition_dict)

        # DYNAMIC STRUCTURED OUTPUT
        dynamic_structured_outputs = function_definition.get('dynamic_structured_outputs', {})

        # REFERENTIAL DYNAMIC OUTPUTS
        referential_outputs = dynamic_structured_outputs.get('referential', [])
        for dynamic_config in referential_outputs:

            # COLLECT IN-SCOPE REFERENCES
            options = self.filter_taxonomy_objects(dynamic_config['ontology_path'],dynamic_config['filter_attributes'])

            # SET ATTRIBUTES
            fetch_attributes = dynamic_config['fetch_attributes']
            output_schema_description = {}
            output_enums = []

            # GET ALL NAMES, ATTRIBUTES
            for option in options:
                output_schema_description[option['name']] = {}
                output_enums.append(option['name'])
                for attribute in fetch_attributes:
                    output_schema_description[option['name']][attribute] = option[attribute]

            # SAVE ENUMS FROM NAMES, DESCRIPTION FROM ATTRIBUTE DICTIONARY
            output_schema['description'] = f"This is the JSON dictionary which contains the different choices and the attributes which describe them. {str(output_schema_description)}"
            output_schema['enum'] = output_enums

            # SET STRUCTURED OUTPUTS IN FUNCTION_DEFINITION
            path_parts = dynamic_config['output_enum_path'].split('.')
            segment = function_definition['output']
            for part in path_parts[:-1]:
                segment = segment[part]
            segment[path_parts[-1]]['enum'] = output_schema
            segment[path_parts[-1]]['description'] += '\n' + output_schema

        # INPUT-BASED DYNAMIC OUTPUTS
        # THIS TAKES IN A DICTIONARY ARGUMENT AND FORMATS IT
        input_outputs = dynamic_structured_outputs.get('input', [])
        for dynamic_config in input_outputs:

            # COLLECT IN-SCOPE REFERENCES
            options = self.filter_taxonomy_objects(dynamic_config['input_argument_path'],dynamic_config['filter_attributes'])

            # SET ATTRIBUTES
            fetch_attributes = dynamic_config['fetch_attributes']
            output_schema_description = {}
            output_enums = []

            # GET ALL NAMES, ATTRIBUTES
            for option in options:
                output_schema_description[option['name']] = {}
                output_enums.append(option['name'])
                for attribute in fetch_attributes:
                    output_schema_description[option['name']][attribute] = option[attribute]

            # SAVE ENUMS FROM NAMES, DESCRIPTION FROM ATTRIBUTE DICTIONARY
            output_schema['description'] = f"This is the JSON dictionary which contains the different choices and the attributes which describe them. {str(output_schema_description)}"
            output_schema['enum'] = output_enums

            # SET STRUCTURED OUTPUTS IN FUNCTION_DEFINITION
            path_parts = dynamic_config['output_enum_path'].split('.')
            segment = function_definition['output']
            for part in path_parts[:-1]:
                segment = segment[part]
            segment[path_parts[-1]]['enum'] = output_schema

        # SET STRUCTURED OUTPUT DEFINITION, TOOLS
        output = function_definition['output']
        tools_to_use = [
            {
                "type": "function",
                "function": {
                    "name": function,
                    "description": function['description'],
                    "parameters": output
                }
            }
        ]
        tool_choice = {"type": "function", "function": {"name": function}}


        # IF MODE IS SPEED, SKIP COGNITION
        if mode == 'speed':
            # PAYLOAD TO COMPLETION ENDPOINT
            system_prompt = system_prompt + '\nWrite your response in the JSON format provided.'
            user_prompt = context + '\n' + instructions
            messages = [
                PromptMessage(role="system", content=system_prompt),
                PromptMessage(role="user", content=user_prompt)
            ]
            
            chat_response = await self.prompt_client.execute_prompt(
                AISDKPrompt(messages=messages, tools=tools_to_use, tool_choice=tool_choice)
            )

        # IF MODE IS PRECISION, DO COGNITION CHAIN
        if mode == 'precision':


            # COGNITION PAYLOAD TO COMPLETION ENDPOINT
            system_prompt = system_prompt
            user_prompt = context + '\n' + cognition
            messages = [
                PromptMessage(role="system", content=system_prompt),
                PromptMessage(role="user", content=user_prompt)
            ]
            
            chat_response = await self.prompt_client.execute_prompt(
                AISDKPrompt(messages=messages)
            )

            # STRUCTURED PAYLOAD TO COMPLETION ENDPOINT
            system_prompt = system_prompt + '\nWrite your response in the JSON format provided.'

            messages = [
                PromptMessage(role="system", content=system_prompt),
                PromptMessage(role="assistant", content=chat_response["message"]["content"]),
                PromptMessage(role="user", content=instructions)
            ]
            
            chat_response = await self.prompt_client.execute_prompt(
                AISDKPrompt(messages=messages, tools=tools_to_use, tool_choice=tool_choice)
            )

        return chat_response
    
    
    # Helper function to fetch dynamic options
    def fetch_dynamic_options_from_dictionary(self, source_path, fetch_attributes, depth=None):
        def traverse_dictionary(node, fetch_attributes, parent_keys=[], current_depth=0):
            options = []
            if isinstance(node, dict):
                for key, value in node.items():
                    current_path = '.'.join(parent_keys + [key])
                    # When at the function level, gather the required attributes
                    if current_depth == depth or (depth is None and isinstance(value, dict) and all(attr in value for attr in fetch_attributes)):
                        option = {attr: value[attr] for attr in fetch_attributes if attr in value}
                        # Include the name from the dictionary key
                        option['name'] = key
                        option['path'] = current_path
                        options.append(option)
                    else:
                        # Continue traversal
                        options.extend(traverse_dictionary(value, fetch_attributes, parent_keys + [key], current_depth + 1))
            return options

        # Split the source path and navigate to the correct subtree
        path_parts = source_path.split('.')
        print(path_parts)
        data_segment = self.ontology
        for part in path_parts:
            try:
                data_segment = data_segment[part]
            except KeyError:
                raise KeyError(f"KeyError: '{part}' not found in current segment")

        # Start the traversal from the specified node
        options = traverse_dictionary(data_segment, fetch_attributes)

        # Convert options to a valid JSON schema object
        enum_values = [option['name'] for option in options]
        descriptions = {option['name']: {attr: option[attr] for attr in fetch_attributes if attr in option} for option in options}

        # print("enum info:")
        # print(enum_values)
        # print(descriptions)

        schema = {
            "type": "string",
            "enum": enum_values,
            "description": "These are the descriptions of the options to return: " + str(descriptions)
        }
        # print(schema)

        return schema
    
    
class Simulator:
    def __init__(self):
        self.prompt_client = ModelCompletion()
    
    
    def filter_taxonomy_objects(self, attribute_filter, ontology_location='functions.native'):
        """
        
        ontology_location = 'functions.native'
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
        ontology_branch = self.get_item_attributes(ontology_location)
        for obj in ontology_branch:
            keep = True
            for attribute in attribute_filter:
                if attribute_filter[attribute]:
                    if obj[attribute] not in attribute_filter[attribute]:
                        keep = False
            if keep:
                matching_taxonomy_objects.append(obj)
        return matching_taxonomy_objects

    # GENERATE RESPONSE FROM EACH ACTION
    async def simulate_actions(self, scenario, input, actions_path, actions_context):

        for action in actions_context:
            attribute_filter = {'name':[action['action']]}
            action_attributes = self.filter_taxonomy_objects(actions_path,attribute_filter)
            # get_item_attributes(data=ontology, target=actions_path)[action['action']]

            system_prompt = "You are a simulation example generator who focuses on high-quality, authentic example generation based on the scenario description and the current context."

            user_prompt = f"""Given this specific scenario, defined as: {scenario}\n\nYou have the current context so far: {input}
            Generate an authentic response from this action: {action}, described as {action_attributes["description"]}.
            The action has this output schema for a response: {action_attributes['output']}.

            Your output response should be a simulated example of the response of the use of the function. It should return results consistent with the described scenario and the description of what the action does.
            The described action is effectively an API call which will be executed, and your simulated response will provide a very thoughtful example of what would return from that API call.

            Explain how the response to this API call would look given the scenario and current context. Describe how you can make this authentic as it pertains to the expected data which would be returned as a real response, explain how the details connect to the overall scenario, and the existing context."""
                
            messages = [
                PromptMessage(role="system", content=system_prompt),
                PromptMessage(role="user", content=user_prompt)
            ]
            
            chat_response = await self.prompt_client.execute_prompt(
                AISDKPrompt(messages=messages)
            )
            
            # Completion
            tools_to_use = [
                {
                    "type": "function",
                    "function": {
                        "name": action['action'],
                        "description": action_attributes['description'],
                        "parameters": action_attributes['output']
                    }
                }
            ]
            tool_choice = {"type": "function", "function": {"name": action['action']}}


            system_prompt += '\n You provide responses in JSON format consistent with the schema the function would provide.'
            
            messages = [
                PromptMessage(role="system", content=system_prompt),
                PromptMessage(role="user", content=user_prompt),
                PromptMessage(role="assistant", content=chat_response["message"]["content"]),
                PromptMessage(role="user", content="Now write the response you have described into the JSON format provided.")
            ]
            
            chat_response = await self.prompt_client.execute_prompt(
                AISDKPrompt(messages=messages, tools=tools_to_use, tool_choice=tool_choice)
            )

            action_result = chat_response["message"]["tool_calls"][0]["function"]["arguments"]

            action['action_result'] = action_result

        return actions_context