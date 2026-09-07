import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# pip install openai
# client = OpenAI()
# by default to getting the key using os.environ.get("OPEN_API_KEY")
# if you saved the key under a different environment variable name, you can do something like:

client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY")
)

completion = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
        {"role": "user", "content": "what is coding"}
    ]
)

print(completion.choices[0].message.content)