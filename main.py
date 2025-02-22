from langchain_openai import ChatOpenAI
from browser_use import Agent
from browser_use import BrowserConfig, Browser
import asyncio
from dotenv import load_dotenv
load_dotenv()

OPEN_AI_API = "sk-proj-"

config = BrowserConfig(
    headless=False,
    disable_security=True,
    chrome_instance_path="/Applications/Arc.app/Contents/MacOS/Arc"
)
browser = Browser()

browser.new_context()

async def main():
    agent = Agent(
        task="Go to google, search for 'next t20 match', click on the first result.",
        llm=ChatOpenAI(model="gpt-4o", api_key=OPEN_AI_API),
        use_vision=True,
        browser=Browser(config=config)
    )
    result = await agent.run()
    print(result)

asyncio.run(main())