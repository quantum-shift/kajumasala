import os
from langchain_openai import ChatOpenAI
from browser_use import Agent
from browser_use import BrowserConfig, Browser, BrowserContextConfig
import asyncio
from dotenv import load_dotenv
from pathlib import Path

import cv2
import numpy as np
import pyautogui
# import mss
# import pyscreenrec
from time import time
import threading
import traceback

load_dotenv()

config = BrowserConfig(
    headless=False,
    disable_security=True,
    chrome_instance_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
)


async def exploreAppBrowserUse(context):
    global recording
    request_id = context['request_id']
    start_url = context['start_url']
    user_goal = context['user_goal']
    explore_app_steps = context['explore_app_steps']

    with open("demoAgent.prompt", "r") as file:
        task_template = file.read()
    task = task_template.format(user_goal=user_goal, steps=explore_app_steps)

    # No recording needed for explore web app
    # recording_thread = threading.Thread(target=record_screen, args=(request_id,))
    # recording_thread.start()


    # recording_path = f"./recordings/{request_id}.avi"
    # fps = 20.0  # Lower FPS for pyautogui

    # # Get screen size
    # screen_size = pyautogui.size()
    # width, height = screen_size

    # fourcc = cv2.VideoWriter_fourcc(*"XVID")
    # out = cv2.VideoWriter(recording_path, fourcc, fps, (width, height))
    
    # recorder = pyscreenrec.ScreenRecorder()
    # recorder.start_recording("recording.mp4", 30, {
    #     	"mon": 1,
	# "left": 100,
	# "top": 100,
	# "width": 1000,
	# "height": 1000
    # })
    
    browser = Browser(config=config)
    contextConfig = BrowserContextConfig(
        browser_window_size={
            'width': 1600,
            'height': 1200
        },
        maximum_wait_page_load_time=2,
        #cookies_file='11labs_cookies.json'
    )
    action_list = []
    async with await browser.new_context(config=contextConfig) as browser_context:
        agent = Agent(
            task=task,
            llm=ChatOpenAI(model="gpt-4o"),
            use_vision=True,
            use_vision_for_planner=True,
            browser_context=browser_context,
            planner_interval=1000,
            initial_actions=[
                {'open_tab': {'url': start_url}}
            ]
        )

        result = await agent.run()
        action_list = agent.action_list
        print(result)
        app_features = []
        action_results = result.action_results()
        for v in action_results:
            app_features.append(v.extracted_content)
    
    await browser.close()
    # recording = False
    # print("Recording stopped")
    # recording_thread.join()
    # recorder.stop_recording()

    # out.release()
    # cv2.destroyAllWindows()  # Ensure all OpenCV windows are closed

    # context['video_path'] = f"./recordings/{request_id}.avi"
    context['explore_action_logs'] = '\n'.join(map(lambda x: x.current_state.next_goal, action_list))
    context['explore_app_features'] = app_features
    print("explore_app_features: UD")
    print(app_features)
    return context


if __name__ == "__main__":
    asyncio.run(exploreAppBrowserUse({
        'request_id': '123',
        'start_url': 'https://elevenlabs.io/app',
        'user_goal': 'explore the eleven labs web application',
        'demo_steps': """- Explore the web application for features
    """
    }))
