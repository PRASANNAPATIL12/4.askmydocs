#!/usr/bin/env python3
"""
Test Emergent LLM Integration
"""

import asyncio
import os
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent / 'backend'))

async def test_emergent_llm():
    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage
        import uuid
        
        # Get API key
        EMERGENT_LLM_KEY = "sk-emergent-64dAeF36b167dF470D"
        
        print(f"Testing with API key: {EMERGENT_LLM_KEY}")
        
        # Create a unique session ID
        session_id = f"test_{uuid.uuid4().hex[:8]}"
        
        # Initialize the chat
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message="You are a helpful assistant."
        ).with_model("openai", "gpt-4o-mini")
        
        # Test message
        user_message = UserMessage(text="What is 2+2?")
        
        # Send message
        response = await chat.send_message(user_message)
        
        print(f"✅ Success! Response: {response}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_emergent_llm())
    sys.exit(0 if success else 1)