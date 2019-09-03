import time
import soundfile as sf
import sounddevice as sd
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from scipy.io.wavfile import write


r = sr.Recognizer()  # obtain source from the microphone
audio_path = 'audio/output.wav'
commands = ['open chrome', 'stop', 'whats the time', 'chrome', 'google']


def user_command(inp):
    for command in commands:
        if inp.lower() == command:
            if inp.lower() == 'stop':
                print('[-] Okay bye')
            else:
                print(command)
                time.sleep(2)
                record()
        else:
            time.sleep(2)
            record()


def speech_to_text(audio):
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("[+] You said : " + r.recognize_google(audio))
        user_command(r.recognize_google(audio))
    except sr.UnknownValueError:
        print("[-] Sorry, could not understand audio")
        time.sleep(2)
        record()
    except sr.RequestError as e:
        print(
            "[-] Could not request results from Google Speech Recognition service; {0}".format(e))
        time.sleep(2)
        record()


def speak(text):
    filename = "speak/audio.mp3"
    tts = gTTS(text)
    tts.save(filename)
    playsound(filename)


def listen(src):
    with src as source:
        r.adjust_for_ambient_noise(source)
        return r.record(source)


def record():
    fs = 44100  # Sample rate
    seconds = 3  # Duration of recording
    try:
        print("Listening: ")
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        write(audio_path, fs, myrecording)  # Save as WAV file
        # Extract audio data and sampling rate from file
        data, fs = sf.read(audio_path)
        # Save as FLAC file at correct sampling rate
        sf.write(audio_path, data, fs)

        src = sr.AudioFile(audio_path)  # obtain source from the audio
        audio = listen(src)
        speech_to_text(audio)
    except KeyboardInterrupt:
        print('[-] You stopped the program')


record()
