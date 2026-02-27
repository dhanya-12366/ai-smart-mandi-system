from openai import OpenAI

client = OpenAI( base_url="https://api.featherless.ai/v1", api_key="rc_968eb230f2138f74c13024f72d6f65a279adac21aa7d7d0d402065e124371af2" )

response = client.chat.completions.create( model="deepseek-ai/DeepSeek-V3-0324", messages=[ {"role": "user", "content": "Hello!"} ] )

print(response.choices[0].message.content)