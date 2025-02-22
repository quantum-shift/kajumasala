from langchain_openai import ChatOpenAI
from browser_use import Agent
from browser_use import BrowserConfig, Browser
import asyncio
from dotenv import load_dotenv
load_dotenv()

config = BrowserConfig(
    headless=False,
    disable_security=True,
)
browser = Browser()

browser.new_context()

async def main():
    agent = Agent(
        task="Go to google, search for 'next t20 match', click on the first result.",
        llm=ChatOpenAI(model="gpt-4o"),
        use_vision=True,
        browser=Browser(config=config)
    )
    result = await agent.run()
    print(result)

asyncio.run(main())