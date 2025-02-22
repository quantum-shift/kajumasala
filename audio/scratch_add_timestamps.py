import re
import datetime

def add_timestamp_to_log(log_string, start_time_ist):
    """Adds a timestamp to each line of a log string, incrementing by one second per line.

    Args:
        log_string (str): The log string to add timestamps to.
        start_time_ist (datetime): The starting datetime object in IST.

    Returns:
        str: The log string with timestamps added to each line.
    """
    lines = log_string.splitlines()
    timestamped_lines = []
    current_time = start_time_ist

    for line in lines:
        timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
        timestamped_lines.append(f"[{timestamp}] {line}")
        current_time += datetime.timedelta(seconds=1)

    return "\n".join(timestamped_lines)

log_data = """
INFO     [browser_use] BrowserUse logging setup complete with level info
INFO     [root] Anonymized telemetry enabled. See https://docs.browser-use.com/development/telemetry for more information.
/Users/blr1/Documents/elabs/kajumasala/myenv/lib/python3.11/site-packages/browser_use/agent/message_manager/views.py:59: LangChainBetaWarning: The function `load` is in beta. It is actively being worked on, so the API may change.
  value['message'] = load(value['message'])
INFO     [agent] 🚀 Starting task: Got to elevenlabs.io and try to create a conversational ai agent
INFO     [agent] 📍 Step 1
INFO     [agent] 👍 Eval: Success - The browser is ready for a new action.
INFO     [agent] 🧠 Memory: Starting task. Need to search for elevenlabs.io and explore for creating a conversational AI agent.
INFO     [agent] 🎯 Next goal: Search for elevenlabs.io on Google.
INFO     [agent] 🛠️  Action 1/1: {"input_text":{"index":0,"text":"elevenlabs.io"}}
INFO     [controller] ⌨️  Input elevenlabs.io into index 0
INFO     [agent] 📍 Step 2
INFO     [agent] 👍 Eval: Success - 'elevenlabs.io' was entered and suggestions are displayed.
INFO     [agent] 🧠 Memory: Starting task. Entered 'elevenlabs.io' to search. Next step is to navigate to elevenlabs.io and explore creating a conversational AI agent.
INFO     [agent] 🎯 Next goal: Click the suggestion for elevenlabs.io/app/conversational-ai/agents to explore creating a conversational AI agent.
INFO     [agent] 🛠️  Action 1/1: {"click_element":{"index":10}}
INFO     [controller] 🖱️  Clicked button with index 10:
INFO     [agent] 📍 Step 3
INFO     [agent] 👍 Eval: Success - Navigated to the ElevenLabs page successfully with options to create or try AI agents.
INFO     [agent] 🧠 Memory: Successfully navigated to https://elevenlabs.io/app/conversational-ai/agents. Options to create or try different AI agents are available.
INFO     [agent] 🎯 Next goal: Click on 'Create this AI agent' to initiate creating a conversational AI agent
INFO     [agent] 🛠️  Action 1/1: {"click_element":{"index":22}}
INFO     [controller] 🖱️  Clicked button with index 22: Create this AI agent
INFO     [agent] 📍 Step 4
INFO     [agent] 👍 Eval: Success - Attempted to create but needed to reload options due to 'Create this AI agent' being in loading state.
INFO     [agent] 🧠 Memory: Successfully reached elevenlabs.io with options for conversational AI agents. Previously tried creating an agent but faced a loading issue.
INFO     [agent] 🎯 Next goal: Click 'Start from blank' to initiate a new AI agent creation.
INFO     [agent] 🛠️  Action 1/1: {"click_element":{"index":23}}
WARNING  [controller] Element not clickable with index 23 - most likely the page changed
INFO     [agent] 📍 Step 5
INFO     [agent] ⚠ Eval: Failed - The interaction with 'Create this AI agent' resulted in an error, possibly due to it being disabled or not present as expected.
INFO     [agent] 🧠 Memory: Currently on the ElevenLabs agent creation page. Previously tried interacting with 'Create this AI agent' button which was not successful due to it not being available.
INFO     [agent] 🎯 Next goal: Switch to setting up the AI agent by filling the required details like agent name, first message, and system prompt.
INFO     [agent] 🛠️  Action 1/3: {"input_text":{"index":19,"text":"Eric the Support Agent"}}
INFO     [agent] 🛠️  Action 2/3: {"input_text":{"index":33,"text":"Hi, I'm Eric. How can I help you today?"}}
INFO     [agent] 🛠️  Action 3/3: {"input_text":{"index":34,"text":"You are a support agent named Eric. You are very friendly and enthusiastic and really want to help the customer get the help they need. Answer in 3 to 7 sentences in most cases."}}
INFO     [controller] ⌨️  Input Eric the Support Agent into index 19
INFO     [agent] Something new appeared after action 1 / 3
INFO     [agent] 📍 Step 6
INFO     [agent] 👍 Eval: Success - The agent information was partially entered, and the new screen shows related fields for completion.
INFO     [agent] 🧠 Memory: The AI agent named 'Eric the Support Agent' is being set up. Filling the 'First Message' and 'System Prompt' fields is in progress. Need to save these changes.
INFO     [agent] 🎯 Next goal: Complete filling the 'System Prompt' and save the setup by clicking 'Save'.
INFO     [agent] 🛠️  Action 1/2: {"input_text":{"index":34,"text":"You are a support agent named Eric. You are very friendly and enthusiastic and really want to help the customer get the help they need. Answer in 3 to 7 sentences in most cases."}}
INFO     [agent] 🛠️  Action 2/2: {"click_element":{"index":39}}
INFO     [agent] 📍 Step 7
INFO     [agent] 👍 Eval: Success - Fields for the conversational AI agent are almost filled and ready for saving.
INFO     [agent] 🧠 Memory: Agent 'Eric the Support Agent' is set up with a first message and system prompt. Ready to save the changes.
INFO     [agent] 🎯 Next goal: Finalize the creation of the AI agent by saving the settings.
INFO     [agent] 🛠️  Action 1/1: {"click_element":{"index":49}}
INFO     [controller] 🖱️  Clicked button with index 49: Save
INFO     [agent] 📍 Step 8
INFO     [agent] 👍 Eval: Success - The agent has been set up successfully and is ready to be utilized.
INFO     [agent] 🧠 Memory: The conversational AI agent 'Eric the Support Agent' creation process is complete. All fields were successfully filled and settings configured.
INFO     [agent] 🎯 Next goal: Finalize the task by confirming the successful creation of the AI agent.
INFO     [agent] 🛠️  Action 1/1: {"done":{"text":"Successfully created a conversational AI agent named 'Eric the Support Agent'. The agent is set up with an initial greeting and system prompt to assist customers effectively."}}
INFO     [agent] 📄 Result: Successfully created a conversational AI agent named 'Eric the Support Agent'. The agent is set up with an initial greeting and system prompt to assist customers effectively.
INFO     [agent] ✅ Task completed successfully... AgentHistoryList(all_results=[ActionResult(is_done=False, extracted_content='⌨️  Input elevenlabs.io into index 0', error=None, include_in_memory=True), ActionResult(is_done=False, extracted_content='🖱️  Clicked button with index 10: ', error=None, include_in_memory=True), ActionResult(is_done=False, extracted_content='🖱️  Clicked button with index 22: Create this AI agent', error=None, include_in_memory=True), ActionResult(is_done=False, extracted_content=None, error='Failed to click element: <button class="relative inline-flex items-center justify-center whitespace-nowrap text-sm font-medium transition-colors duration-200 focus-ring disabled:pointer-events-auto bg-background/20 border border-subtle text-foreground shadow-none hover:bg-gray-alpha-50 active:bg-gray-alpha-100 disabled:bg-background disabled:text-gray-400 h-9 px-[12px] rounded-[10px] w-full" disabled=""> [interactive, top, highlight:23, in-viewport]. Error: Element: <button class="relative inline-flex items-center justify-center whitespace-nowrap text-sm font-medium transition-colors duration-200 focus-ring disabled:pointer-events-auto bg-background/20 border border-subtle text-foreground shadow-none hover:bg-gray-alpha-50 active:bg-gray-alpha-100 disabled:bg-background disabled:text-gray-400 h-9 px-[12px] rounded-[10px] w-full" disabled=""> [interactive, top, highlight:23, in-viewport] not found', include_in_memory=False), ActionResult(is_done=False, extracted_content='⌨️  Input Eric the Support Agent into index 19', error=None, include_in_memory=True), ActionResult(is_done=False, extracted_content='Something new appeared after action 1 / 3', error=None, include_in_memory=True), ActionResult(is_done=False, extracted_content='🖱️  Clicked button with index 49: Save', error=None, include_in_memory=True), ActionResult(is_done=True, extracted_content="Successfully created a conversational AI agent named 'Eric the Support Agent'. The agent is set up with an initial greeting and system prompt to assist customers effectively.", error=None, include_in_memory=False)], all_model_outputs=[{'input_text': {'index': 0, 'text': 'elevenlabs.io'}, 'interacted_element': None}, {'click_element': {'index': 10}, 'interacted_element': DOMHistoryElement(tag_name='cr-searchbox-match', xpath='div/div/cr-searchbox-match[6]', highlight_index=10, entire_parent_branch_path=['ntp-app', 'div', 'div', 'cr-searchbox', 'div', 'cr-searchbox-dropdown', 'div', 'div', 'div', 'cr-searchbox-match'], attributes={'tabindex': '0', 'role': 'option', 'aria-label': 'AI Voice Generator & Text to Speech | ElevenLabs elevenlabs.io/app/conversational-ai/agents location from history, press tab then enter to remove suggestion.'}, shadow_root=True, css_selector='div > div > cr-searchbox-match:nth-of-type(6)[role="option"][aria-label="AI Voice Generator & Text to Speech | ElevenLabs elevenlabs.io/app/conversational-ai/agents location from history, press tab then enter to remove suggestion."]', page_coordinates=None, viewport_coordinates=None, viewport_info=None)}, {'click_element': {'index': 22}, 'interacted_element': DOMHistoryElement(tag_name='button', xpath='html/body/div/div[2]/div[3]/div[2]/div/main/div/div/div[3]/button', highlight_index=22, entire_parent_branch_path=['div', 'div', 'div', 'div', 'div', 'main', 'div', 'div', 'div', 'button'], attributes={'class': 'relative inline-flex items-center justify-center whitespace-nowrap text-sm font-medium transition-colors duration-200 focus-ring disabled:pointer-events-auto bg-foreground text-background shadow-none hover:bg-gray-alpha-800 active:bg-gray-alpha-700 disabled:bg-gray-alpha-400 disabled:text-gray-200 h-9 px-[12px] rounded-[10px] w-full'}, shadow_root=False, css_selector='html > body > div > div:nth-of-type(2) > div:nth-of-type(3) > div:nth-of-type(2) > div > main > div > div > div:nth-of-type(3) > button.relative.inline-flex.items-center.justify-center.whitespace-nowrap.text-sm.font-medium.transition-colors.duration-200.focus-ring.bg-foreground.text-background.shadow-none.h-9.w-full', page_coordinates=None, viewport_coordinates=None, viewport_info=None)}, {'click_element': {'index': 23}, 'interacted_element': DOMHistoryElement(tag_name='button', xpath='html/body/div/div[2]/div[3]/div[2]/div/main/div/div/div[3]/button[2]', highlight_index=23, entire_parent_branch_path=['div', 'div', 'div', 'div', 'div', 'main', 'div', 'div', 'div', 'button'], attributes={'class': 'relative inline-flex items-center justify-center whitespace-nowrap text-sm font-medium transition-colors duration-200 focus-ring disabled:pointer-events-auto bg-background/20 border border-subtle text-foreground shadow-none hover:bg-gray-alpha-50 active:bg
-gray-alpha-100 disabled:bg-background disabled:text-gray-400 h-9 px-[12px] rounded-[10px] w-full', 'disabled': ''}, shadow_root=False, css_selector='html > body > div > div:nth-of-type(2) > div:nth-of-type(3) > div:nth-of-type(2) > div > main > div > div > div:nth-of-type(3) > button:nth-of-type(2).relative.inline-flex.items-center.justify-center.whitespace-nowrap.text-sm.font-medium.transition-colors.duration-200.focus-ring.border.border-subtle.text-foreground.shadow-none.h-9.w-full', page_coordinates=None, viewport_coordinates=None, viewport_info=None)}, {'input_text': {'index': 19, 'text': 'Eric the Support Agent'}, 'interacted_element': DOMHistoryElement(tag_name='input', xpath='html/body/div/div[2]/div[3]/div[2]/div/main/div/div[2]/div/div/div/div/div/p/input', highlight_index=19, entire_parent_branch_path=['div', 'div', 'div', 'div', 'div', 'main', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'p', 'input'], attributes={'id': 'agent-name-input', 'class': 'px-1 border border-transparent hover:border-gray-100 bg-transparent rounded-lg focus:border-gray-900 focus:ring-gray-900 absolute inset-x-[calc(-1px_-_theme(space.1))] -inset-y-0.5 font-semibold text-lg', 'aria-label': 'name', 'placeholder': 'Agent name', 'name': 'name'}, shadow_root=False, css_selector='html > body > div > div:nth-of-type(2) > div:nth-of-type(3) > div:nth-of-type(2) > div > main > div > div:nth-of-type(2) > div > div > div > div > div > p > input.px-1.border.border-transparent.bg-transparent.rounded-lg.absolute.font-semibold.text-lg[id="agent-name-input"][aria-label="n...
"""

# Set the start time to 10:00 AM IST on the current date
start_time_ist = datetime.datetime(2025, 2, 22, 10, 0, 0)  # Year, month, day, hour, minute, second

timestamped_log = add_timestamp_to_log(log_data, start_time_ist)
print(timestamped_log)
