from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
load_dotenv()

OPEN_AI_API = "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"

async def main():
    agent = Agent(
        task="Go to Reddit, search for 'browser-use', click on the first post and return the first comment.",
        llm=ChatOpenAI(model="gpt-4o", api_key=OPEN_AI_API),
    )
    result = await agent.run()
    print(result)

asyncio.run(main())