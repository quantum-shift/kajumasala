from langchain_openai import ChatOpenAI
from browser_use import Agent
from browser_use import BrowserConfig, Browser, BrowserContextConfig
import asyncio
from dotenv import load_dotenv

load_dotenv()

# user_goal = """Demonstrate the Conversational Agent creation platform with an example of a 'Sales Negotiation Coach'.
# Emphasise on features such as 'Voice Language', 'System Prompt'
# """
steps = """1. Open elevenlabs.io website directly
2. Click 'Go to app'
3. Click 'Conversational AI' under products section in LHS
4. On the LHS choose 'Agents' -> Click 'Create an Ai Agent' -> 'Blank template'
5. Provide name as 'Sales Negotiation Coach' -> 'Create Agent' 
6. Select 'Agent Language' as 'Dutch' -> Input the 'System prompt' as something related to Negotiation coach.
7. Finally click 'Test AI Agent' and end.
"""

def create_steps_prompt(context: dict) -> str:
    if not context.get('user_query'):
        raise RuntimeError("Missing user_query in generateDemoSteps.create_steps_prompt")
    
    context.update('user_goal', context.get('user_query'))
    context.update('steps', steps)
    
    raise RuntimeError("Error path in generateDemoSteps.create_steps_prompt")