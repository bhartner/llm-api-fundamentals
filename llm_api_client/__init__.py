"""
Understanding LLM API Calls
===========================

This package contains functions for learning how to build and make API calls
to Large Language Models (LLMs), focusing on proper request structure,
message formatting, and parameter understanding.

Main functions:
- create_simple_request(): Create a basic API request with a single message
- create_conversation_request(): Create a multi-turn conversation request
- create_temperature_request(): Create requests with different temperature settings
- make_api_call(): Execute API calls using the OpenAI client library
- demonstrate_token_limit(): Show how to handle token limits
"""

from .client import (
    CHAT_MODEL,
    create_simple_request,
    create_conversation_request,
    create_temperature_request,
    make_api_call,
    demonstrate_token_limit,
    main
)

__version__ = "1.0.0"
__author__ = "Ben Hartner"
__description__ = "Understanding LLM API Calls"

# Make key functions available at package level
__all__ = [
    "create_simple_request",
    "create_conversation_request", 
    "create_temperature_request",
    "make_api_call",
    "demonstrate_token_limit",
    "main"
]
