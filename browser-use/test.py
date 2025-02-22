from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
from browser_use import BrowserConfig,Browser,Controller

load_dotenv()

config = BrowserConfig(
    headless=False,
    disable_security=True,
    chrome_instance_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
)

browser = Browser(config=config)

async def main():
    agent = Agent(
        task="Go to elevenlabs.io and try to create a conversational ai agent",
        llm=ChatOpenAI(model="gpt-4o"),
        browser=browser
    )
    result = await agent.run()
    print(result)

asyncio.run(main())