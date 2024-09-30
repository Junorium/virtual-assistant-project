import openai

openai.api_key = "" # import based on local machine
response_instruction = "" # how response will be crafted; change based on desired tone

def gen_response(prompt):
  response = openai.ChatCompletion.create(
    model="",
    messages=[
      {'role':'assistant',
      'content':response_instruction},
      {'role':'user',
      'content':prompt}
    ]
  )
