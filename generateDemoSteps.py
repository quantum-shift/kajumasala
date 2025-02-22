from langchain_openai import ChatOpenAI
from browser_use import Agent
from browser_use import BrowserConfig, Browser, BrowserContextConfig
import asyncio
from dotenv import load_dotenv

load_dotenv()

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

user_query_based_steps = """1. Open elevenlabs.io website directly
2. Click 'Go to app'
3. Find {app_feature} 
4. Explore the {app_feature}
"""

explore_steps = """1. Open elevenlabs.io website directly
2. Click 'Go to app'
3. Explore the website for a while, figure out what features it has
4. Click on every possible surface and see what happens
5. Log of all the features and their descriptions

"""

def create_steps_prompt(context: dict) -> str:
    if not context.get('user_query'):
        raise RuntimeError("Missing user_query in generateDemoSteps.create_steps_prompt")
    
    context['user_goal'] = context.get('user_query')
    # context['demo_steps'] = steps
    context['demo_steps'] = user_query_based_steps.format(app_feature=context.get('app_feature'))
    
    # raise RuntimeError("Error path in generateDemoSteps.create_steps_prompt")

def explore_web_app(context: dict) -> str:
    # if not context.get('user_query'):
    #     raise RuntimeError("Missing user_query in generateDemoSteps.create_steps_prompt")
    
    context['user_goal'] = context.get('user_query')
    context['explore_app_steps'] = explore_steps
    
# async def generateDemoVideo(context):
#     request_id = context['request_id']
#     start_url = context['start_url']

#     with open("demoAgent.prompt", "r") as file:
#         task_template = file.read()
#     task = task_template.format(user_goal=user_goal, steps=demo_steps)

#     # Create and start the recording thread
#     recording_thread = threading.Thread(target=record_screen, args=(request_id,))
#     recording_thread.start()


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
    
    # browser = Browser(config=config)
    # contextConfig = BrowserContextConfig(
    #     browser_window_size={
    #         'width': 1600,
    #         'height': 1200
    #     },
    #     maximum_wait_page_load_time=2,
    #     #cookies_file='11labs_cookies.json'
    # )
    # action_list = []
    # async with await browser.new_context(config=contextConfig) as browser_context:
    #     agent = Agent(
    #         task=task,
    #         llm=ChatOpenAI(model="gpt-4o"),
    #         use_vision=True,
    #         use_vision_for_planner=True,
    #         browser_context=browser_context,
    #         planner_interval=1000,
    #         initial_actions=[
    #             {'open_tab': {'url': start_url}}
    #         ]
    #     )

    #     result = await agent.run()
    #     action_list = agent.action_list
    #     print("I'm hereHJHHHHHHHHHHHH")
    #     print(result)
    #     app_features = []
    #     action_results = result.action_results()
    #     for v in action_results:
    #         app_features.append(v.extracted_content)
    
    # await browser.close()
    # recording = False
    # print("Recording stopped")
    # recording_thread.join()
    # # recorder.stop_recording()

    # # out.release()
    # # cv2.destroyAllWindows()  # Ensure all OpenCV windows are closed

    # context['video_path'] = f"./recordings/{request_id}.avi"
    # context['action_logs'] = '\n'.join(map(lambda x: x.current_state.next_goal, action_list))
    # context['app_features'] = app_features
    # return context
