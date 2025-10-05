r"""
Understanding LLM API Calls
===========================

This code focuses on:
- Building properly structured API requests
- Understanding message format and roles
- Working with API parameters like temperature
- Making actual API calls using the OpenAI client library

Note: Using the OpenAI client library, but the actual model and endpoint
are configured via environment variables and may not be OpenAI models.

## How to run this file:

1. Make sure you're in the llm_api_client folder:
    cd <llm_api_client-folder>

2. Make sure your virtual environment is activated:
    # On macOS/Linux:
    source .venv/bin/activate
   
    # On Windows:
    .venv\Scripts\activate
    or
    .venv\Scripts\Activate.ps1

    Also if "uv sync" does not work, try doing:

    uv sync --no-install-project

    In this current code the .env file's OPENAI_CHAT_MODEL can be set to model to, as an example:
    but you should change it to:

    OPENAI_CHAT_MODEL=gemini-2.5-flash

3. Run the file:
    python client.py

    This will execute the main() function at the bottom and show examples of
    all the API request structures.
"""

import os
import json
from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# The value from the .env file will now overwrite any existing OS variable
# load_dotenv(override=True)

# Get model from environment - this is set by your course instructor
CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL")

#CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gemini-2.5-flash")


def create_simple_request() -> Dict:
    """
    Create a simple API request with a single user message.
    
    Returns:
        A dictionary representing the API request payload
    """
    # TODO 1: Create and return a proper API request dictionary
    # It should ask "What is the capital of France?"
    # Include the model and messages fields
    
    request = {
        "model": CHAT_MODEL,
        "messages": [
            # TODO 1: Add a user message here asking about the capital of France
            {"role": "user", "content": "What is the capital of France?"}
        ]
    }
    
    return request


def create_conversation_request() -> Dict:
    """
    Create an API request with a multi-turn conversation.
    
    Returns:
        A dictionary representing the API request payload
    """
    # Build a conversation about programming
    messages = [
        {"role": "system", "content": "You are a helpful programming assistant."},
        {"role": "user", "content": "What is a variable?"},
        {"role": "assistant", "content": "A variable is a named storage location in memory that holds a value."},
        {"role": "user", "content": "What are the rules for naming variables in Python?"}
    ]
    
    request = {
        "model": CHAT_MODEL,
        "messages": messages
    }
    
    return request


def create_temperature_request(creativity_needed: bool) -> Dict:
    """
    Create an API request with appropriate temperature setting.
    
    Args:
        creativity_needed: If True, use high temperature; if False, use low temperature
        
    Returns:
        A dictionary representing the API request payload
    """
    messages = [
        {"role": "user", "content": "Generate a haiku about programming"}
    ]
    
    # TODO 3: Set the temperature based on creativity_needed
    # High creativity: temperature around 0.8-1.0
    # Low creativity: temperature around 0.1-0.3
    
    request = {
        "model": CHAT_MODEL,
        "messages": messages,
        "temperature": 0.9 if creativity_needed else 0.2
    }
    
    return request


def make_api_call(request: Dict) -> str:
    """
    Make an actual API call to OpenAI and return the response.
    
    Args:
        request: The API request payload
        
    Returns:
        The assistant's response text
    """
    # Initialize OpenAI client
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE"),
    )
    
    # Extract and return just the message content from the response
    # Hint: The response structure is response.choices[0].message.content
    
    try:
        # 1. Make the API call passing **request
        # 2. Extract the message content from the response
        # 3. Return the content
        #pass  # Remove this and implement the function
        response = client.chat.completions.create(**request)
        
        # Added based on behavior when max_tokens is too low. 
        # Extract the content from the response
        returned_content = response.choices[0].message.content

        # Check if the content is None or an empty string, often caused by max_tokens being too low
        if returned_content:
            # If content exists, return it
            return returned_content
        else:
            # If content is None or empty, return the default message
            return "token size too small to answer request"
        
        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"


def demonstrate_token_limit() -> Dict:
    """
    Create a request that demonstrates the max_tokens parameter.
    
    Returns:
        A dictionary representing the API request payload
    """
    messages = [
        {"role": "user", "content": "Explain machine learning in detail"}
    ]
    
    # TODO 5: Create a request that limits the response to approximately 50 tokens
    request = {
        "model": CHAT_MODEL,
        "messages": messages,
        "max_tokens": 50  # 50 and 500 Intentionally set too low to trigger token limit behavior.  Not sure the min max token size required, but 5000 generally returns results.
    }
    
    return request


def main():
    """Demonstrate all the functions."""
    print("=== OpenAI API Calls ===\n")
    
    # 1. Simple request
    print("1. Simple Request:")
    simple_req = create_simple_request()
    print(json.dumps(simple_req, indent=2))
    
    # 2. Conversation request
    print("\n2. Conversation Request:")
    conv_req = create_conversation_request()
    print(json.dumps(conv_req, indent=2))
    
    # 3. Temperature examples
    print("\n3. Temperature Requests:")
    creative_req = create_temperature_request(creativity_needed=True)
    factual_req = create_temperature_request(creativity_needed=False)
    print("Creative:", json.dumps(creative_req, indent=2))
    print("Factual:", json.dumps(factual_req, indent=2))
    
    # 4. Make an actual API call (commented out for testing)
    print("\n4. Actual API Call:")
    response = make_api_call(simple_req)
    #response = make_api_call(conv_req)
    #response = make_api_call(creative_req)
    #response = make_api_call(factual_req)
    
    print(f"Response: {response}")
    
    # 5. Token limit
    print("\n5. Token Limit Request:")
    token_req = demonstrate_token_limit()
    print(json.dumps(token_req, indent=2))

    response_token_limit = make_api_call(token_req)
    print(f"Response: {response_token_limit}")


if __name__ == "__main__":
    main()