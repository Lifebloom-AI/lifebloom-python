### V2 Ontology Build Script

from prompt import ModelCompletion, PromptMessage, AISDKPrompt
import json
from ontology import ontology
import asyncio


class WorkflowExecutor:
    
    def __init__(self):
        self.ontology = ontology
        self.prompt_client = ModelCompletion()
    
    
    def get_item_attributes(self, subset, location: str):
        path_parts = location.split('.')
        segment = subset
        for part in path_parts:
            segment = segment[part]
        return segment
    

    def filter_taxonomy_objects(self, ontology_subset, location, attribute_filter):
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
    
    
    async def execute_inference_function(self, function_context):
        # FUNCTION_CONTEXT: INPUT_DATA, MODE, FUNCTION_NAME, PERSONA

        # UNPACK VARS
        input_data = function_context['input']
        mode = function_context['mode']
        function_name = function_context['function_name']

        # GET INFERENCE FUNCTION DEFINITION FROM ONTOLOGY
        function_definition = self.filter_taxonomy_objects(self.ontology, 'function.inference',{'name':function_name})[0]
        
        # print(function_definition['prompt'])
        # SYSTEM
        system = function_definition['prompt']['system']['value']

        # COGNITION
        cognition = function_definition['prompt']['cognition']['value']

        # IF PERSONA, SET CONFIGS FOR SYSTEM/COGNITION BY PRECEDENCE
        if 'persona' in function_context:
            persona = function_context['persona']

            # IF PERSONA IS NOT DEFAULT, SET DEFAULT CONFIGS
            if persona['name'] != 'default':
                system = ontology['personae'][persona['name']]['functions'][function_name]['default']['system']
                cognition = ontology['personae'][persona['name']]['functions'][function_name]['default']['cognition']

                # IF PERSONA UID IS DEFINED IN PERSONAE TAXONOMY FOR THIS FUNCTION
                if persona['uid'] in ontology['personae'][persona['name']]['functions'][function_name]:

                    # IF PERSONA UID FOR THIS FUNCTION HAS SYSTEM
                    if ontology['personae'][persona['name']]['functions'][function_name][persona['uid']]['system'] != '':
                        system = ontology['personae'][persona['name']]['functions'][function_name]['default']['system']

                    # IF PERSONA UID FOR THIS FUNCTION HAS COGNITION
                    if ontology['personae'][persona['name']]['functions'][function_name][persona['uid']]['cognition'] != '':
                        cognition = ontology['personae'][persona['name']]['functions'][function_name]['default']['cognition']

        # CONTEXT
        context_attributes = function_definition['prompt']['context']['attributes']
        context_dict = {attr: input_data[attr] for attr in context_attributes}
        context = function_definition['prompt']['context']['value'].format(**context_dict)

        # INSTRUCTIONS
        instructions_attributes = function_definition['prompt']['instructions']['attributes']
        instructions_dict = {attr: input_data[attr] for attr in instructions_attributes}
        instructions = function_definition['prompt']['instructions']['value'].format(**instructions_dict)

        # DYNAMIC STRUCTURED OUTPUT
        dynamic_structured_outputs = function_definition.get('dynamic_structured_outputs', {})

        # REFERENTIAL DYNAMIC OUTPUTS
        referential_outputs = dynamic_structured_outputs.get('referential', [])
        for dynamic_config in referential_outputs:

            # COLLECT IN-SCOPE REFERENCES
            options = self.filter_taxonomy_objects(self.ontology, dynamic_config['ontology_path'],dynamic_config['filter_attributes'])

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

            # SET STRUCTURED OUTPUTS IN FUNCTION_DEFINITION
            path_parts = dynamic_config['output_enum_path'].split('.')
            segment = function_definition['output']
            for part in path_parts[:-1]:
                segment = segment[part]

            if len(output_enums) > 0:
                segment[path_parts[-1]]['enum'] = output_enums
                segment[path_parts[-1]]['description'] += '\n' + f"This is the JSON dictionary which contains the different choices and the attributes which describe them. {str(output_schema_description)}"

        # INPUT-BASED DYNAMIC OUTPUTS
        # THIS TAKES IN A DICTIONARY ARGUMENT AND FORMATS IT
        input_outputs = dynamic_structured_outputs.get('input', [])
        for dynamic_config in input_outputs:

            # COLLECT IN-SCOPE REFERENCES
            options = self.filter_taxonomy_objects(input_data,dynamic_config['input_argument_path'],dynamic_config['filter_attributes'])

            # SET ATTRIBUTES
            fetch_attributes = dynamic_config['fetch_attributes']
            output_schema_description = {}
            output_enums = []

            # GET ALL NAMES, ATTRIBUTES
            for option in options:
                if type(option) is list:
                    output_enums.append(option)
                    output_schema_description[option] = {}
                if type(option) is dict:
                    output_enums.append(option['name'])
                    output_schema_description[option['name']] = {}
                else:
                    output_schema_description = {}



                for attribute in fetch_attributes:
                    output_schema_description[option['name']][attribute] = option[attribute]

            # SET STRUCTURED OUTPUTS IN FUNCTION_DEFINITION
            path_parts = dynamic_config['output_enum_path'].split('.')
            segment = function_definition['output']
            for part in path_parts[:-1]:
                segment = segment[part]
            if len(output_enums) > 0:
                segment[path_parts[-1]]['enum'] = output_enums
                segment[path_parts[-1]]['description'] += '\n' + f"This is the JSON dictionary which contains the different choices and the attributes which describe them. {str(output_schema_description)}"

        # SET STRUCTURED OUTPUT DEFINITION, TOOLS
        output = function_definition['output']
        
        tools_to_use = [
            {
                "type": "function",
                "function": {
                    "name": function_name,
                    "description": function_definition['description']['description'],
                    "parameters": output
                }
            }
        ]
        
        tool_choice = {"type": "function", "function": {"name": function_name}}

        # IF MODE IS SPEED, SKIP COGNITION
        if mode == 'speed':
            # PAYLOAD TO COMPLETION ENDPOINT
            system_prompt = system + '\nWrite your response in the JSON format provided.'
            user_prompt = context + '\n' + instructions
            messages = [
                PromptMessage(role="system", content=system_prompt),
                PromptMessage(role="user", content=user_prompt)
            ]
            
            chat_response = await self.prompt_client.execute_prompt(
                AISDKPrompt(messages=messages, tools=tools_to_use, tool_choice=tool_choice)
            )

            return chat_response

        # IF MODE IS PRECISION, DO COGNITION CHAIN
        if mode == 'precision':

            # COGNITION PAYLOAD TO COMPLETION ENDPOINT
            system_prompt = system
            user_prompt = context + '\n' + cognition
            messages = [
                PromptMessage(role="system", content=system_prompt),
                PromptMessage(role="user", content=user_prompt)
            ]
            
            chat_response = await self.prompt_client.execute_prompt(
                AISDKPrompt(messages=messages)
            )

            
            cognition = chat_response["message"].content

            # STRUCTURED PAYLOAD TO COMPLETION ENDPOINT
            system_prompt = system + '\nWrite your response in the JSON format provided.'
            
            messages = [
                PromptMessage(role="system", content=system_prompt),
                PromptMessage(role="user", content=user_prompt),
                PromptMessage(role="assistant", content=cognition),
                PromptMessage(role="user", content=instructions)
            ]
            
            chat_response = await self.prompt_client.execute_prompt(
                AISDKPrompt(messages=messages, tools=tools_to_use, tool_choice=tool_choice)
            )

            return chat_response, context


        # IF MODE IS TRAINING, DO COGNITION CHAIN AND EXPLANATION CHAIN
        if mode == 'training':

            # COGNITION PAYLOAD TO COMPLETION ENDPOINT
            system_prompt = system
            user_prompt = context + '\n' + cognition

            messages = [
                PromptMessage(role="system", content=system),
                PromptMessage(role="user", content=user_prompt)
            ]

            chat_response = await self.prompt_client.execute_prompt(
                AISDKPrompt(messages=messages)
            )
            cognition = chat_response["message"].content

            # STRUCTURED PAYLOAD TO COMPLETION ENDPOINT
            system_prompt = system + '\nWrite your response in the JSON format provided.'
            messages = [
                PromptMessage(role="system", content=system_prompt),
                PromptMessage(role="user", content=user_prompt),
                PromptMessage(role="assistant", content=cognition),
                PromptMessage(role="user", content=instructions)
            ]
            chat_response = await self.prompt_client.execute_prompt(
                AISDKPrompt(messages=messages, tools=tools_to_use, tool_choice=tool_choice)
            )

            completion = json.loads(chat_response["message"].tool_calls[0].function.arguments)

            # STRUCTURED PAYLOAD TO COMPLETION ENDPOINT
            system_prompt = system
            
            messages = [
                PromptMessage(role="system", content=system_prompt),
                PromptMessage(role="user", content=user_prompt),
                PromptMessage(role="assistant", content=cognition),
                PromptMessage(role="user", content=instructions),
                PromptMessage(role="assistant", content=cognition),
                PromptMessage(role="user", content="Explain your answer.")
            ]
            
            chat_response = await self.prompt_client.execute_prompt(
                AISDKPrompt(messages=messages)
            )


            explanation = chat_response["message"].content

            completion[function_name + '_details'] = {
                'cognition': cognition,
                'explanation': explanation
            }

            return completion
        
    # Helper function to fetch dynamic options
    def fetch_dynamic_options_from_dictionary(dictionary, source_path, fetch_attributes, depth=None):
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
        # print(path_parts)
        data_segment = ontology
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

    # GENERATE RESPONSE FROM EACH ACTION
    async def simulate_actions(self, scenario, input, actions_path, actions_context):
        
        async def execute_simulation(scenario, input, actions_path, action):

            try:
                print("SIMULATING ACTION: ", [action['action']])
                attribute_filter = {'name':[action['action']]}
                action_attributes = self.filter_taxonomy_objects(self.ontology, actions_path,attribute_filter)[0]
                action_attributes['name']=action_attributes['name'].replace(' ','_')
                # print(action_attributes)

                # get_item_attributes(data=ontology, target=actions_path)[action['action']]

                system_prompt = "You are a simulation example generator who focuses on high-quality, authentic example generation based on the scenario description and the current context."

                user_prompt = f"""Given this specific scenario, defined as: {scenario}\n\nYou have the current context so far: {input}
            Generate an authentic response from this action: {action}, described as {action_attributes["description"]}.
            The action has this output schema for a response: {str(action_attributes['output'])}.

            Your output response should be a simulated example of the response of the use of the function. It should return results consistent with the described scenario and the description of what the action does.
            The described action is effectively an API call which will be executed, and your simulated response will provide a very thoughtful example of what would return from that API call.

            Explain how the response to this API call would look given the scenario and current context. Describe how you can make this authentic as it pertains to the expected data which would be returned as a real response, explain how the details connect to the overall scenario, and the existing context."""


                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
                
                messages = [
                    PromptMessage(role="system", content=system_prompt),
                    PromptMessage(role="user", content=user_prompt)
                ]
                
                chat_response = await self.prompt_client.execute_prompt(
                    AISDKPrompt(messages=messages)
                )

                # completion
                tools_to_use = [
                    {
                        "type": "function",
                        "function": {
                            "name": action_attributes['name'],
                            "description": action_attributes['description'],
                            "parameters": action_attributes['output']
                            }
                        }
                ]
                tool_choice = {"type": "function", "function": {"name": action_attributes['name']}}
                # print(tools_to_use)


                system_prompt += '\n You provide responses in JSON format consistent with the schema the function would provide.'
                
                messages = [
                    PromptMessage(role="system", content=system_prompt),
                    PromptMessage(role="user", content=user_prompt),
                    PromptMessage(role="assistant", content=chat_response["message"].content),
                    PromptMessage(role="user", content="Now write the response you have described into the JSON format provided.")
                ]
                
                chat_response = await self.prompt_client.execute_prompt(
                    AISDKPrompt(messages=messages, tools=tools_to_use, tool_choice=tool_choice)
                )

                action_result = json.loads(chat_response["message"].tool_calls[0].function.arguments)

                action['action_result'] = action_result
            except: # Action doesn't exist, simulation failure
                action['action_result'] = "Failure"
                
            return action

            
        routines = []
        for action in actions_context:
            routines.append(execute_simulation(scenario, input, actions_path, action))
            
        actions_context = await asyncio.gather(*routines)

        return actions_context
    
    
    async def run_workflow(self, workflow_name, persona, input, mode='precision', simulation=True, scenario=None):
        if 'actions_context' not in input:
            input['actions_context'] = []

        thread = []
        output_thread = []
        workflow = ontology['workflows'][workflow_name]

        # RUN EACH STAGE
        for stage in workflow['stages']:
            thread_run, context = await self.process_stage(stage['name'], input, persona)
            thread.append(thread_run)

            # ADD LAST THREAD RUN OUTPUTS TO INPUTS
            for attribute in thread_run['output']:
                if attribute in ['actions','actions_context']:
                    continue
                else:
                    input[attribute] = thread_run['output'][attribute]

            actions_to_run = []
            
            # IF THERE ARE ACTIONS, EXECUTE THEM
            if 'actions' in thread_run:

                # CHECK TO SEE IF ACTIONS ALREADY RUN
                for action in thread_run['actions']:
                    run_action = True
                    for run in thread:
                        if 'actions' in run and action['action'] in run["actions"]:
                            run_action = False
                    if run_action:
                        actions_to_run.append(action)

            actions_path = "function.action"

            # SIMULATE ACTIONS
            if simulation:
                thread_run['actions'] = await self.simulate_actions(scenario, input, actions_path, actions_to_run)
                input['actions_context'].append(thread_run['actions'])

            # OR RETURN ACTIONS TO EXECUTE
            else:
                print("EXECUTE ACTIONS: ", actions_to_run)
                return thread
            
            formatted_thread = {
                "function_name": stage['name'],
                "input_context": context,
                "output": thread_run['output'],
            }
            output_thread.append(formatted_thread)

        # GET LATEST OF EACH ATTRIBUTE IN THREAD
        output_attributes = workflow['output']['attributes']
        output_template = workflow['output']['template']
        output_dict = {}
        for attribute in output_attributes:
            output_dict[attribute] = input[attribute]

        output = output_template.format(**output_dict)
        print('WORKFLOW OUTPUT: ',output,'\n\n')
        return output_dict, output_thread

    async def process_stage(self, function_name, input, persona):
        # PAYLOAD
        function_context = {
            'function_name': function_name,
            'input': input,
            'persona': persona,
            'mode': 'precision'
            }

        # EXECUTE & STORE
        print("EXECUTING: ",function_name)
        response, context = await self.execute_inference_function(function_context)
        
        print("RESPONSE: ", response["message"].tool_calls[0].function.arguments)
        function_context['output'] = json.loads(response["message"].tool_calls[0].function.arguments)

        # GET ACTIONS TO EXECUTE
        if 'actions_context' in json.loads(response["message"].tool_calls[0].function.arguments):
            
            function_context['actions'] = json.loads(response["message"].tool_calls[0].function.arguments)['actions_context']

        return function_context, context