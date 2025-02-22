from langchain_openai import ChatOpenAI
from browser_use import Agent
from browser_use import BrowserConfig, Browser, BrowserContextConfig
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

config = BrowserConfig(
    headless=False,
    disable_security=True,
    chrome_instance_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
)

# Define your local variables
user_goal = """Demonstrate the Conversational Agent creation platform with an example of a 'Sales Negotiation Coach'.
Emphasise on features such as 'Voice Language', 'System Prompt'
"""
steps = """1. Open elevenlabs.io website directly
2. Click 'Go to app'
3. Click 'Conversational AI' under products section in LHS
4. On the LHS choose 'Agents' -> Click 'Create an Ai Agent' -> 'Blank template'
5. Provide name as 'Sales Negotiation Coach' -> 'Create Agent' 
6. Select 'Agent Language' as 'Dutch' -> Input the 'System prompt' as something related to Negotiation coach.
7. Finally click 'Test AI Agent' and end.
"""

async def main():
    with open("demoAgent.prompt", "r") as file:
        prompt_template = file.read()
    
    task = prompt_template.format(user_goal=user_goal, steps=steps)

    browser = Browser(config=config)
    contextConfig = BrowserContextConfig(
        browser_window_size={
            'width': 1600,
            'height': 1200
        },
        save_recording_path="./recordings",
    )
    async with await browser.new_context(config=contextConfig) as context:
        agent = Agent(
            task=task,
            llm=ChatOpenAI(model="gpt-4o"),
            use_vision=True,
            browser_context=context
        )
        result = await agent.run()
        print(result)

    await browser.close()

asyncio.run(main())