from langchain_openai import ChatOpenAI
from browser_use import Agent
from browser_use import BrowserConfig, Browser, BrowserContextConfig
import asyncio
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()

config = BrowserConfig(
    headless=False,
    disable_security=True,
    chrome_instance_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
)

def createTempDir(req_id):
    dir_path = f"./recordings/{req_id}"

    directory = Path(dir_path)
    directory.mkdir(parents=True, exist_ok=True)
    return dir_path

async def generateDemoVideo(context):
    request_id = context['request_id']
    start_url = context['start_url']
    user_goal = context['user_goal']
    demo_steps = context['demo_steps']

    with open("demoAgent.prompt", "r") as file:
        task_template = file.read()
    task = task_template.format(user_goal=user_goal, steps=demo_steps)

    recording_path = createTempDir(request_id)
    browser = Browser(config=config)
    contextConfig = BrowserContextConfig(
        browser_window_size={
            'width': 1600,
            'height': 1200
        },
        save_recording_path=recording_path,
    )
    async with await browser.new_context(config=contextConfig) as browser_context:
        agent = Agent(
            task=task,
            llm=ChatOpenAI(model="gpt-4o"),
            use_vision=True,
            use_vision_for_planner=True,
            browser_context=browser_context,
            initial_actions=[
                {'open_tab': {'url': start_url}}
            ]
        )
        result = await agent.run()
        print(result)
    await browser.close()

    context['demo_video_path'] = recording_path
    context['action_logs'] = result
    return context


if __name__ == '__main__':
    context = {
        'request_id': 'test',
        'start_url': 'https://www.elevenlabs.io/',
        'user_goal': "Demonstrate the Conversational Agent creation platform with an example of a 'Sales Negotiation Coach'. Emphasise on features such as 'Voice Language', 'System Prompt'",
        'demo_steps': """1. Open elevenlabs.io website directly
2. Click 'Go to app'
3. Click 'Conversational AI' under products section in LHS
4. On the LHS choose 'Agents' -> Click 'Create an Ai Agent' -> 'Blank template'
5. Provide name as 'Sales Negotiation Coach' -> 'Create Agent' 
6. Select 'Agent Language' as 'Dutch' -> Input the 'System prompt' as something related to Negotiation coach.
7. Finally click 'Test AI Agent' and end.
"""
    }
    asyncio.run(generateDemoVideo(context))
    print(context)