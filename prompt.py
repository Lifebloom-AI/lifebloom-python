from typing import List, Optional
from openai import AsyncOpenAI
import os
import asyncio
import json

from pydantic import BaseModel, Field, validator


### Pydantic Functional Objects
class PromptMessage(BaseModel):
    role: str
    content: str
    
    @validator("role")
    def validate_role(cls, v):
        if v not in ["system", "user", "assistant"]:
            raise ValueError(f"Invalid role: {v}")
        return v
    
    @validator("content")
    def validate_content(cls, v):
        if not v:
            raise ValueError("Content cannot be empty")
        return v

class AISDKPrompt(BaseModel):
    messages: List[PromptMessage]
    details: Optional[dict] = Field({}, min_length=0, max_length=100000)
    tools: Optional[dict] = Field(None, min_length=0, max_length=100000)
    tool_choice: Optional[dict] = Field(None, min_length=0, max_length=100000)


class ModelCompletion:
    def __init__(self, provider_name=None, model_name=None):
        
        # Get default configs
        self.config = self.read_config()
        
        # Allow config overrides in parameters
        self.model_name = self.config["model_name"] if model_name is None else model_name
        self.provider_name = self.config["provider_name"] if provider_name is None else provider_name
        
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
            raise ValueError(f"Invalid provider name: {self.provider_name}. Must be one of {self.provider_client_template.keys()}")
        
        # Validate OpenAI
        if not os.environ.get("OPENAI_API_KEY")  and self.provider_name == "openai":
            raise ValueError(f"Missing API Key for provider: {self.provider_name}. Please set the API key 'OPENAI_API_KEY' in your environment variables.")
        if not os.environ.get("OPENAI_ORGANIZATION") and self.provider_name == "openai":
            raise ValueError(f"Missing Organization for provider: {self.provider_name}. Please set the organization 'OPENAI_ORGANIZATION' in your environment variables.")
        
        # Validate Groq
        if not os.environ.get("GROQ_API_KEY") and self.provider_name == "groq":
            raise ValueError(f"Missing API Key for provider: {self.provider_name}. Please set the API key 'GROQ_API_KEY' in your environment variables.")
        
        # Validate Custom
        if not os.environ.get(self.config["api_key_env_var"]) and self.provider_name == "custom":
            raise ValueError(f"Missing API Key for provider: {self.provider_name}. Please set the API key '{self.config['api_key_env_var']}' in your environment variables.")
        
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
            }
        }
        
    def get_session(self):
        # Default MAX_RETRIES for all completions
        MAX_RETRIES = 5
        return AsyncOpenAI(
            max_retries=MAX_RETRIES,
            **self.provider_client_template[self.provider_name]
        )
        
    async def execute_prompt(self, prompt: AISDKPrompt) -> dict:
        
        # If tools supplied (OpenAI SDK functions)
        if prompt.tools:
            res =  await self.model_session.chat.completions.create(
                model=self.model_name,
                messages=prompt.messages,
                tools=prompt.tools,
                tool_choice=prompt.tool_choice,
            )
            
        else:
            res =  await self.model_session.chat.completions.create(
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
        
        
    async def batch_prompt(self, batch_prompt: List[AISDKPrompt], semaphore_limit = 1000):
        # Async call prompt for each message in batched_messages
        
        semaphore = asyncio.Semaphore(semaphore_limit)
        async with semaphore:
            return await asyncio.gather(
                *[self.execute_prompt(prompt) for prompt in batch_prompt]
            )

    async def single_prompt(self, system_message: str, user_message: str, assistant_message: str=None, details: dict = {}, tools: dict = None, tool_choice: dict = None):
        
        message_list = []
        
        # Create system prompt message
        message_list.append(PromptMessage(role="system", content=system_message))
        
        # Create user prompt message
        message_list.append(PromptMessage(role="user", content=user_message))
        
        if assistant_message:
            # Create assistant prompt message
            message_list.append(PromptMessage(role="assistant", content=assistant_message))
            
        # Create AISDKPrompt object
        prompt = AISDKPrompt(messages=message_list, details=details, tools=tools, tool_choice=tool_choice)
        
        # Execute prompt
        return await self.execute_prompt(prompt)
        
