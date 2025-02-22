from langchain_openai import ChatOpenAI
from browser_use import Agent
from browser_use import BrowserConfig, Browser, BrowserContextConfig
import asyncio
from dotenv import load_dotenv

load_dotenv()

config = BrowserConfig(
    headless=False,
    disable_security=True,
    chrome_instance_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
)


async def main():
    browser = Browser(config=config)
    contextConfig = BrowserContextConfig(
        browser_window_size={
            'width': 1600,
            'height': 1200
        },
        save_recording_path="./recordings"
    )
    async with await browser.new_context(config=contextConfig) as context:
        agent = Agent(
            task="Generate demo steps by exploring the product",
            llm=ChatOpenAI(model="gpt-4o"),
            use_vision=True,
            browser_context=context
        )
        result = await agent.run()
        print(result)

    await browser.close()

asyncio.run(main())