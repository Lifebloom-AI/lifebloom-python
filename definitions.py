# INSTANTIATE ONTOLOGY
ontology = {
    'feature': [
        {
            'name':'',        # NAME OF THE FEATURE (WORKFLOWS WITH MULTIPLE SCENARIO EXAMPLES REVIEWED BY PERSONAE)
            'description':'', # DESCRIPTION OF THE FEATURE
            'scenarios': {    # SCENARIOS WHICH TEST THE FEATURE
                'scenario_id': {                        # UNIQUE IDENTIFIER FOR THIS SCENARIO
                    'category':'',                      # CATEGORY NAME FOR THIS SCENARIO
                    'subcategory':'',                   # SUBCATEGORY NAME FOR THIS SCENARIO
                    'workflow_id': str,                 # UNIQUE IDENTIFIER FOR THE WORKFLOW USED
                    'workflow_input_example':dict,      # THE EXAMPLE INPUT PROVIDED FOR THIS SCENARIO
                    'workflow_stage_examples': [        # ARRAY OF WORKFLOW STAGE EXAMPLE RUNS BASED ON THE EXAMPLE INPUT FOR THIS SCENARIO
                        {
                            'stage_id':str,                   # UNIQUE IDENTIFIER FOR THE STAGE
                            'persona_id':str,                 # UNIQUE IDENTIFIER FOR THE PERSONA CONTEXT THIS STAGE WAS RUN UNDER
                            'stage_cognition_example':str,    # EXAMPLE OUTPUT FOR COGNITIVE STEPS SEGMENT OF STAGE
                            'stage_output_example':dict,      # EXAMPLE OUTPUT FOR THE OUTPUT OF STAGE
                            'stage_explanation_example': str  # EXAMPLE OUTPUT FOR EXPLANATION OF THE OUTPUT OF STAGE
                        }
                    ]
                }
            }
        },
    ],
    'personae': {},     # NAME, DESCRIPTION, UUID
    'preference': {},   # CHOSEN, REJECTED, REASON, SCENARIO_ID, PERSONA_ID
    'functions':{            # NATIVE, ACTION, TASKS, EXAMPLE_FUNCTIONS
        'native' : [],            # NAME, SERVICE, TYPE: {type:str, enum:[data,automation,communication]}, IMPACT, METADATA, DISABLED
        'action': [],             # NAME, SERVICE, TYPE: {type:str, enum:[data,automation,communication]}, INPUT, OUTPUT, IMPACT, METADATA, DISABLED
        'inference' : [],
        'reference_functions': {}

    },
    'workflows': {}     # NAME, DESCRIPTION, INPUT, STAGES, OUTPUT
}









# ACTION TYPES
action_types = {
    "Create": {
        "description": "Create new data or resources.",
        "examples": [
            "Create a new user account.",
            "Create a new database table.",
            "Create a new file."
        ]
    },
    "Read": {
        "description": "Retrieve or access existing data.",
        "examples": [
            "Read a user's profile information.",
            "Read data from a database table.",
            "Read the contents of a file."
        ]
    },
    "Update": {
        "description": "Modify or edit existing data.",
        "examples": [
            "Update a user's profile information.",
            "Update a database record.",
            "Edit the contents of a file."
        ]
    },
    "Delete": {
        "description": "Remove or delete existing data.",
        "examples": [
            "Delete a user account.",
            "Delete a database table.",
            "Delete a file."
        ]
    },
    "Search": {
        "description": "Look up specific data based on criteria.",
        "examples": [
            "Search for a user by name.",
            "Search for data in a database using a query.",
            "Search for a file by name."
        ]
    },
    "Query": {
        "description": "Retrieve specific data using a query language.",
        "examples": [
            "Query a database using SQL.",
            "Query an API for specific data.",
            "Query a search engine for relevant results."
        ]
    },
    "Restore": {
        "description": "Recover data from a backup or snapshot.",
        "examples": [
            "Restore a deleted file from a backup.",
            "Restore a database from a snapshot.",
            "Restore a system from a backup image."
        ]
    },
    "Backup": {
        "description": "Create a copy of data for safekeeping.",
        "examples": [
            "Backup files to an external drive.",
            "Backup a database to a cloud storage service.",
            "Backup a system to a backup server."
        ]
    },
    "Snapshot": {
        "description": "Create a point-in-time copy of data.",
        "examples": [
            "Take a snapshot of a virtual machine.",
            "Create a snapshot of a database.",
            "Take a snapshot of a file system."
        ]
    },
    "Scan": {
        "description": "Identify vulnerabilities or threats.",
        "examples": [
            "Scan a system for viruses.",
            "Scan a network for vulnerabilities.",
            "Scan a database for security threats."
        ]
    },
    "Remediate": {
        "description": "Fix vulnerabilities or threats.",
        "examples": [
            "Remediate a vulnerability by patching a system.",
            "Remediate a threat by removing malware.",
            "Remediate a security risk by configuring a firewall."
        ]
    },
    "Containment": {
        "description": "Isolate a threat or vulnerability to prevent spread.",
        "examples": [
            "Contain a malware outbreak by isolating infected machines.",
            "Contain a security breach by isolating a compromised account.",
            "Contain a vulnerabxility by isolating a affected system."
        ]
    },
    "Notify": {
        "description": "Send a notification about an event.",
        "examples": [
            "Notify a user of a new message.",
            "Notify an admin of a system failure.",
            "Notify a team of a new task assignment."
        ]
    },
    "Alert": {
        "description": "Trigger a warning or notification about a critical event.",
        "examples": [
            "Alert an admin of a critical system failure.",
            "Alert a team of a security breach.",
            "Alert a user of a suspicious login attempt."
        ]
    },
    "Report": {
        "description": "Generate a summary or detailed document about data or events.",
        "examples": [
            "Generate a report of system usage statistics.",
            "Create a report of security incidents.",
            "Generate a report of sales data."
        ]
    },
    "Monitor": {
        "description": "Continuously observe and track data or system performance.",
        "examples": [
            "Monitor system performance metrics.",
            "Monitor network traffic.",
            "Monitor a user's activity."
        ]
    },
    "Deploy": {
        "description": "Put a system, application, or code into production.",
        "examples": [
            "Deploy a new software application.",
            "Deploy a updated version of a system.",
            "Deploy a new database schema."
        ]
    },
    "Execute_Script": {
        "description": "Run a script or program.",
        "examples": [
            "Execute a Python script.",
            "Run a shell script.",
            "Execute a batch file."
        ]
    },
    "Execute_Process": {
        "description": "Run a process or application.",
        "examples": [
            "Execute a backup process.",
            "Run a database query process.",
            "Launch a web server process."
        ]
    },
    "Configure": {
        "description": "Set up or modify system or application settings.",
        "examples": [
            "Configure a network router.",
            "Set up a database connection.",
            "Modify application settings."
        ]
    },
    "Schedule": {
        "description": "Plan or schedule a task or event for a future time.",
        "examples": [
            "Schedule a backup for tomorrow.",
            "Plan a meeting for next week.",
            "Set a reminder for a future event."
        ]
    }
}