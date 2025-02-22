from langchain_openai import ChatOpenAI
from browser_use import Agent
from browser_use import BrowserConfig, Browser, BrowserContextConfig
import asyncio
from dotenv import load_dotenv
from pathlib import Path

import cv2
import numpy as np
import pyautogui
import mss
import pyscreenrec
from time import time

load_dotenv()

config = BrowserConfig(
    headless=False,
    disable_security=True,
    chrome_instance_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
)

def createTempDir(req_id):
    dir_path = f"./recordings/{req_id}"

    directory = Path(dir_path)
    directory.mkdir(parents=True, exist_ok=True)
    return dir_path

# async def record_screen(out, fps):
#     """Continuously capture the screen while the agent is running."""
#     with mss.mss() as sct:
#         screen = sct.monitors[1]  # Capture the full screen
#         frame_time = 1 / fps
#         while True:
#             start_time = time()
#             print("Taking a screenshot")
            
#             screenshot = sct.grab(screen)  # Capture frame
#             frame = np.array(screenshot)  # Convert to numpy array
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)  # Convert to OpenCV BGR format
#             out.write(frame)  # Write frame to video file

#             # Sleep to maintain the desired FPS
#             elapsed_time = time() - start_time
#             await asyncio.sleep(max(0, frame_time - elapsed_time))

async def generateDemoVideo(context):
    request_id = context['request_id']
    start_url = context['start_url']
    user_goal = context['user_goal']
    demo_steps = context['demo_steps']

    with open("demoAgent.prompt", "r") as file:
        task_template = file.read()
    task = task_template.format(user_goal=user_goal, steps=demo_steps)

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
        #cookies_file='11labs_cookies.json'
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
    # recorder.stop_recording()

    # out.release()
    # cv2.destroyAllWindows()  # Ensure all OpenCV windows are closed

    context['demo_video_path'] = ""
    context['action_logs'] = result
    return context

asyncio.run(generateDemoVideo({
    'request_id': '123',
    'start_url': 'https://elevenlabs.io/app',
    'user_goal': 'create a negotiation coach conversational agent',
    'demo_steps': """- Click 'Conversational AI' under products section in LHS
"""
}))