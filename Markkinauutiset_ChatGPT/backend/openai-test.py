
from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

chatgpt_outpput = completion.choices[0].message
print(type(chatgpt_outpput))
print(chatgpt_outpput)
print('.-----')
print(completion.choices[0].message.content)
