import os 
from google.cloud import translate_v2 as translate 

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/daniel/workspace/python/live-chat-translator/creds/google_creds.json'

def translate(text, target, translate_client = translate.Client()):
	'''
	Google Cloud Translation API will take text and the desired
	translated language which Google has a list of supported languages
	here: https://cloud.google.com/translate/docs/languages 

	:return: dict of results containing input, translatedText, and
			 detectedSourceLanguage
	'''

	result = translate_client.translate(text, target_language=target)

	return result['translatedText']

print(translate('내 이름은 다니엘이야', 'en') + '\n')
print(translate('My name is Daniel', 'ko'))
