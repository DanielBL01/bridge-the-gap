import os 
from google.cloud import translate_v2 as translate 

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/daniel/workspace/python/live-chat-translator/creds/google_creds.json'

translate_client = translate.Client()

text = 'Hello, my name is Daniel'
target = 'ko'

result = translate_client.translate(text, target_language=target)

print(result)
