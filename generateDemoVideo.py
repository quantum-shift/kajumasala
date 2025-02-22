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

def createTempDir(req_id):
    dir_path = f"./recordings/{req_id}"

    directory = Path(dir_path)
    directory.mkdir(parents=True, exist_ok=True)
    return dir_path

# Flag to control the recording thread
recording = True

def record_screen():
    global recording
    # Set up parameters for video recording
    # screen_size = pyautogui.size()  # Get the size of the primary monitor
    fps = 20.0  # Frames per second to record

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")  # Codec for .avi file
    output = cv2.VideoWriter("screen_record.avi", fourcc, fps, (3024, 1964))

    while recording:
        print("Taking screenshot")
        # Capture the screen
        img = pyautogui.screenshot()

        # Convert the image to a numpy array
        frame = np.array(img)

        # Convert the frame to BGR (OpenCV uses BGR while pyautogui uses RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Write the frame to the video file
        # print(f"Writing frame to video: {frame.shape}, {frame}")
        output.write(frame)

        # Display the recording screen (optional)
        # cv2.imshow("Recording", frame)

        # Add a small delay to control frame rate
        if cv2.waitKey(1) == ord('q'):
            break

    # Release everything when job is finished
    output.release()
    cv2.destroyAllWindows()

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
    global recording
    request_id = context['request_id']
    start_url = context['start_url']
    user_goal = context['user_goal']
    demo_steps = context['demo_steps']

    with open("demoAgent.prompt", "r") as file:
        task_template = file.read()
    task = task_template.format(user_goal=user_goal, steps=demo_steps)

    # Create and start the recording thread
    recording_thread = threading.Thread(target=record_screen)
    recording_thread.start()


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
        print("I'm hereHJHHHHHHHHHHHH")
        print(result)
    
    await browser.close()
    recording = False
    print("Recording stopped")
    recording_thread.join()
    # recorder.stop_recording()

    # out.release()
    # cv2.destroyAllWindows()  # Ensure all OpenCV windows are closed

    context['demo_video_path'] = ""
    context['action_logs'] = '\n'.join(map(lambda x: x.current_state.next_goal, action_list))
    return context

if __name__ == "__main__":
    asyncio.run(generateDemoVideo({
        'request_id': '123',
        'start_url': 'https://elevenlabs.io/app',
        'user_goal': 'create a negotiation coach conversational agent',
        'demo_steps': """- Click 'Conversational AI' under products section in LHS
    """
    }))
