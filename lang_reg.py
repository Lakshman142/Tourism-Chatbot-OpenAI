from google.cloud import speech_v1p1beta1 as speech

client = speech.SpeechClient()

speech_file = "resources/multi.wav"
first_lang = "en-US"
second_lang = "es"

with open(speech_file, "rb") as audio_file:
    content = audio_file.read()

audio = speech.RecognitionAudio(content=content)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=44100,
    audio_channel_count=2,
    language_code=first_lang,
    alternative_language_codes=[second_lang],
)

print("Waiting for operation to complete...")
response = client.recognize(config=config, audio=audio)

for i, result in enumerate(response.results):
    alternative = result.alternatives[0]
    print("-" * 20)
    print("First alternative of result {}: {}".format(i, alternative))
    print("Transcript: {}".format(alternative.transcript))