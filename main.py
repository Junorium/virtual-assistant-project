# pip install openai
# pip install google-cloud-speech
# pip install pyaudio google-cloud-speech

import os
import pyaudio
import wave
import openai
from google.cloud import speech


openai.api_key = "" # import based on local machine
response_instruction = "" # how response will be crafted; change based on desired tone

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path_to_your_service_account.json"

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
WAVE_OUTPUT_FILENAME = "output.wav"

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

def transcribe(audio):
  return None

'''  
def record_audio():
    audio = pyaudio.PyAudio()

    # Start recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Recording...")
    frames = []

    try:
        while True:
            data = stream.read(CHUNK)
            frames.append(data)

    except KeyboardInterrupt:
        print("Finished recording.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded data as a WAV file
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    return WAVE_OUTPUT_FILENAME
'''
