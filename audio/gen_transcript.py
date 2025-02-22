import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gen_transcript(action_log, context):
    sys_prompt= "You are mimicing the actions of a user. You have the actions in a list of logs. You need to give a transcript for human consumption while you perform those actions. It should be in present tense and easy to understand for the audience. Start from the logs where it "
    if context:
        pass

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": sys_prompt
        },
        {
            "role": "user",
            "content": "Here is the action log: " + action_log
        },
        {
            "role": "user",
            "content": "Please convert it into present tense and present it in a way that is easy to understand for the audience." 
        }
    ],
    store=True
    )
    return completion.choices[0].message.content


if __name__ == "__main__":
    with open("./audio/action_log_filtered.txt", "r") as file:
        action_log = file.read()
    with open("./audio/transcript_test6.txt", "w") as file:
        file.write(gen_transcript(action_log, None))
