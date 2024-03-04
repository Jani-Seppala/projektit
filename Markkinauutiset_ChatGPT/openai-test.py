# from openai import OpenAI
# client = OpenAI()

# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#   ]
# )

# print(completion.choices[0].message)

# from openai import OpenAI
# client = OpenAI()

# try:
#     completion = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         max_tokens=150,  # Limit the response length
#         temperature=0.7,  # Adjust for creativity vs coherence
#         messages=[
#             {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#             {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#         ]
#     )
#     print(completion.choices[0].message)
# except Exception as e:
#     print(f"Encountered an error: {e}")
#     # Implement backoff strategy here (e.g., wait and retry)


from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)