import pyaudio
import wave
import os
from gtts import gTTS
import keyboard
import time
from os import environ
import openai
from pygments.formatters import img
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
from transformers import pipeline
from pygame import mixer
from PIL import Image
from io import BytesIO
import requests
import matplotlib.pyplot as plt

# Set your OpenAI API key
openai.api_key = ''
class MessageList:
    def __init__(self, role, content):
        self.role = role
        self.content = content

data_list = []
filename = "recorded_audio.wav"
output_file = "output.mp3"
textUser = ""

def record_audio(duration=5):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    p = pyaudio.PyAudio()

    stream = p.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )

    print("Hold Space bar to start recording...\n")

    frames = []
    is_recording = False
    while True:
        if keyboard.is_pressed("space"):
            if not is_recording:
                mixer.quit()
                plt.close()
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

    wf = wave.open(filename, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()

def transcribe_audio():
    transcriber = pipeline(
        "automatic-speech-recognition", model="vinai/PhoWhisper-small"
    )
    output = transcriber(filename)["text"]
    print(f"You: ", end="")
    PrintText(output)
    dataMessage = MessageList("user", output + '.(Only when there is a request related to creating an image, do we write an additional word at the end of the sentence: UnlivableImage)')
    data_list.append(dataMessage)

    return output

def GetResultFromOpenAI():
    print("ChatGPT's thinking...\n")
    messages = [{"role": item.role, "content": item.content} for item in data_list]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0125",
            messages=messages
        )

        result = response.choices[0].message['content'].strip()
        if "UnlivableImage" in result:
            image_url = generate_image(textUser)
            if image_url:
                download_image(image_url, "generated_image.png")
        dataMessage = MessageList("assistant", result)
        data_list.append(dataMessage)
        return result.replace("(UnlivableImage)", "")
    except Exception as e:
        return None

def generate_image(prompt):
    try:
        response = openai.Image.create(
            model="dall-e-3",
              prompt=prompt,
              size="1024x1024",
              quality="standard",
              n=1,
        )
        image_url = response['data'][0]['url']
        return image_url
    except Exception as e:
        return None

def download_image(url, file_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        img.save(file_path)
        showImage(file_path)
    except Exception as e:
        return None

def text_to_speech_vietnamese(text):
    mixer.quit()
    if os.path.exists(output_file):
        os.remove(output_file)

    tts = gTTS(text=text, lang="vi")
    tts.save(output_file)
    print(f"ChatGPT's responding:...\n")
    time.sleep(1)
    print(f"ChatGPT: ", end="")
    PrintText(text)

    mixer.init()
    mixer.music.load(output_file)
    mixer.music.play()

def PrintText(text):
    for i in text:
        print(i, end="", flush=True)
        time.sleep(0.04)
    print("\n")
    
def showImage(file_path):
    try:
        img = img.imread(file_path)
        plt.imshow(img)
        plt.axis('off')
        plt.show(block=False)
    except Exception as e:
        None

if __name__ == "__main__":
    print(f"ChatGPT: ", end="")
    PrintText("Hello, Nice to meet you! Have a good day!")

    while True:
        # record_audio()
        textUser = transcribe_audio()
        response = GetResultFromOpenAI()
        if response:
            text_to_speech_vietnamese(response)
