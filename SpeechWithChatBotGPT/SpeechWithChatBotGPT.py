import pyaudio
import wave
import requests
import json
import os
from gtts import gTTS
import keyboard
import time
import sys
import subprocess
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from transformers import pipeline
from pygame import mixer
import json
import re 

class MessageList:
    def __init__(self, role, Content):
        self.role = role
        self.Content = Content

data_list = []
filename = "recorded_audio.wav"
output_file = "output.mp3"

def record_audio(duration=5):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Hold Space bar to start recording...\n")

    frames = []
    is_recording = False
    while True:
        if keyboard.is_pressed('space'):
            if not is_recording:
                mixer.quit()
                print("Start Recording...\n")
                is_recording = True
        else:
            if is_recording:
                time.sleep(2)
                print("Recording Stopped\n")
                break

        if is_recording:
            data = stream.read(CHUNK)
            frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def transcribe_audio():
    transcriber = pipeline("automatic-speech-recognition", model="vinai/PhoWhisper-small")
    output = transcriber(filename)['text']
    print(f"You: ", end='')
    PrintText(output)
    dataMessage = MessageList("user", output)
    data_list.append(dataMessage)
    
    return output

def GetResultFromOpenAI(text):
    openai_api_key = "openai_api_key"
    url = "https://api.openai.com/v1/chat/completions"
        
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": json_data_list,
        "temperature": 1.1
    }
    print(f"ChatGPT's thinking...\n")
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()['choices'][0]['message']['content']
        result = result.replace("*", '')
        dataMessage = MessageList("assistant", result)
        data_list.append(dataMessage)
        return result
    else:
        print("Error:", response.status_code, response.text)
        
def text_to_speech_vietnamese(text):
    mixer.quit()
    if os.path.exists(output_file):
        os.remove(output_file)
        
    tts = gTTS(text=text, lang='vi')
    tts.save(output_file)
    print(f"ChatGPT's responding:...\n")
    time.sleep(1)
    print(f"ChatGPT: ", end='')
    PrintText(text)

    mixer.init()
    mixer.music.load(output_file)
    mixer.music.play()
    
def PrintText(text): 
    for i in text:
      print(i,end='' ,flush=True)
      time.sleep(0.04)
    print("\n")
      
if __name__ == "__main__":    

    print(f"ChatGPT: ", end='')
    
    PrintText("Hello, Nice to meet you! Have a good day for you!")
    while True:
        record_audio()
        text = transcribe_audio()
        json_data_list = [{"role": item.role, "content": item.Content} for item in data_list]
        response = GetResultFromOpenAI(text)
        text_to_speech_vietnamese(response)
    