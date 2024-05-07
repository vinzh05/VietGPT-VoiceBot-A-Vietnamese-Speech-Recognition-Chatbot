# VietGPT-VoiceBot-A-Vietnamese-Speech-Recognition-Chatbot

VietGPT VoiceBot: Chatbot automatically recognizes Vietnamese voice and uses the ChatGPT API for natural language interaction.

## Installation
1. **PyAudio**: 
  - Use pip to install PyAudio:
     ```bash
     pip install pyaudio
     ```

2. **Requests**: 
  - Use pip to install Requests:
     ```bash
     pip install requests
     ```

3. **gTTS (Google Text-to-Speech)**: 
  - Use pip to install gTTS:
     ```bash
     pip install gtts
     ```

4. **Keyboard**: 
  - Use pip to install Keyboard:
     ```bash
     pip install keyboard
     ```

5. **Pygame**:
  - Use pip to install pygame
     ```bash
     pip install pygame
     ```

6. **Transformers**: 
  - Use pip to install Transformers
     ```bash
     pip install transformers
     ```

## Record audio

### I use python's pyaudio library to record voice and write it to an input .wav file

- record_audio

    ```bash
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
                is_recording = True
        else:
            if is_recording:
                time.sleep(2)
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
    ```
    
## Speech auto Recognition

### I use Phowhisper's transformers library developed by VinAI Company to listen and understand Vietnamese or English language, from which I can output the words you say.

- Transcrible language
  
  ```bash
    transcriber = pipeline("automatic-speech-recognition", model="vinai/PhoWhisper-small")
    output = transcriber(filename)['text']
  ```
  
## Connect openAI

### I use the API provided by openAI to chat, interact and ask questions with chatGPT.

- Connect with openAI
  ```bash
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
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()['choices'][0]['message']['content']
        return result
    else:
        print("Error:", response.status_code, response.text)
  ```

## Text to speech with Google

### I use the gTTS library made by Google to convert text to audio and play it to listener

- Text to speech   
    ```bash
    def text_to_speech_vietnamese(text):
    mixer.quit()
    if os.path.exists(output_file):
        os.remove(output_file)
        
    tts = gTTS(text=text, lang='vi')
    tts.save(output_file)

    mixer.init()
    mixer.music.load(output_file)
    mixer.music.play()
    
Authors
-------

-   BUI QUANG VINH
-   Contact: [BUI QUANG VINH](https://www.facebook.com/Vinzh05)


Donations
---------

Support the ongoing development and improvement of SeleniumSupport:

-   Donate via [Binance](https://www.binance.com/) Address: TRvXSzxnjDWTTi1fnouqjFvb2YNzG5RqsZ 
-   Donate via [Momo](https://momo.vn/) Address: 0974602103
-   Donate via [Paypal](https://www.paypal.com/) Address: quangvinhb167@gmail.com
-   Support on [Telegram](https://t.me/Vinzh05)
-   Support on [Facebook](https://www.facebook.com/Vinzh05)
