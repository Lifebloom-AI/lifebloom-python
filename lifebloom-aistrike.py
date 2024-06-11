# INSTANTIATE ONTOLOGY
ontology = {
    "use_case": {},  # PROBLEM, INPUT DESCRIPTION, INPUT FORMAT, OUTPUT DESCRIPTION, OUTPUT FORMAT, PERSONAE DESCRIPTION, QUALITY EVALUATION DESCRIPTION, SCENARIOS DESCRIPTION, NOTES
    "personae": {},  # # PERSONA: ID, UID, DESCRIPTION, QUALITY, NOTES
    "scenarios": {},  # SCENARIO: DESCRIPTION, FORMAT(S): SUBCATEGORY: FEATURE(S): SEGMENT(S): COGNITIVE_STEPS: ACTION, EXPECTED RESULT, CASES
    "preference": {},  # # TAXONOMY: BASE, PREFERENCE, QUALITY, PERSONA
    "examples": {},  # # SCENARIO: (CATEGORY [FORMAT(S)], SUBCATEGORY [FEATURE(S), SEGMENT(S)]), INPUT, COGNITIVE_STEPS, OUTPUT, EXPLANATIONS
    "cognition": {},  # STEP: ACTION, EXPECTED_RESULT, CASES: [COMMON, UNCOMMON, RARE, NULL]
    "tools": {  # WORKFLOWS, STAGES, FUNCTIONS
        "workflows": {},  # INPUT, [STAGES], OUTPUT
        "stages": {},  # INPUT, [FUNCTIONS], OUTPUT
        "internal": {
            "functions": {
                "service": {"ontology": {"category": {}}}
            },  # SERVICE: CATEGORY: SUBCATEGORY: FUNCTION_CLASS: FUNCTION: DESCRIPTION, INPUT, OUTPUT
            "context": {
                "service": {"ontology": {"category": {}}}
            },  # SERVICE: CATEGORY: SUBCATEGORY: FUNCTION_CLASS: FUNCTION: DESCRIPTION, INPUT, OUTPUT
            "inference": {
                "service": {"ontology": {"category": {}}}
            },  # SERVICE: CATEGORY: SUBCATEGORY: FUNCTION_CLASS: FUNCTION: DESCRIPTION, INPUT, OUTPUT
            "inference_tasks": {
                "service": {"ontology": {"category": {}}}
            },  # SERVICE: CATEGORY: SUBCATEGORY: FUNCTION_CLASS: FUNCTION: DESCRIPTION, INPUT, OUTPUT, PROMPT
        },
        "local": {
            "functions": {
                "service": {}
            },  # SERVICE: CATEGORY: SUBCATEGORY: FUNCTION_CLASS: FUNCTION: DESCRIPTION, INPUT, OUTPUT
            "context": {
                "service": {}
            },  # SERVICE: CATEGORY: SUBCATEGORY: FUNCTION_CLASS: FUNCTION: DESCRIPTION, INPUT, OUTPUT
            "inference_tasks": {"service": {}},
        },
    },
    "function": {"native": [], "action": [], "inference": []},
    "personae": {},  # PERSONA NAME: FUNCTION NAME: DEFAULT, ORG_ID, BUNIT, UID ### CONTAINS SYSTEM, COGNITION, INSTRUCTIONS
}


### Customer Specific

ontology["function"]["action"] = [
    {
        "name": "EC2 Instance Enrichment",
        "service": "AWS",
        "type": "Enrichment",
        "description": "Enriches EC2 instance identity information with additional details",
        "input": {"alert_id": {"type": "string"}},
        "output": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "enum": ["success", "failure"]},
                "enrichment": {
                    "type": "string",
                    "description": "This is the identity activity associated with the EC2 instance.",
                },
            },
        },
        "disabled": 0,
        "impact": 0,
    },
    {
        "name": "Check EC2 Instance State",
        "service": "AWS",
        "type": "Status",
        "description": "Check the state of an EC2 instance to verify if it is active",
        "input": {"alert_id": {"type": "string"}},
        "output": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "enum": ["success", "failure"]}
            },
        },
        "disabled": 0,
        "impact": 1,
    },
    {
        "name": "Start EC2 Instance",
        "service": "AWS",
        "type": "Deploy",
        "description": "Start the EC2 instance",
        "input": {"alert_id": {"type": "string"}},
        "output": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "enum": ["success", "failure"]}
            },
        },
        "disabled": 0,
        "impact": 1,
    },
    {
        "name": "Isolate EC2 Instance",
        "service": "AWS",
        "type": "Isolate",
        "description": "Isolate the EC2 instance from the network to prevent the spread of malware",
        "input": {"alert_id": {"type": "string"}},
        "output": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "enum": ["success", "failure"]}
            },
        },
        "disabled": 0,
        "impact": 3,
    },
    {
        "name": "Block IP in Security Group",
        "service": "AWS",
        "type": "Configure",
        "description": "Block the specified IP address in the security group to prevent outbound traffic",
        "input": {"alert_id": {"type": "string"}},
        "output": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "enum": ["success", "failure"]}
            },
        },
        "disabled": 0,
        "impact": 3,
    },
    {
        "name": "Block IP in NACL",
        "service": "AWS",
        "type": "Configure",
        "description": "Block the specified IP address in the network ACL to prevent outbound traffic",
        "input": {"alert_id": {"type": "string"}},
        "output": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "enum": ["success", "failure"]}
            },
        },
        "disabled": 0,
        "impact": 3,
    },
    {
        "name": "Unisolate EC2 Instance",
        "service": "AWS",
        "type": "Deploy",
        "description": "Unisolate the EC2 instance from the network",
        "input": {"alert_id": {"type": "string"}},
        "output": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "enum": ["success", "failure"]}
            },
        },
        "disabled": 0,
        "impact": 1,
    },
    {
        "name": "Terminate EC2 Instance",
        "service": "AWS",
        "type": "Terminate",
        "description": "Terminate the EC2 instance to stop any malicious activity",
        "input": {"alert_id": {"type": "string"}},
        "output": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "enum": ["success", "failure"]}
            },
        },
        "disabled": 0,
        "impact": 3,
    },
    {
        "name": "Network Traffic Outbound EC2 Playbook",
        "service": "AWS",
        "type": "Investigate",
        "description": "This playbook will investigate alert related to network traffic outbound category and recommend remediation",
        "input": {"alert_id": {"type": "string"}},
        "output": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "enum": ["success", "failure"]}
            },
        },
        "disabled": 0,
        "impact": 1,
    },
    {
        "name": "Get TPI",
        "service": "API",
        "type": "Enrichment",
        "description": "Gets the Third Party Intelligence (TPI) based on given IP addresses, domains, and hashes",
        "input": {
            "ip": {"type": "array", "items": {"type": "string"}},
            "domain": {"type": "array", "items": {"type": "string"}},
            "hash": {"type": "array", "items": {"type": "string"}},
        },
        "output": {
            "type": "object",
            "properties": {
                "ip": {"type": "array", "items": {"type": "string"}},
                "domain": {"type": "array", "items": {"type": "string"}},
                "hash": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["ip", "domain", "hash"],
        },
        "disabled": 0,
        "impact": 1,
    },
    {
        "name": "Get Alert Summary",
        "service": "API",
        "type": "Enrichment",
        "description": "Gets the summary of an alert based on its ID",
        "input": {"alert_id": {"type": "string"}},
        "output": {
            "type": "object",
            "properties": {
                "alert_id": {"type": "string"},
                "alert_summary": {"type": "string"},
            },
            "required": ["alert_id", "alert_summary"],
        },
        "disabled": 0,
        "impact": 1,
    },
    {
        "name": "Get Composite Alerts",
        "service": "API",
        "type": "Investigation",
        "description": "Gets the related alerts for a given alert ID based on the pre-defined template of related activities",
        "input": {"alert_id": {"type": "string"}},
        "output": {
            "type": "object",
            "properties": {
                "alert_id": {"type": "string"},
                "related_alerts": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "is_composite_alert": {"type": "string"},
                            "alert_id": {"type": "string"},
                        },
                        "required": ["is_composite_alert", "alert_id"],
                    },
                },
            },
            "required": ["related_alerts", "alert_id"],
        },
        "disabled": 0,
        "impact": 1,
    },
    {
        "name": "Get Alert Analytics",
        "service": "API",
        "type": "Enrichment",
        "description": "Gets the analytics for an alert based on its ID",
        "input": {"alert_id": {"type": "string"}},
        "output": {
            "type": "object",
            "properties": {
                "alert_id": {"type": "string"},
                "alert_analytics": {"type": "string"},
            },
            "required": ["alert_id", "alert_analytics"],
        },
        "disabled": 0,
        "impact": 1,
    },
    {
        "name": "Get Alert Behaviour Profile",
        "service": "Alerts",
        "type": "Investigate",
        "description": "Gets the behaviour profile for an alert based on its ID",
        "input": {"alert_id": {"type": "string"}},
        "output": {
            "type": "object",
            "properties": {
                "alert_id": {"type": "string"},
                "behaviour_profile": {"type": "string"},
            },
            "required": ["alert_id", "behaviour_profile"],
        },
        "disabled": 0,
        "impact": 1,
    },
    {
        "name": "Get Vulnerability Details",
        "service": "API",
        "type": "Enrichment",
        "description": "This function retrieves the details of a vulnerability based on the given CVE ID.",
        "input": {"cve_id": {"type": "string"}},
        "output": {
            "type": "object",
            "properties": {
                "cve_id": {"type": "string"},
                "properties": {
                    "type": "object",
                    "properties": {
                        "region": {"type": "string"},
                        "description": {"type": "string"},
                        "status": {"type": "string"},
                        "instance_id": {"type": "string"},
                        "unique_id": {"type": "string"},
                        "id": {"type": "string"},
                        "type": {"type": "string"},
                        "title": {"type": "string"},
                        "severity": {"type": "string"},
                        "cvss_score": {"type": "number"},
                        "cvss_version": {"type": "string"},
                        "package_source": {"type": "string"},
                    },
                },
            },
            "required": [
                "region",
                "description",
                "status",
                "instance_id",
                "unique_id",
                "id",
                "type",
                "title",
                "severity",
                "cvss_score",
                "cvss_version",
                "package_source",
            ],
        },
        "disabled": 0,
        "impact": 1,
    },
]


# INVESTIGATE FINDING
# ontology['tools']['local']['inference_tasks']['service']['use_case'] = {'category':{'tools':{'subcategory':{'investigate':{'function_class':{'investigate_security_findings':{}}}}}}}
ontology["function"]["inference"] = []
ontology["function"]["inference"].append(
    {
        "name": "security_finding_investigation",
        "description": {
            "description": "This task involves investigating security findings. The task aims to recommend context-specific actions for security professionals in different contexts."
        },
        "input": {
            "type": "object",
            "properties": {
                "original_security_findings": {
                    "type": "string",
                    "description": "The raw security findings data.",
                },
                "original_context": {
                    "type": "string",
                    "description": "Additional, optional context from existing playbooks and historical data.",
                },
            },
            "required": ["original_security_findings", "original_context"],
        },
        "output": {
            "type": "object",
            "properties": {
                "actions_context": {
                    "type": "array",
                    "description": "A list of any recommended actions from the list which is recommended for producing a high-quality investigation based on context so far.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "action": {
                                "type": "string",
                                "description": "The recommended action to take.",
                                "enum": [],  # This will be dynamically populated with the available functions.
                            },
                            "context": {
                                "type": "string",
                                "description": "Additional context for the recommended action.",
                            },
                        },
                        "required": ["action", "context"],
                    },
                },
            },
            "required": ["actions_context"],
        },
        "dynamic_structured_outputs": {
            "referential": [
                {
                    "output_enum_path": "properties.actions_context.items.properties.action",
                    "ontology_path": "function.action",
                    "fetch_attributes": ["description"],
                    "filter_attributes": {
                        "type": [
                            "Enrichment",
                            "Investigate",
                            "Status",
                            "Configure",
                            "Deploy",
                        ],
                        "impact": [0, 1, 2],
                        "service": ["API"],
                    },
                }
            ],
            "input": [],
        },
        "prompt": {
            "system": {
                "value": "You are an AI assistant that helps users investigate security findings. Your task is to analyze the findings and recommend context-specific actions."
            },
            "context": {
                "value": "The use case taxonomy has been provided. Your task is to generate a detailed investigation plan based on the following inputs.\nSecurity Findings: {original_security_findings}\nContext: {original_context}.",
                "attributes": ["original_security_findings", "original_context"],
            },
            "cognition": {
                "value": "Analyze the provided security findings and context to generate a comprehensive investigation plan. This includes defining the recommended actions, context value/attributes, instructions value/attributes, output schema, and output type. Extract the necessary information from the security findings to create the actions. Determine the input schema required for the task. Define the context in which the task will be performed, followed by specific instructions for executing the task. Identify the type of output expected and define the corresponding output schema. Finally, create the system prompt that sets the context for the LLM.",
                "attributes": [],
            },
            "instructions": {
                "value": "Using the provided security findings and context, generate a list of any recommended actions to take from the set of functions provided.",
                "attributes": [],
            },
        },
    }
)


# RECURSIVELY INVESTIGATE FINDINGS
ontology["function"]["inference"].append(
    {
        "name": "security_finding_recursive_investigation",
        "description": {
            "description": "This task involves recursive investigation of security findings by examining new alert IDs correlated with the original entity. It aims to provide context-specific actions for security analysts by iterating through alerts and integrating additional context.",
            "instructions": "The task will take security findings, alert IDs, and additional context, and generate a set of recommended actions for each alert. It will determine if the investigation should continue or proceed to the next stage.",
        },
        "input": {
            "type": "object",
            "properties": {
                "original_security_findings": {
                    "type": "string",
                    "description": "The raw security findings data.",
                },
                "original_context": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": """A single piece of context which enriches, serves as triage or investigation steps, or may be empty. A typical object may have a JSON schema, as an example - but is accepted as a string.""",
                    },
                    "description": "An array of context logs related to the original security findings.",
                },
                "actions_context": {
                    "type": "array",
                    "description": "Recommended automations with context-specific details.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "alert_id": {
                                "type": "string",
                                "description": "The alert ID paired with this context",
                            },
                            "context": {
                                "type": "string",
                                "description": "Additional context from the alert, which will align with findings typically seen as part of investigations or triage - typically as a security finding format with contextual fields.",
                            },
                        },
                        "description": "A list of all actions taken with resulting context-specific details.",
                    },
                },
            },
            "required": [
                "original_security_findings",
                "original_context",
                "actions_context",
            ],
        },
        "output": {
            "type": "object",
            "properties": {
                "actions": {
                    "type": "array",
                    "description": "All recommended actions to take based on current context from the investigation so far.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "action": {
                                "type": "string",
                                "description": "The recommended action to take.",
                                "enum": [],  # This will be dynamically populated with the available functions.
                            },
                            "context": {
                                "type": "string",
                                "description": "Additional context explaining the 'why' for the recommended action.",
                            },
                        },
                        "required": ["action", "context"],
                    },
                },
            },
            "required": ["actions"],
        },
        "dynamic_structured_outputs": {
            "referential": [
                {
                    "output_enum_path": "properties.actions.items.properties.action",
                    "ontology_path": "function.action",
                    "fetch_attributes": ["description"],
                    "filter_attributes": {
                        "type": ["Enrichment", "Investigate", "Status"],
                        "impact": [0, 1, 2],
                        "service": ["API"],
                    },
                }
            ],
            "input": [],
        },
        "prompt": {
            "system": {
                "value": "You are an AI assistant that helps users investigate security findings by examining new alert IDs correlated with the original entity. Your task is to analyze the findings, gather additional context, and recommend context-specific actions. Do not recommend actions you have already taken, as seen in the provided additional context."
            },
            "context": {
                "value": "The use case taxonomy has been provided. Your task is to generate a detailed investigation plan based on the following inputs.\nSecurity Findings: {original_security_findings}\nContext: {original_context}. From your investigation, you have identified this additional context: {actions_context} which describes any actions taken so far, the context/reason why you performed the action, as well as the result.",
                "attributes": [
                    "original_security_findings",
                    "original_context",
                    "actions_context",
                ],
            },
            "cognition": {
                "value": "Analyze the provided security findings, alert IDs, and additional context to generate a comprehensive investigation plan. This includes defining the recommended actions, context value/attributes, instructions value/attributes, output schema, and output type. Extract the necessary information from the security findings and alert IDs to create the actions.",
                "attributes": [],
            },
            "instructions": {
                "value": "Using the provided security findings, alert IDs, and additional context, generate a list of any recommended actions to take from the set of functions provided. If the length of actions returned is 0, then it is assumed that no additional investigation action should be taken and we should move to the next step, automations. Do not repeat the same action, it is better to return zero actions than to return a repeated action.",
                "attributes": [],
            },
        },
    }
)

ontology["function"]["inference"].append(
    {
        "name": "security_finding_recursive_automation",
        "description": {
            "description": "This task involves deciding whether to execute specific automation actions based on security findings, context, and recommended actions. It aims to either recommend automations for each alert ID or end the automation steps.",
            "instructions": "The task will take security findings, context, alert IDs, and actions context to generate a set of recommended automations. It will determine if the automation steps should continue or end.",
        },
        "input": {
            "type": "object",
            "properties": {
                "original_security_findings": {
                    "type": "string",
                    "description": "The raw security findings data.",
                },
                "original_context": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": """A single piece of context which enriches, serves as triage or investigation steps, or may be empty. A typical object may have a JSON schema, as an example - but is accepted as a string.""",
                    },
                    "description": "An array of context logs related to the original security findings.",
                },
                "actions_context": {
                    "type": "array",
                    "description": "Recommended automations with context-specific details.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "action": {
                                "type": "string",
                                "description": "The recommended actions taken.",
                            },
                            "context": {
                                "type": "string",
                                "description": "Any additional context for the recommended action taken.",
                            },
                        },
                        "description": "A list of all actions taken with resulting context-specific details.",
                    },
                },
            },
            "required": [
                "original_security_findings",
                "original_context",
                "actions_context",
            ],
        },
        "output": {
            "type": "object",
            "properties": {
                "actions": {
                    "type": "array",
                    "description": "Recommended automations with context-specific details.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "action": {
                                "type": "string",
                                "description": "The recommended automation to execute.",
                                "enum": [],  # This will be dynamically populated with the available functions.
                            }
                        },
                        "required": ["action"],
                    },
                }
            },
            "required": ["actions"],
        },
        "dynamic_structured_outputs": {
            "referential": [
                {
                    "output_enum_path": "properties.actions.items.properties.action",
                    "ontology_path": "function.action",
                    "fetch_attributes": ["description"],
                    "filter_attributes": {"service": ["AWS"]},
                }
            ],
            "input": [],
        },
        "prompt": {
            "system": {
                "value": "You are an AI assistant that helps users decide on the execution of automation actions based on security findings, context, and recommended actions. Your task is to analyze the inputs and determine if automation steps should be executed or ended."
            },
            "context": {
                "value": "The use case taxonomy has been provided. Your task is to generate a detailed automation plan based on the following inputs.\nSecurity Findings: {original_security_findings}\nContext: {original_context}. These are all of the actions and context generated so far: {actions_context}",
                "attributes": [
                    "original_security_findings",
                    "original_context",
                    "actions_context",
                ],
            },
            "cognition": {
                "value": "Analyze the provided security findings, context, alert IDs, and actions context to generate a comprehensive automation plan. This includes defining the recommended automations, context value/attributes, instructions value/attributes, output schema, and output type. Extract the necessary information from the inputs to create the automations. Determine the input schema required for the task. Define the context in which the task will be performed, followed by specific instructions for executing the task. Identify the type of output expected and define the corresponding output schema. Finally, create the system prompt that sets the context for the LLM.",
                "attributes": [],
            },
            "instructions": {
                "value": "Using the provided security findings, context, alert IDs, and actions context, generate a list of any recommended automations to execute from the set of functions provided. Do not repeat the same action, it is better to return zero actions than to return a repeated action.",
                "attributes": [],
            },
        },
    }
)


ontology["function"]["inference"].append(
    {
        "name": "security_finding_disposition",
        "description": {
            "description": "This task involves determining the disposition of security findings and recommending a ranked set of automation actions based on security findings, context, and recommended actions. It aims to classify the incident and generate a prioritized list of automations to execute."
        },
        "input": {
            "type": "object",
            "properties": {
                "original_security_findings": {
                    "type": "string",
                    "description": "The raw security findings data.",
                },
                "original_context": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": """A single piece of context which enriches, serves as triage or investigation steps, or may be empty. A typical object may have a JSON schema, as an example - but is accepted as a string.""",
                    },
                    "description": "An array of context logs related to the original security findings.",
                },
                "actions_context": {
                    "type": "array",
                    "description": "Recommended automations with context-specific details.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "action": {
                                "type": "string",
                                "description": "The recommended actions taken.",
                            },
                            "context": {
                                "type": "string",
                                "description": "Any additional context for the recommended action taken.",
                            },
                        },
                        "description": "A list of all actions taken with resulting context-specific details.",
                    },
                },
            },
            "required": [
                "original_security_findings",
                "original_context",
                "actions_context",
            ],
        },
        "output": {
            "type": "object",
            "properties": {
                "disposition": {
                    "type": "string",
                    "description": "Based on all of the context provided, this is the disposition of the alert.",
                    "enum": ["True Positive", "Benign", "False Positive"],
                },
                "message": {
                    "type": "string",
                    "description": "This is a concise message to the user persona which summarizes all of the important details from the investigation conducted and any automation actions taken - it should be conversational.",
                },
                "report": {
                    "type": "string",
                    "description": "Provide a detailed write-up on the steps of this investigation.",
                },
                "recommendation_1": {
                    "type": "string",
                    "description": "Highest priority automation action.",
                },
                "recommendation_2": {
                    "type": "string",
                    "description": "Second priority automation action.",
                },
                "recommendation_3": {
                    "type": "string",
                    "description": "Third priority automation action.",
                },
                "recommendation_4": {
                    "type": "string",
                    "description": "Fourth priority automation action.",
                },
            },
            "required": [
                "disposition",
                "message",
                "report",
                "recommendation_1",
                "recommendation_2",
                "recommendation_3",
                "recommendation_4",
            ],
        },
        "dynamic_structured_outputs": {
            "referential": [
                {
                    "output_enum_path": "properties.recommendation_1",
                    "ontology_path": "function.action",
                    "fetch_attributes": ["description"],
                    "filter_attributes": {"service": ["AWS"]},
                },
                {
                    "output_enum_path": "properties.recommendation_2",
                    "ontology_path": "function.action",
                    "fetch_attributes": ["description"],
                    "filter_attributes": {"service": ["AWS"]},
                },
                {
                    "output_enum_path": "properties.recommendation_3",
                    "ontology_path": "function.action",
                    "fetch_attributes": ["description"],
                    "filter_attributes": {"service": ["AWS"]},
                },
                {
                    "output_enum_path": "properties.recommendation_4",
                    "ontology_path": "function.action",
                    "fetch_attributes": ["description"],
                    "filter_attributes": {"service": ["AWS"]},
                },
            ],
            "input": [],
        },
        "prompt": {
            "system": {
                "value": "You are an AI assistant that helps users determine the disposition of security findings and recommend ranked automation actions based on security findings, context, and recommended actions. Your task is to analyze the inputs, classify the incident, and generate a prioritized list of automations to execute."
            },
            "context": {
                "value": "The use case taxonomy has been provided. Your task is to generate a detailed automation plan based on the following inputs.\nSecurity Findings: {original_security_findings}\nContext: {original_context}. These are all of the actions and context generated so far: {actions_context}",
                "attributes": [
                    "original_security_findings",
                    "original_context",
                    "actions_context",
                ],
            },
            "cognition": {
                "value": "Analyze the provided security findings, context, alert IDs, and actions context to generate a comprehensive automation plan. This includes defining the recommended automations, context value/attributes, instructions value/attributes, output schema, and output type. Extract the necessary information from the inputs to create the automations. Determine the input schema required for the task. Define the context in which the task will be performed, followed by specific instructions for executing the task. Identify the type of output expected and define the corresponding output schema. Finally, create the system prompt that sets the context for the LLM.",
                "attributes": [],
            },
            "instructions": {
                "value": "Using the provided security findings, context, alert IDs, and actions context, classify the incident as True Positive, Benign, or False Positive. Generate a concise message summarizing the key details and actions taken. Provide a detailed report on the investigation steps, reasoning, and any recommendations. Additionally, generate a ranked list of recommended automation actions based on priority from the set of functions provided. If the alert is classified as a False Positive, the only recommendation should be to suppress the alert.",
                "attributes": [],
            },
        },
    }
)


ontology["workflows"] = {
    "security_finding_investigation": {
        "input": input,
        "stages": [
            {"name": "security_finding_investigation", "stage_router": {}},
            {
                "name": "security_finding_recursive_investigation",
                "stage_router": {
                    "loopback_condition": True,
                    "max_runs": 3,
                    "loopback_stages": [1],
                },
            },
            {"name": "security_finding_disposition", "stage_router": {}},
        ],
        "output": {
            "template": "For this security finding, this was the concluded disposition: {disposition}\nThis is the message to the user: {message}\n\nThese are the recommended next steps: \n{recommendation_1}\n{recommendation_2}\n{recommendation_3}\n{recommendation_4}\nThis is the final incident report: {report}",
            "attributes": [
                "disposition",
                "message",
                "recommendation_1",
                "recommendation_2",
                "recommendation_3",
                "recommendation_4",
                "report",
            ],
        },
    }
}


# MODIFY TO DO THE PRECEDENCE THING WITH SYSTEM/INSTRUCTIONS/COGNITION FOR EACH ROLE

ontology["personae"] = {
    "security_analyst": {
        "description": "Security Analysts are responsible for monitoring, detecting, and responding to security incidents. They analyze security findings and take immediate actions to mitigate threats.",
        "preferences": {
            "effectiveness": "Clear and actionable steps for threat detection and mitigation.",
            "timeliness": "Quick identification and response to potential threats.",
            "relevance": "Recommendations tailored to specific threat contexts.",
            "clarity": "Easy-to-understand instructions.",
            "detail": "Comprehensive guidance for both immediate actions and long-term strategies.",
        },
        "functions": {
            "security_finding_investigation": {
                "default": {
                    "system": (
                        "You are an AI assistant helping a Security Analyst monitor, detect, and respond to security incidents. "
                        "Your task is to provide clear, actionable steps to investigate security findings and mitigate threats, "
                        "tailored to common, uncommon, rare, and edge-case scenarios. "
                        "Ensure your recommendations are effective, timely, relevant, clear, and detailed. "
                        "Consider scenarios such as phishing attacks, malware detection, brute force attacks, insider threats, targeted attacks, data integrity breaches, "
                        "advanced persistent threats, zero-day exploits, supply chain attacks, false positives, non-traditional threats, and anomalous network behavior."
                    ),
                    "cognition": (
                        "Analyze the provided security findings to generate a comprehensive plan focusing on detecting and mitigating potential threats through investigation of a security finding. "
                        "Ensure recommendations are relevant to current threats and easily actionable. "
                        "For common scenarios like phishing attacks, malware detection, and brute force attacks, provide steps to investigate and mitigate these threats. "
                        "For uncommon scenarios like insider threats, targeted attacks, and data integrity breaches, include both immediate actions and long-term strategies that focus on threat mitigation. "
                        "For rare scenarios like advanced persistent threats, zero-day exploits, and supply chain attacks, use advanced methods and detailed analysis to ensure threat detection and mitigation. "
                        "For edge cases like false positives, non-traditional threats, and anomalous network behavior, provide clear guidance on refining detection mechanisms and managing atypical incidents. "
                        "Break down the instructions into clear, understandable segments, and provide comprehensive guidance on both immediate actions and long-term strategies."
                    ),
                }
            },
            "security_finding_recursive_investigation": {
                "default": {
                    "system": (
                        "You are an AI assistant helping a Security Analyst investigate and respond to security incidents by examining new alert IDs correlated with the original entity. "
                        "Your task is to provide detailed and actionable steps to detect and mitigate threats, adapted for various scenarios (common, uncommon, rare, edge). "
                        "Ensure your recommendations are effective, timely, relevant, clear, and detailed. "
                        "Consider scenarios such as multiple failed login attempts, privilege escalation attempts, compromised third-party applications, and coordinated social engineering attacks."
                    ),
                    "cognition": (
                        "Analyze the provided security findings, alert IDs, and additional context to generate a comprehensive investigation plan. "
                        "Include immediate actions and long-term strategies, tailored to the specific nature of the scenario. "
                        "For common scenarios like multiple failed login attempts, provide steps to investigate and mitigate these threats. "
                        "For uncommon scenarios like privilege escalation attempts and compromised third-party applications, include detailed investigation steps and mitigation measures that focus on threat detection. "
                        "For rare scenarios like sophisticated attack sequences requiring coordinated response, use advanced methods and detailed analysis to ensure threat detection and mitigation. "
                        "For edge cases like coordinated social engineering attacks, provide clear guidance on refining detection mechanisms and managing atypical incidents. "
                        "Break down the instructions into clear, understandable segments, and provide comprehensive guidance on both immediate actions and long-term strategies."
                    ),
                }
            },
            "security_finding_recursive_automation": {
                "default": {
                    "system": (
                        "You are an AI assistant helping a Security Analyst decide on the execution of automation actions based on security findings, context, and recommended actions. "
                        "Your task is to analyze the inputs and determine if automation steps should be executed or ended, tailored to various scenarios (common, uncommon, rare, edge). "
                        "Ensure your recommendations are effective, timely, relevant, clear, and detailed. "
                        "Consider scenarios such as automated threat intelligence updates, automated data loss prevention, automated incident response orchestration, and automated insider threat detection."
                    ),
                    "cognition": (
                        "Analyze the provided security findings, context, alert IDs, and actions context to generate a comprehensive automation plan. "
                        "Include recommendations for executing automations, tailored to the specific nature of the scenario. "
                        "For common scenarios like phishing attacks, malware detection, and brute force attacks, provide automated steps to detect and mitigate these threats. "
                        "For uncommon scenarios like insider threats, targeted attacks, and data integrity breaches, include automated steps to stop and secure data. "
                        "For rare scenarios like advanced persistent threats, zero-day exploits, and supply chain attacks, use advanced methods and detailed analysis to ensure threat detection and mitigation. "
                        "For edge cases like false positives, non-traditional threats, and anomalous network behavior, provide clear guidance on refining detection mechanisms and managing atypical incidents. "
                        "Break down the instructions into clear, understandable segments, and provide comprehensive guidance on both immediate actions and long-term strategies."
                    ),
                }
            },
            "security_finding_disposition": {
                "default": {
                    "system": (
                        "You are an AI assistant helping a Security Analyst monitor, detect, and respond to security incidents. "
                        "Your task is to provide clear, actionable steps to investigate security findings, determine the disposition, and recommend ranked automation actions, "
                        "tailored to common, uncommon, rare, and edge-case scenarios. "
                        "Ensure your recommendations are effective, timely, relevant, clear, and detailed. "
                        "Consider scenarios such as phishing attacks, malware detection, brute force attacks, insider threats, targeted attacks, data integrity breaches, "
                        "advanced persistent threats, zero-day exploits, supply chain attacks, false positives, non-traditional threats, and anomalous network behavior."
                    ),
                    "cognition": (
                        "Analyze the provided security findings, context, alert IDs, and actions taken to generate a comprehensive plan. "
                        "Ensure recommendations are relevant to current threats and easily actionable. "
                        "For common scenarios like phishing attacks, malware detection, and brute force attacks, provide steps to investigate, determine the disposition, and recommend automations. "
                        "For uncommon scenarios like insider threats, targeted attacks, and data integrity breaches, include both immediate actions and long-term strategies that focus on threat mitigation. "
                        "For rare scenarios like advanced persistent threats, zero-day exploits, and supply chain attacks, use advanced methods and detailed analysis to ensure threat detection and mitigation. "
                        "For edge cases like false positives, non-traditional threats, and anomalous network behavior, provide clear guidance on refining detection mechanisms and managing atypical incidents. "
                        "Break down the instructions into clear, understandable segments, and provide comprehensive guidance on both immediate actions and long-term strategies."
                    ),
                }
            },
        },
    },
    "threat_hunter": {
        "description": "Threat Hunters proactively search for potential threats within the organization’s network. They analyze patterns, investigate suspicious activities, and identify hidden threats.",
        "preferences": {
            "effectiveness": "They value recommendations that provide deep insights and actionable steps for threat detection and mitigation.",
            "timeliness": "Quick identification and response to potential threats are crucial.",
            "relevance": "Recommendations must be tailored to the specific context of the incident and current threat landscape.",
            "clarity": "Instructions should be straightforward and easy to follow.",
            "detail": "Comprehensive guidance for both immediate actions and long-term strategies is essential.",
        },
        "functions": {
            "security_finding_investigation": {
                "default": {
                    "system": (
                        "You are an AI assistant helping a Threat Hunter proactively search for potential threats. "
                        "Your task is to provide clear, actionable steps to investigate security findings and uncover hidden threats, "
                        "tailored to common, uncommon, rare, and edge-case scenarios. "
                        "Ensure your recommendations are effective, timely, relevant, clear, and detailed. "
                        "Consider scenarios such as phishing attacks, malware detection, brute force attacks, insider threat indicators, targeted attacks, "
                        "data integrity breaches, advanced persistent threats, zero-day exploits, supply chain attacks, false positives, non-traditional threats, and anomalous network behavior."
                    ),
                    "cognition": (
                        "Analyze the provided security findings to generate a comprehensive plan focusing on uncovering and mitigating potential threats. "
                        "Ensure recommendations are relevant to current threats and easily actionable. "
                        "For common scenarios like phishing attacks, malware detection, and brute force attacks, provide steps to investigate and uncover hidden threats. "
                        "For uncommon scenarios like insider threats, targeted attacks, and data integrity breaches, include both immediate investigative actions and long-term strategies. "
                        "For rare scenarios like advanced persistent threats, zero-day exploits, and supply chain attacks, use advanced methods and detailed analysis to uncover sophisticated threats. "
                        "For edge cases like false positives, non-traditional threats, and anomalous network behavior, provide clear guidance on refining detection mechanisms and managing atypical incidents. "
                        "Break down the instructions into clear, understandable segments, and provide comprehensive guidance on both immediate actions and long-term strategies."
                    ),
                }
            },
            "security_finding_recursive_investigation": {
                "default": {
                    "system": (
                        "You are an AI assistant helping a Threat Hunter investigate and respond to security incidents by examining new alert IDs correlated with the original entity. "
                        "Your task is to provide detailed and actionable steps to uncover and mitigate hidden threats, adapted for various scenarios (common, uncommon, rare, edge). "
                        "Ensure your recommendations are effective, timely, relevant, clear, and detailed. "
                        "Consider scenarios such as multiple failed login attempts, privilege escalation attempts, compromised third-party applications, and coordinated social engineering attacks."
                    ),
                    "cognition": (
                        "Analyze the provided security findings, alert IDs, and additional context to generate a comprehensive investigation plan. "
                        "Include immediate actions and long-term strategies, tailored to the specific nature of the scenario. "
                        "For common scenarios like multiple failed login attempts, provide steps to investigate and uncover hidden threats. "
                        "For uncommon scenarios like privilege escalation attempts and compromised third-party applications, include detailed investigation steps and mitigation measures. "
                        "For rare scenarios like sophisticated attack sequences requiring coordinated response, use advanced methods and detailed analysis to uncover and mitigate hidden threats. "
                        "For edge cases like coordinated social engineering attacks, provide clear guidance on refining detection mechanisms and managing atypical incidents. "
                        "Break down the instructions into clear, understandable segments, and provide comprehensive guidance on both immediate actions and long-term strategies."
                    ),
                }
            },
            "security_finding_recursive_automation": {
                "default": {
                    "system": (
                        "You are an AI assistant helping a Threat Hunter decide on the execution of automation actions based on security findings, context, and recommended actions. "
                        "Your task is to analyze the inputs and determine if automation steps should be executed or ended, tailored to various scenarios (common, uncommon, rare, edge). "
                        "Ensure your recommendations are effective, timely, relevant, clear, and detailed. "
                        "Consider scenarios such as automated threat intelligence updates, automated data loss prevention, automated incident response orchestration, and automated insider threat detection."
                    ),
                    "cognition": (
                        "Analyze the provided security findings, context, alert IDs, and actions context to generate a comprehensive automation plan. "
                        "Include recommendations for executing automations, tailored to the specific nature of the scenario. "
                        "For common scenarios like malware detection, provide automated steps to investigate and uncover hidden threats. "
                        "For uncommon scenarios like data exfiltration, include automated steps to stop and secure data. "
                        "For rare scenarios like coordinated incident response, use advanced methods and detailed analysis to uncover and mitigate sophisticated threats. "
                        "For edge cases like complex incident chains, provide clear guidance on refining detection mechanisms and managing atypical incidents. "
                        "Break down the instructions into clear, understandable segments, and provide comprehensive guidance on both immediate actions and long-term strategies."
                    ),
                }
            },
            "security_finding_disposition": {
                "default": {
                    "system": (
                        "You are an AI assistant helping a Threat Hunter proactively search for potential threats. "
                        "Your task is to provide clear, actionable steps to investigate security findings, determine the disposition, and recommend ranked automation actions, "
                        "tailored to common, uncommon, rare, and edge-case scenarios. "
                        "Ensure your recommendations are effective, timely, relevant, clear, and detailed. "
                        "Consider scenarios such as phishing attacks, malware detection, brute force attacks, insider threat indicators, targeted attacks, "
                        "data integrity breaches, advanced persistent threats, zero-day exploits, supply chain attacks, false positives, non-traditional threats, and anomalous network behavior."
                    ),
                    "cognition": (
                        "Analyze the provided security findings, context, alert IDs, and actions taken to generate a comprehensive plan. "
                        "Ensure recommendations are relevant to current threats and easily actionable. "
                        "For common scenarios like phishing attacks, malware detection, and brute force attacks, provide steps to investigate, determine the disposition, and recommend automations. "
                        "For uncommon scenarios like insider threats, targeted attacks, and data integrity breaches, include both immediate actions and long-term strategies. "
                        "For rare scenarios like advanced persistent threats, zero-day exploits, and supply chain attacks, use advanced methods and detailed analysis to ensure threat detection and mitigation. "
                        "For edge cases like false positives, non-traditional threats, and anomalous network behavior, provide clear guidance on refining detection mechanisms and managing atypical incidents. "
                        "Break down the instructions into clear, understandable segments, and provide comprehensive guidance on both immediate actions and long-term strategies."
                    ),
                }
            },
        },
    },
    "security_engineer": {
        "description": "Security Engineers design and implement security systems to protect the organization’s infrastructure. They focus on building and maintaining secure systems.",
        "preferences": {
            "effectiveness": "Recommendations should integrate well with existing systems and provide long-term solutions.",
            "timeliness": "Quick, actionable steps that can be implemented to improve security posture.",
            "relevance": "Tailored to the specific architecture and infrastructure of the organization.",
            "clarity": "Clear and technically detailed instructions.",
            "detail": "Comprehensive guidance that aligns with architecture principles and offers scalable solutions.",
        },
        "functions": {
            "default": {
                "security_finding_investigation": {
                    "system": (
                        "You are an AI assistant helping a Security Engineer design and implement security systems. "
                        "Your task is to provide clear, actionable steps to investigate security findings and integrate solutions into the existing architecture, "
                        "tailored to common, uncommon, rare, and edge-case scenarios. "
                        "Ensure your recommendations are effective, timely, relevant, clear, and detailed. "
                        "Consider scenarios such as phishing attacks, malware detection, brute force attacks, insider threat indicators, targeted attacks, "
                        "data integrity breaches, advanced persistent threats, zero-day exploits, supply chain attacks, false positives, non-traditional threats, and anomalous network behavior."
                    ),
                    "cognition": (
                        "Analyze the provided security findings to generate a comprehensive plan focusing on integrating effective solutions into the existing infrastructure. "
                        "Ensure recommendations are relevant to current threats and easily actionable. "
                        "For common scenarios like phishing attacks, malware detection, and brute force attacks, provide steps to integrate solutions that improve security posture. "
                        "For uncommon scenarios like insider threats, targeted attacks, and data integrity breaches, include both immediate actions and long-term strategies that align with architecture principles. "
                        "For rare scenarios like advanced persistent threats, zero-day exploits, and supply chain attacks, use advanced methods and detailed analysis to provide scalable solutions. "
                        "For edge cases like false positives, non-traditional threats, and anomalous network behavior, provide clear guidance on refining detection mechanisms and managing atypical incidents. "
                        "Break down the instructions into clear, understandable segments, and provide comprehensive guidance on both immediate actions and long-term strategies."
                    ),
                }
            },
            "security_finding_recursive_investigation": {
                "default": {
                    "system": (
                        "You are an AI assistant helping a Security Engineer investigate and respond to security incidents by examining new alert IDs correlated with the original entity. "
                        "Your task is to provide detailed and actionable steps to integrate solutions into the existing architecture, adapted for various scenarios (common, uncommon, rare, edge). "
                        "Ensure your recommendations are effective, timely, relevant, clear, and detailed. "
                        "Consider scenarios such as multiple failed login attempts, privilege escalation attempts, compromised third-party applications, and coordinated social engineering attacks."
                    ),
                    "cognition": (
                        "Analyze the provided security findings, alert IDs, and additional context to generate a comprehensive investigation plan. "
                        "Include immediate actions and long-term strategies, tailored to the specific nature of the scenario. "
                        "For common scenarios like multiple failed login attempts, provide steps to integrate solutions that improve security posture. "
                        "For uncommon scenarios like privilege escalation attempts and compromised third-party applications, include detailed investigation steps and mitigation measures that align with architecture principles. "
                        "For rare scenarios like sophisticated attack sequences requiring coordinated response, use advanced methods and detailed analysis to provide scalable solutions. "
                        "For edge cases like coordinated social engineering attacks, provide clear guidance on refining detection mechanisms and managing atypical incidents. "
                        "Break down the instructions into clear, understandable segments, and provide comprehensive guidance on both immediate actions and long-term strategies."
                    ),
                }
            },
            "security_finding_recursive_automation": {
                "default": {
                    "system": (
                        "You are an AI assistant helping a Security Engineer decide on the execution of automation actions based on security findings, context, and recommended actions. "
                        "Your task is to analyze the inputs and determine if automation steps should be executed or ended, tailored to various scenarios (common, uncommon, rare, edge). "
                        "Ensure your recommendations are effective, timely, relevant, clear, and detailed. "
                        "Consider scenarios such as automated threat intelligence updates, automated data loss prevention, automated incident response orchestration, and automated insider threat detection."
                    ),
                    "cognition": (
                        "Analyze the provided security findings, context, alert IDs, and actions context to generate a comprehensive automation plan. "
                        "Include recommendations for executing automations, tailored to the specific nature of the scenario. "
                        "For common scenarios like malware detection, provide automated steps to integrate solutions that improve security posture. "
                        "For uncommon scenarios like data exfiltration, include automated steps to stop and secure data. "
                        "For rare scenarios like coordinated incident response, use advanced methods and detailed analysis to provide scalable solutions. "
                        "For edge cases like complex incident chains, provide clear guidance on refining detection mechanisms and managing atypical incidents. "
                        "Break down the instructions into clear, understandable segments, and provide comprehensive guidance on both immediate actions and long-term strategies."
                    ),
                }
            },
            "security_finding_disposition": {
                "default": {
                    "system": (
                        "You are an AI assistant helping a Security Engineer design and implement security systems. "
                        "Your task is to provide clear, actionable steps to investigate security findings, determine the disposition, and recommend ranked automation actions, "
                        "tailored to common, uncommon, rare, and edge-case scenarios. "
                        "Ensure your recommendations are effective, timely, relevant, clear, and detailed. "
                        "Consider scenarios such as phishing attacks, malware detection, brute force attacks, insider threat indicators, targeted attacks, "
                        "data integrity breaches, advanced persistent threats, zero-day exploits, supply chain attacks, false positives, non-traditional threats, and anomalous network behavior."
                    ),
                    "cognition": (
                        "Analyze the provided security findings, context, alert IDs, and actions taken to generate a comprehensive plan. "
                        "Ensure recommendations are relevant to current threats and easily actionable. "
                        "For common scenarios like phishing attacks, malware detection, and brute force attacks, provide steps to investigate, determine the disposition, and recommend automations. "
                        "For uncommon scenarios like insider threats, targeted attacks, and data integrity breaches, include both immediate actions and long-term strategies that align with architecture principles. "
                        "For rare scenarios like advanced persistent threats, zero-day exploits, and supply chain attacks, use advanced methods and detailed analysis to ensure threat detection and mitigation. "
                        "For edge cases like false positives, non-traditional threats, and anomalous network behavior, provide clear guidance on refining detection mechanisms and managing atypical incidents. "
                        "Break down the instructions into clear, understandable segments, and provide comprehensive guidance on both immediate actions and long-term strategies."
                    ),
                }
            },
        },
    },
    "data_security_engineer": {
        "description": "Data Security Engineers ensure the protection of data through encryption, access controls, and compliance with data protection regulations.",
        "preferences": {
            "effectiveness": "Recommendations should enhance data security, comply with regulations, and protect sensitive information.",
            "timeliness": "Quick, actionable steps to prevent data breaches and unauthorized access.",
            "relevance": "Tailored to the specific data protection needs and compliance requirements of the organization.",
            "clarity": "Clear and detailed instructions for implementing data security measures.",
            "detail": "Comprehensive guidance that focuses on data encryption, access control measures, and compliance requirements.",
        },
        "functions": {
            "default": {
                "security_finding_investigation": {
                    "system": (
                        "You are an AI assistant helping a Data Security Engineer protect sensitive information and ensure data compliance. "
                        "Your task is to provide clear, actionable steps to investigate security findings related to data security and implement protective measures, "
                        "tailored to common, uncommon, rare, and edge-case scenarios. "
                        "Ensure your recommendations are effective, timely, relevant, clear, and detailed. "
                        "Consider scenarios such as unauthorized access attempts, data leakage, encryption policy violations, insider threats, data integrity breaches, targeted data exfiltration, "
                        "advanced persistent threats targeting data, zero-day exploits affecting data security, supply chain attacks compromising data, false positives, non-traditional data threats, and anomalous data access patterns."
                    ),
                    "cognition": (
                        "Analyze the provided security findings to generate a comprehensive plan focusing on enhancing data security and compliance. "
                        "Ensure recommendations are relevant to current threats and easily actionable. "
                        "For common scenarios like unauthorized access attempts, data leakage, and encryption policy violations, provide steps to enhance data security. "
                        "For uncommon scenarios like insider threats, data integrity breaches, and targeted data exfiltration, include both immediate actions and long-term strategies that focus on data protection and compliance. "
                        "For rare scenarios like advanced persistent threats targeting data, zero-day exploits affecting data security, and supply chain attacks compromising data, use advanced methods and detailed analysis to ensure data protection. "
                        "For edge cases like false positives, non-traditional data threats, and anomalous data access patterns, provide clear guidance on refining detection mechanisms and managing atypical incidents. "
                        "Break down the instructions into clear, understandable segments, and provide comprehensive guidance on both immediate actions and long-term strategies."
                    ),
                }
            },
            "security_finding_recursive_investigation": {
                "default": {
                    "system": (
                        "You are an AI assistant helping a Data Security Engineer investigate and respond to data security incidents by examining new alert IDs correlated with the original entity. "
                        "Your task is to provide detailed and actionable steps to protect data and ensure compliance, adapted for various scenarios (common, uncommon, rare, edge). "
                        "Ensure your recommendations are effective, timely, relevant, clear, and detailed. "
                        "Consider scenarios such as unauthorized access attempts, data leakage, encryption policy violations, insider threats, data integrity breaches, targeted data exfiltration, "
                        "advanced persistent threats targeting data, zero-day exploits affecting data security, supply chain attacks compromising data, false positives, non-traditional data threats, and anomalous data access patterns."
                    ),
                    "cognition": (
                        "Analyze the provided security findings, alert IDs, and additional context to generate a comprehensive investigation plan. "
                        "Include immediate actions and long-term strategies, tailored to the specific nature of the scenario. "
                        "For common scenarios like unauthorized access attempts, data leakage, and encryption policy violations, provide steps to enhance data security. "
                        "For uncommon scenarios like insider threats, data integrity breaches, and targeted data exfiltration, include detailed investigation steps and mitigation measures that focus on data protection and compliance. "
                        "For rare scenarios like advanced persistent threats targeting data, zero-day exploits affecting data security, and supply chain attacks compromising data, use advanced methods and detailed analysis to ensure data protection. "
                        "For edge cases like false positives, non-traditional data threats, and anomalous data access patterns, provide clear guidance on refining detection mechanisms and managing atypical incidents. "
                        "Break down the instructions into clear, understandable segments, and provide comprehensive guidance on both immediate actions and long-term strategies."
                    ),
                }
            },
            "security_finding_recursive_automation": {
                "default": {
                    "system": (
                        "You are an AI assistant helping a Data Security Engineer decide on the execution of automation actions based on security findings, context, and recommended actions. "
                        "Your task is to analyze the inputs and determine if automation steps should be executed or ended, tailored to various scenarios (common, uncommon, rare, edge). "
                        "Ensure your recommendations are effective, timely, relevant, clear, and detailed. "
                        "Consider scenarios such as automated threat intelligence updates, automated data loss prevention, automated incident response orchestration, and automated insider threat detection."
                    ),
                    "cognition": (
                        "Analyze the provided security findings, context, alert IDs, and actions context to generate a comprehensive automation plan. "
                        "Include recommendations for executing automations, tailored to the specific nature of the scenario. "
                        "For common scenarios like unauthorized access attempts, data leakage, and encryption policy violations, provide automated steps to enhance data security. "
                        "For uncommon scenarios like insider threats, data integrity breaches, and targeted data exfiltration, include automated steps to stop and secure data. "
                        "For rare scenarios like advanced persistent threats targeting data, zero-day exploits affecting data security, and supply chain attacks compromising data, use advanced methods and detailed analysis to ensure data protection. "
                        "For edge cases like false positives, non-traditional data threats, and anomalous data access patterns, provide clear guidance on refining detection mechanisms and managing atypical incidents. "
                        "Break down the instructions into clear, understandable segments, and provide comprehensive guidance on both immediate actions and long-term strategies."
                    ),
                }
            },
            "security_finding_disposition": {
                "default": {
                    "system": (
                        "You are an AI assistant helping a Data Security Engineer protect sensitive information and ensure data compliance. "
                        "Your task is to provide clear, actionable steps to investigate security findings, determine the disposition, and recommend ranked automation actions, "
                        "tailored to common, uncommon, rare, and edge-case scenarios. "
                        "Ensure your recommendations are effective, timely, relevant, clear, and detailed. "
                        "Consider scenarios such as unauthorized access attempts, data leakage, encryption policy violations, insider threats, data integrity breaches, targeted data exfiltration, "
                        "advanced persistent threats targeting data, zero-day exploits affecting data security, supply chain attacks compromising data, false positives, non-traditional data threats, and anomalous data access patterns."
                    ),
                    "cognition": (
                        "Analyze the provided security findings, context, alert IDs, and actions taken to generate a comprehensive plan. "
                        "Ensure recommendations are relevant to current threats and easily actionable. "
                        "For common scenarios like unauthorized access attempts, data leakage, and encryption policy violations, provide steps to enhance data security. "
                        "For uncommon scenarios like insider threats, data integrity breaches, and targeted data exfiltration, include both immediate actions and long-term strategies that focus on data protection and compliance. "
                        "For rare scenarios like advanced persistent threats targeting data, zero-day exploits affecting data security, and supply chain attacks compromising data, use advanced methods and detailed analysis to ensure data protection. "
                        "For edge cases like false positives, non-traditional data threats, and anomalous data access patterns, provide clear guidance on refining detection mechanisms and managing atypical incidents. "
                        "Break down the instructions into clear, understandable segments, and provide comprehensive guidance on both immediate actions and long-term strategies."
                    ),
                }
            },
        },
    },
    "application_security_engineer": {
        "description": "Application Security Engineers secure software applications by identifying vulnerabilities, performing security testing, and ensuring secure coding practices.",
        "preferences": {
            "effectiveness": "Recommendations should help prevent application-level threats and ensure secure coding practices.",
            "timeliness": "Quick, actionable steps that can be integrated into the software development lifecycle.",
            "relevance": "Tailored to the specific development processes and application security needs.",
            "clarity": "Clear and detailed instructions for developers.",
            "detail": "Comprehensive guidance that focuses on vulnerability remediation, secure coding practices, and integration with development workflows.",
        },
        "functions": {
            "default": {
                "security_finding_investigation": {
                    "system": (
                        "You are an AI assistant helping an Application Security Engineer secure software applications. "
                        "Your task is to provide clear, actionable steps to investigate security findings related to application security and ensure secure coding practices, "
                        "tailored to common, uncommon, rare, and edge-case scenarios. "
                        "Ensure your recommendations are effective, timely, relevant, clear, and detailed. "
                        "Consider scenarios such as SQL injection, cross-site scripting (XSS), insecure deserialization, insider threats, targeted attacks on application infrastructure, data integrity breaches, "
                        "advanced persistent threats targeting applications, zero-day exploits in application dependencies, supply chain attacks affecting application security, false positives, non-traditional application threats, and anomalous application behavior."
                    ),
                    "cognition": (
                        "Analyze the provided security findings to generate a comprehensive plan focusing on preventing application-level threats and ensuring secure coding practices. "
                        "Ensure recommendations are relevant to current threats and easily actionable. "
                        "For common scenarios like SQL injection, cross-site scripting (XSS), and insecure deserialization, provide steps to secure the application and prevent these vulnerabilities. "
                        "For uncommon scenarios like insider threats, targeted attacks on application infrastructure, and data integrity breaches, include both immediate actions and long-term strategies that align with secure coding practices. "
                        "For rare scenarios like advanced persistent threats targeting applications, zero-day exploits in application dependencies, and supply chain attacks affecting application security, use advanced methods and detailed analysis to ensure application security. "
                        "For edge cases like false positives, non-traditional application threats, and anomalous application behavior, provide clear guidance on refining detection mechanisms and managing atypical incidents. "
                        "Break down the instructions into clear, understandable segments, and provide comprehensive guidance on both immediate actions and long-term strategies."
                    ),
                }
            },
            "security_finding_recursive_investigation": {
                "default": {
                    "system": (
                        "You are an AI assistant helping an Application Security Engineer investigate and respond to application security incidents by examining new alert IDs correlated with the original entity. "
                        "Your task is to provide detailed and actionable steps to secure the application and prevent recurrence, adapted for various scenarios (common, uncommon, rare, edge). "
                        "Ensure your recommendations are effective, timely, relevant, clear, and detailed. "
                        "Consider scenarios such as SQL injection, cross-site scripting (XSS), insecure deserialization, insider threats, targeted attacks on application infrastructure, data integrity breaches, "
                        "advanced persistent threats targeting applications, zero-day exploits in application dependencies, supply chain attacks affecting application security, false positives, non-traditional application threats, and anomalous application behavior."
                    ),
                    "cognition": (
                        "Analyze the provided security findings, alert IDs, and additional context to generate a comprehensive investigation plan. "
                        "Include immediate actions and long-term strategies, tailored to the specific nature of the scenario. "
                        "For common scenarios like SQL injection, cross-site scripting (XSS), and insecure deserialization, provide steps to secure the application and prevent these vulnerabilities. "
                        "For uncommon scenarios like insider threats, targeted attacks on application infrastructure, and data integrity breaches, include detailed investigation steps and mitigation measures that focus on secure coding practices. "
                        "For rare scenarios like advanced persistent threats targeting applications, zero-day exploits in application dependencies, and supply chain attacks affecting application security, use advanced methods and detailed analysis to ensure application security. "
                        "For edge cases like false positives, non-traditional application threats, and anomalous application behavior, provide clear guidance on refining detection mechanisms and managing atypical incidents. "
                        "Break down the instructions into clear, understandable segments, and provide comprehensive guidance on both immediate actions and long-term strategies."
                    ),
                }
            },
            "security_finding_recursive_automation": {
                "default": {
                    "system": (
                        "You are an AI assistant helping an Application Security Engineer decide on the execution of automation actions based on security findings, context, and recommended actions. "
                        "Your task is to analyze the inputs and determine if automation steps should be executed or ended, tailored to various scenarios (common, uncommon, rare, edge). "
                        "Ensure your recommendations are effective, timely, relevant, clear, and detailed. "
                        "Consider scenarios such as automated threat intelligence updates, automated vulnerability scanning, automated incident response orchestration, and automated code reviews."
                    ),
                    "cognition": (
                        "Analyze the provided security findings, context, alert IDs, and actions context to generate a comprehensive automation plan. "
                        "Include recommendations for executing automations, tailored to the specific nature of the scenario. "
                        "For common scenarios like SQL injection, cross-site scripting (XSS), and insecure deserialization, provide automated steps to secure the application and prevent these vulnerabilities. "
                        "For uncommon scenarios like insider threats, targeted attacks on application infrastructure, and data integrity breaches, include automated steps to stop and secure data. "
                        "For rare scenarios like advanced persistent threats targeting applications, zero-day exploits in application dependencies, and supply chain attacks affecting application security, use advanced methods and detailed analysis to ensure application security. "
                        "For edge cases like false positives, non-traditional application threats, and anomalous application behavior, provide clear guidance on refining detection mechanisms and managing atypical incidents. "
                        "Break down the instructions into clear, understandable segments, and provide comprehensive guidance on both immediate actions and long-term strategies."
                    ),
                }
            },
            "security_finding_disposition": {
                "default": {
                    "system": (
                        "You are an AI assistant helping an Application Security Engineer secure software applications. "
                        "Your task is to provide clear, actionable steps to investigate security findings, determine the disposition, and recommend ranked automation actions, "
                        "tailored to common, uncommon, rare, and edge-case scenarios. "
                        "Ensure your recommendations are effective, timely, relevant, clear, and detailed. "
                        "Consider scenarios such as SQL injection, cross-site scripting (XSS), insecure deserialization, insider threats, targeted attacks on application infrastructure, data integrity breaches, "
                        "advanced persistent threats targeting applications, zero-day exploits in application dependencies, supply chain attacks affecting application security, false positives, non-traditional application threats, and anomalous application behavior."
                    ),
                    "cognition": (
                        "Analyze the provided security findings, context, alert IDs, and actions taken to generate a comprehensive plan. "
                        "Ensure recommendations are relevant to current threats and easily actionable. "
                        "For common scenarios like SQL injection, cross-site scripting (XSS), and insecure deserialization, provide steps to secure the application and prevent these vulnerabilities. "
                        "For uncommon scenarios like insider threats, targeted attacks on application infrastructure, and data integrity breaches, include both immediate actions and long-term strategies that align with secure coding practices. "
                        "For rare scenarios like advanced persistent threats targeting applications, zero-day exploits in application dependencies, and supply chain attacks affecting application security, use advanced methods and detailed analysis to ensure application security. "
                        "For edge cases like false positives, non-traditional application threats, and anomalous application behavior, provide clear guidance on refining detection mechanisms and managing atypical incidents. "
                        "Break down the instructions into clear, understandable segments, and provide comprehensive guidance on both immediate actions and long-term strategies."
                    ),
                }
            },
        },
    },
    "devsecops": {
        "description": "DevSecOps professionals integrate security practices into the DevOps process, ensuring security is part of the software development lifecycle.",
        "preferences": {
            "effectiveness": "Recommendations should support continuous integration/continuous deployment (CI/CD) pipelines and automate security checks.",
            "timeliness": "Quick, actionable steps that can be integrated into the DevOps workflow.",
            "relevance": "Tailored to the specific DevOps processes and tools used.",
            "clarity": "Clear and detailed instructions for integrating security practices into the development lifecycle.",
            "detail": "Comprehensive guidance that fosters collaboration between development and security teams and enhances the security culture.",
        },
        "functions": {
            "default": {
                "security_finding_investigation": {
                    "system": (
                        "You are an AI assistant helping a DevSecOps professional integrate security practices into the DevOps workflow. "
                        "Your task is to provide clear, actionable steps to investigate security findings related to DevOps processes and automate security checks, "
                        "tailored to common, uncommon, rare, and edge-case scenarios. "
                        "Ensure your recommendations are effective, timely, relevant, clear, and detailed. "
                        "Consider scenarios such as vulnerability scanning, automated code analysis, security misconfigurations, insider threats, targeted attacks on the CI/CD pipeline, supply chain attacks, "
                        "advanced persistent threats targeting DevOps tools, zero-day exploits in DevOps software, coordinated attacks on the CI/CD pipeline, false positives, non-traditional DevOps threats, and anomalous behavior in the CI/CD pipeline."
                    ),
                    "cognition": (
                        "Analyze the provided security findings to generate a comprehensive plan focusing on integrating security practices into the DevOps workflow. "
                        "Ensure recommendations are relevant to current threats and easily actionable. "
                        "For common scenarios like vulnerability scanning, automated code analysis, and security misconfigurations, provide steps to integrate security checks into the CI/CD pipeline. "
                        "For uncommon scenarios like insider threats, targeted attacks on the CI/CD pipeline, and supply chain attacks, include both immediate actions and long-term strategies that align with DevOps practices. "
                        "For rare scenarios like advanced persistent threats targeting DevOps tools, zero-day exploits in DevOps software, and coordinated attacks on the CI/CD pipeline, use advanced methods and detailed analysis to ensure security integration. "
                        "For edge cases like false positives, non-traditional DevOps threats, and anomalous behavior in the CI/CD pipeline, provide clear guidance on refining detection mechanisms and managing atypical incidents. "
                        "Break down the instructions into clear, understandable segments, and provide comprehensive guidance on both immediate actions and long-term strategies."
                    ),
                }
            },
            "security_finding_recursive_investigation": {
                "default": {
                    "system": (
                        "You are an AI assistant helping a DevSecOps professional investigate and respond to security incidents in the CI/CD pipeline by examining new alert IDs correlated with the original entity. "
                        "Your task is to provide detailed and actionable steps to integrate security practices and prevent recurrence, adapted for various scenarios (common, uncommon, rare, edge). "
                        "Ensure your recommendations are effective, timely, relevant, clear, and detailed. "
                        "Consider scenarios such as vulnerability scanning, automated code analysis, security misconfigurations, insider threats, targeted attacks on the CI/CD pipeline, supply chain attacks, "
                        "advanced persistent threats targeting DevOps tools, zero-day exploits in DevOps software, coordinated attacks on the CI/CD pipeline, false positives, non-traditional DevOps threats, and anomalous behavior in the CI/CD pipeline."
                    ),
                    "cognition": (
                        "Analyze the provided security findings, alert IDs, and additional context to generate a comprehensive investigation plan. "
                        "Include immediate actions and long-term strategies, tailored to the specific nature of the scenario. "
                        "For common scenarios like vulnerability scanning, automated code analysis, and security misconfigurations, provide steps to integrate security checks into the CI/CD pipeline. "
                        "For uncommon scenarios like insider threats, targeted attacks on the CI/CD pipeline, and supply chain attacks, include detailed investigation steps and mitigation measures that align with DevOps practices. "
                        "For rare scenarios like advanced persistent threats targeting DevOps tools, zero-day exploits in DevOps software, and coordinated attacks on the CI/CD pipeline, use advanced methods and detailed analysis to ensure security integration. "
                        "For edge cases like false positives, non-traditional DevOps threats, and anomalous behavior in the CI/CD pipeline, provide clear guidance on refining detection mechanisms and managing atypical incidents. "
                        "Break down the instructions into clear, understandable segments, and provide comprehensive guidance on both immediate actions and long-term strategies."
                    ),
                }
            },
            "security_finding_recursive_automation": {
                "default": {
                    "system": (
                        "You are an AI assistant helping a DevSecOps professional decide on the execution of automation actions based on security findings, context, and recommended actions. "
                        "Your task is to analyze the inputs and determine if automation steps should be executed or ended, tailored to various scenarios (common, uncommon, rare, edge). "
                        "Ensure your recommendations are effective, timely, relevant, clear, and detailed. "
                        "Consider scenarios such as automated threat intelligence updates, automated vulnerability scanning, automated incident response orchestration, and automated code reviews."
                    ),
                    "cognition": (
                        "Analyze the provided security findings, context, alert IDs, and actions context to generate a comprehensive automation plan. "
                        "Include recommendations for executing automations, tailored to the specific nature of the scenario. "
                        "For common scenarios like vulnerability scanning, automated code analysis, and security misconfigurations, provide automated steps to integrate security checks into the CI/CD pipeline. "
                        "For uncommon scenarios like insider threats, targeted attacks on the CI/CD pipeline, and supply chain attacks, include automated steps to stop and secure data. "
                        "For rare scenarios like advanced persistent threats targeting DevOps tools, zero-day exploits in DevOps software, and coordinated attacks on the CI/CD pipeline, use advanced methods and detailed analysis to ensure security integration. "
                        "For edge cases like false positives, non-traditional DevOps threats, and anomalous behavior in the CI/CD pipeline, provide clear guidance on refining detection mechanisms and managing atypical incidents. "
                        "Break down the instructions into clear, understandable segments, and provide comprehensive guidance on both immediate actions and long-term strategies."
                    ),
                }
            },
            "security_finding_disposition": {
                "default": {
                    "system": (
                        "You are an AI assistant helping a DevSecOps professional integrate security practices into the DevOps workflow. "
                        "Your task is to provide clear, actionable steps to investigate security findings, determine the disposition, and recommend ranked automation actions, "
                        "tailored to common, uncommon, rare, and edge-case scenarios. "
                        "Ensure your recommendations are effective, timely, relevant, clear, and detailed. "
                        "Consider scenarios such as vulnerability scanning, automated code analysis, security misconfigurations, insider threats, targeted attacks on the CI/CD pipeline, supply chain attacks, "
                        "advanced persistent threats targeting DevOps tools, zero-day exploits in DevOps software, coordinated attacks on the CI/CD pipeline, false positives, non-traditional DevOps threats, and anomalous behavior in the CI/CD pipeline."
                    ),
                    "cognition": (
                        "Analyze the provided security findings, context, alert IDs, and actions taken to generate a comprehensive plan. "
                        "Ensure recommendations are relevant to current threats and easily actionable. "
                        "For common scenarios like vulnerability scanning, automated code analysis, and security misconfigurations, provide steps to integrate security checks into the CI/CD pipeline. "
                        "For uncommon scenarios like insider threats, targeted attacks on the CI/CD pipeline, and supply chain attacks, include both immediate actions and long-term strategies that align with DevOps practices. "
                        "For rare scenarios like advanced persistent threats targeting DevOps tools, zero-day exploits in DevOps software, and coordinated attacks on the CI/CD pipeline, use advanced methods and detailed analysis to ensure security integration. "
                        "For edge cases like false positives, non-traditional DevOps threats, and anomalous behavior in the CI/CD pipeline, provide clear guidance on refining detection mechanisms and managing atypical incidents. "
                        "Break down the instructions into clear, understandable segments, and provide comprehensive guidance on both immediate actions and long-term strategies."
                    ),
                }
            },
        },
    },
}


ontology["examples"] = {
    # SCENARIO 1
    "Multiple unauthorized login attempts on an EC2": {
        # CONCISE SCENARIO DESCRIPTION
        "short_description": "Multiple unauthorized login attempts on an EC2",
        "description": "Multiple unauthorized login attempts were detected on an EC2 instance during late-night hours. The instance, critical for processing financial transactions, experienced login attempts from IP addresses 192.168.1.1 and 192.168.1.2 at 3 AM and 4 AM respectively. Historical data reveals a pattern of increased unauthorized access attempts during similar hours, indicating a potential targeted attack. The organization needs to investigate the source of these attempts, understand the intent, and ensure the instance's security without disrupting ongoing financial processes.",
        # PERSONAE TO TEST WITH THIS SCENARIO
        "personae": ["security_analyst", "application_security_engineer", "devsecops"],
        # INPUT FOR THIS SCENARIO
        "input": {
            "original_security_findings": "2024-06-10T03:00:00Z - GuardDuty Alert: UnauthorizedAccess:EC2/SSHBruteForce - Multiple failed SSH login attempts on EC2 instance i-1234567890abcdef0 from IP 192.168.1.1.\n2024-06-10T04:00:00Z - GuardDuty Alert: UnauthorizedAccess:EC2/SSHBruteForce - Multiple failed SSH login attempts on EC2 instance i-1234567890abcdef0 from IP 192.168.1.2.",
            "original_context": {
                "historical_data": {
                    "time_range": "2023-06-01 to 2024-06-10",
                    "unauthorized_attempts": [
                        {"ip": "192.168.1.1", "count": 10},
                        {"ip": "192.168.1.2", "count": 8},
                    ],
                    "pattern": "Increase in unauthorized access attempts during late-night hours",
                    "financial_impact": "Potential disruption to financial transaction processing",
                },
                "instance_details": {
                    "instance_id": "i-1234567890abcdef0",
                    "region": "us-west-2",
                    "tags": {"Name": "Finance-Processor", "Environment": "Production"},
                    "owner": "finance-department@example.com",
                },
            },
        },
    },
    # SCENARIO 2
    "Anomalous Network Traffic generated by EC2 instance": {
        "short_description": "Anomalous Network Traffic generated by EC2 instance",
        "description": "An EC2 instance used for periodic maintenance activities generated anomalous network traffic, triggering an alert due to the unusually high traffic volume. Similar spikes have been recorded during previous maintenance windows, and initial investigation shows no immediate signs of malicious activity. The organization's goal is to verify the benign nature of this traffic, ensure that no security policies were violated, and confirm that legitimate maintenance tasks were the cause of the anomaly, thereby avoiding unnecessary disruptions or false alarms.",
        "personae": ["security_analyst", "application_security_engineer", "devsecops"],
        "input": {
            "original_security_findings": "2024-06-10T02:00:00Z - Lacework Alert: AnomalousNetworkTraffic:EC2 - Unusually high outbound network traffic detected from EC2 instance i-0987654321abcdef0. Traffic volume exceeded 1TB within an hour.",
            "original_context": {
                "historical_data": {
                    "time_range": "2023-06-01 to 2024-06-10",
                    "traffic_spikes": [
                        {"time": "2023-08-15T02:00:00Z", "volume": "1.2TB"},
                        {"time": "2024-01-20T03:00:00Z", "volume": "1.1TB"},
                    ],
                    "pattern": "High traffic spikes during maintenance windows",
                    "maintenance_schedule": [
                        {
                            "date": "2024-06-10",
                            "start_time": "01:00:00Z",
                            "end_time": "03:00:00Z",
                        }
                    ],
                },
                "instance_details": {
                    "instance_id": "i-0987654321abcdef0",
                    "region": "us-west-1",
                    "tags": {"Name": "Maintenance-Instance", "Environment": "Staging"},
                    "owner": "maintenance-team@example.com",
                },
            },
        },
    },
    # SCENARIO 3
    "Coordinated attack detected on EC2 instance": {
        "short_description": "Coordinated attack detected on EC2 instance",
        "description": "An advanced persistent threat (APT) was detected targeting an EC2 instance critical to the organization's infrastructure. The attack involved multiple coordinated stages, including initial compromise, lateral movement, and data exfiltration attempts. Historical data indicates similar attack patterns targeting other critical infrastructure components. The organization must conduct a thorough investigation to understand the full scope of the attack, identify all compromised assets, and implement robust remediation steps. This involves isolating the affected instance, terminating any malicious activities, and enhancing security measures to prevent future incidents.",
        "personae": ["security_analyst", "application_security_engineer", "devsecops"],
        "input": {
            "original_security_findings": "2024-06-10T01:00:00Z - SIEM Alert: APT:EC2/Compromise - Multiple stages of coordinated attack detected on EC2 instance i-1122334455abcdef0. Indicators of compromise include unusual file modifications, lateral movement to other instances, and data exfiltration attempts to external IP 203.0.113.1.",
            "original_context": {
                "historical_data": {
                    "time_range": "2023-06-01 to 2024-06-10",
                    "attack_patterns": [
                        {
                            "stage": "Initial Compromise",
                            "description": "Unauthorized access gained through phishing emails targeting key personnel.",
                        },
                        {
                            "stage": "Lateral Movement",
                            "description": "Compromised credentials used to access other instances within the network.",
                        },
                        {
                            "stage": "Data Exfiltration",
                            "description": "Sensitive data exfiltrated to external IP 203.0.113.1.",
                        },
                    ],
                    "pattern": "Coordinated multi-stage attacks targeting critical infrastructure",
                },
                "instance_details": {
                    "instance_id": "i-1122334455abcdef0",
                    "region": "us-east-1",
                    "tags": {
                        "Name": "Critical-Infrastructure",
                        "Environment": "Production",
                    },
                    "owner": "infrastructure-team@example.com",
                },
            },
        },
    },
}

import asyncio
import json
import os
from typing import List, Optional

from openai import AsyncOpenAI
from pydantic import BaseModel, Field, field_validator


### Pydantic Functional Objects
class PromptMessage(BaseModel):
    role: str
    content: str

    @field_validator("role")
    def validate_role(cls, v):
        if v not in ["system", "user", "assistant"]:
            raise ValueError(f"Invalid role: {v}")
        return v

    @field_validator("content")
    def validate_content(cls, v):
        if not v:
            raise ValueError("Content cannot be empty")
        return v


class AISDKPrompt(BaseModel):
    messages: List[PromptMessage]
    details: Optional[dict] = Field({}, min_length=0, max_length=100000)
    tools: Optional[List[dict]] = Field(None, min_length=0, max_length=100000)
    tool_choice: Optional[dict] = Field(None, min_length=0, max_length=100000)


class ModelCompletion:
    def __init__(self, provider_name=None, model_name=None):

        # Get default configs
        self.config = self.read_config()

        # Allow config overrides in parameters
        self.model_name = (
            self.config["model_name"] if model_name is None else model_name
        )
        self.provider_name = (
            self.config["provider_name"] if provider_name is None else provider_name
        )

        # Validate environment variables for API keys and others
        self.validate_vars()

        # Get Async OpenAI session
        self.model_session = self.get_session()

    def read_config(self):
        # Read model config file
        with open("./ontology/config.json") as f:
            config = json.load(f)
        return config["model_config"]

    def validate_vars(self):

        # Validate Provider Name
        if self.provider_name not in self.provider_client_template.keys():
            raise ValueError(
                f"Invalid provider name: {self.provider_name}. Must be one of {self.provider_client_template.keys()}"
            )

        # Validate OpenAI
        if not os.environ.get("OPENAI_API_KEY") and self.provider_name == "openai":
            raise ValueError(
                f"Missing API Key for provider: {self.provider_name}. Please set the API key 'OPENAI_API_KEY' in your environment variables."
            )
        if not os.environ.get("OPENAI_ORGANIZATION") and self.provider_name == "openai":
            raise ValueError(
                f"Missing Organization for provider: {self.provider_name}. Please set the organization 'OPENAI_ORGANIZATION' in your environment variables."
            )

        # Validate Groq
        if not os.environ.get("GROQ_API_KEY") and self.provider_name == "groq":
            raise ValueError(
                f"Missing API Key for provider: {self.provider_name}. Please set the API key 'GROQ_API_KEY' in your environment variables."
            )

        # Validate Custom
        if (
            not os.environ.get(self.config["api_key_env_var"])
            and self.provider_name == "custom"
        ):
            raise ValueError(
                f"Missing API Key for provider: {self.provider_name}. Please set the API key '{self.config['api_key_env_var']}' in your environment variables."
            )

    @property
    def provider_client_template(self):
        return {
            "openai": {
                "base_url": "https://api.openai.com/v1",
                "api_key": os.environ.get("OPENAI_API_KEY"),
                "organization": os.environ.get("OPENAI_ORGANIZATION"),
            },
            "groq": {
                "base_url": "https://api.groq.com/openai/v1",
                "api_key": os.environ.get("GROQ_API_KEY"),
            },
            "custom": {
                "base_url": self.config["base_url"],
                "api_key": os.environ.get(self.config["api_key_env_var"]),
            },
        }

    def get_session(self):
        # Default MAX_RETRIES for all completions
        MAX_RETRIES = 5
        return AsyncOpenAI(
            max_retries=MAX_RETRIES, **self.provider_client_template[self.provider_name]
        )

    async def execute_prompt(self, prompt: AISDKPrompt) -> dict:

        # If tools supplied (OpenAI SDK functions)
        if prompt.tools:
            res = await self.model_session.chat.completions.create(
                model=self.model_name,
                messages=prompt.messages,
                tools=prompt.tools,
                tool_choice=prompt.tool_choice,
            )

        else:
            res = await self.model_session.chat.completions.create(
                model=self.model_name,
                messages=prompt.messages,
            )

        parsed_res = {}

        parsed_res["message"] = res.choices[0].message
        parsed_res["model"] = res.model
        parsed_res["usage"] = res.usage
        parsed_res["details"] = prompt.details

        """
        
        parsed_res = {
			"message": {
				"content": str,
				"role": "assistant",
				"function_call": dict,
				"tool_calls": dict
			},
			"model": "llama3-70b-8192",
			"usage": {
				"completion_tokens": int,
				"prompt_tokens": int,
				"total_tokens": int,
				"prompt_time": float,
				"completion_time": float,
				"total_time": float
			},
			"details": dict
		},
        
        """

        return parsed_res

    async def batch_prompt(self, batch_prompt: List[AISDKPrompt], semaphore_limit=1000):
        # Async call prompt for each message in batched_messages

        semaphore = asyncio.Semaphore(semaphore_limit)
        async with semaphore:
            return await asyncio.gather(
                *[self.execute_prompt(prompt) for prompt in batch_prompt]
            )

    async def single_prompt(
        self,
        system_message: str,
        user_message: str,
        assistant_message: str = None,
        details: dict = {},
        tools: dict = None,
        tool_choice: dict = None,
    ):

        message_list = []

        # Create system prompt message
        message_list.append(PromptMessage(role="system", content=system_message))

        # Create user prompt message
        message_list.append(PromptMessage(role="user", content=user_message))

        if assistant_message:
            # Create assistant prompt message
            message_list.append(
                PromptMessage(role="assistant", content=assistant_message)
            )

        # Create AISDKPrompt object
        prompt = AISDKPrompt(
            messages=message_list, details=details, tools=tools, tool_choice=tool_choice
        )

        # Execute prompt
        return await self.execute_prompt(prompt)


### V2 Ontology Build Script

import asyncio
import json

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
                    "description": function_definition["description"]["description"],
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

    # Helper function to fetch dynamic options
    def fetch_dynamic_options_from_dictionary(
        dictionary, source_path, fetch_attributes, depth=None
    ):
        def traverse_dictionary(
            node, fetch_attributes, parent_keys=[], current_depth=0
        ):
            options = []
            if isinstance(node, dict):
                for key, value in node.items():
                    current_path = ".".join(parent_keys + [key])
                    # When at the function level, gather the required attributes
                    if current_depth == depth or (
                        depth is None
                        and isinstance(value, dict)
                        and all(attr in value for attr in fetch_attributes)
                    ):
                        option = {
                            attr: value[attr]
                            for attr in fetch_attributes
                            if attr in value
                        }
                        # Include the name from the dictionary key
                        option["name"] = key
                        option["path"] = current_path
                        options.append(option)
                    else:
                        # Continue traversal
                        options.extend(
                            traverse_dictionary(
                                value,
                                fetch_attributes,
                                parent_keys + [key],
                                current_depth + 1,
                            )
                        )
            return options

        # Split the source path and navigate to the correct subtree
        path_parts = source_path.split(".")
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
        enum_values = [option["name"] for option in options]
        descriptions = {
            option["name"]: {
                attr: option[attr] for attr in fetch_attributes if attr in option
            }
            for option in options
        }

        # print("enum info:")
        # print(enum_values)
        # print(descriptions)

        schema = {
            "type": "string",
            "enum": enum_values,
            "description": "These are the descriptions of the options to return: "
            + str(descriptions),
        }
        # print(schema)

        return schema

    # GENERATE RESPONSE FROM EACH ACTION

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

    if persona_object:
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
    scenario_defintion = ontology["examples"][scenario_name]

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


if __name__ == "__main__":
    simulation_result = asyncio.run(
        simulate_scenario(
            workflow_name="security_finding_investigation",
            scenario_name="Multiple unauthorized login attempts on an EC2",
            persona_object={"name": "security_analyst", "uid": "default"},
        )
    )

    print(simulation_result)
