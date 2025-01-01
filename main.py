# required dependencies
# pip install openai
# pip install google-cloud-speech
# pip install pyaudio

import os
import pyaudio
import wave
import openai
from google.cloud import speech
from google.cloud.speech import types, enums

# insert openai api key below
openai.api_key = "your_openai_api_key"  # Replace with your actual OpenAI API key
response_instruction = "Craft responses in an easy to understand tone, without lists or visual formats.  Treat response as if it will only be said."

# Google Cloud Service Account Key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path_to_your_service_account.json"

# Audio recording settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
WAVE_OUTPUT_FILENAME = "output.wav"

# Function to generate a response from OpenAI
def gen_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Replace with the desired OpenAI model
            messages=[
                {'role': 'assistant', 'content': response_instruction},
                {'role': 'user', 'content': prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error generating response: {e}")
        return None

# Function to transcribe audio using Google Cloud Speech-to-Text
def transcribe(audio_file_path):
    try:
        client = speech.SpeechClient()
        with open(audio_file_path, 'rb') as audio_file:
            content = audio_file.read()

        audio = types.RecognitionAudio(content=content)
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code="en-US"
        )

        response = client.recognize(config=config, audio=audio)

        # Combine transcriptions from all results
        transcript = " ".join([result.alternatives[0].transcript for result in response.results])
        return transcript
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None

# Function to record audio from the microphone
def record_audio():
    audio = pyaudio.PyAudio()

    # Start recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Recording... Press Ctrl+C to stop.")
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

# Main program flow
if __name__ == "__main__":
    print("Recording audio...")
    audio_file = record_audio()

    print("Transcribing audio...")
    transcription = transcribe(audio_file)
    if transcription:
        print("Transcription:", transcription)

        print("Generating response...")
        response = gen_response(transcription)
        if response:
            print("AI Response:", response)
