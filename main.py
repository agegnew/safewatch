import os
import openai
import base64

client = openai.OpenAI(
    api_key='a1c616ae-14a1-4aff-8662-d0627950b5ff',
    base_url="https://api.sambanova.ai/v1",
)
with open('/Users/igorsergeevic/Desktop/SafeWatch/test/qwe.jpg', 'rb') as f:
    f_data = f.read()
base64_string = base64.b64encode(f_data).decode('utf-8')
print(base64_string)
response = client.chat.completions.create(
    model='Llama-3.2-11B-Vision-Instruct',
    messages=[{"role": "system", "content": "You are a helpful assistant"}, {"role": "user", "content": f"{f_data} tell me what isn that on photo?"}],
    temperature=0.1,
    top_p=0.1
)

print(response.choices[0].message.content)

