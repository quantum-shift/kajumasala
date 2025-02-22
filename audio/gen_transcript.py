import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


with open("./audio/action_log.txt", "r") as file:
    action_log = file.read()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant that presents actions taken by a user, to a group of people in a meeting. You are given a transcript of the actions taken by the user and you need to present the actions in a way that is easy to understand for the audience."
        },
        {
            "role": "user",
            "content": "Here is the action log: " + action_log
        }
    ],
    store=True
)

# print(completion.choices[0].message.content)

with open("./audio/transcript.txt", "w") as file:
    file.write(completion.choices[0].message.content)

