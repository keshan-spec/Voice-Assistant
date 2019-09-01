import time
import soundfile as sf
import sounddevice as sd
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from scipy.io.wavfile import write


fs = 44100  # Sample rate
seconds = 3  # Duration of recording
r = sr.Recognizer()  # obtain source from the microphone
audio_path = 'audio/output.wav'


def speak(text):
    filename = "speak/audio.mp3"
    tts = gTTS(text)
    tts.save(filename)
    playsound(filename)


def listen(src):
    with src as source:
        r.adjust_for_ambient_noise(source)
        return r.record(source)


def speech_to_text(audio):
    text = r.recognize_google(audio)
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("You said : " + text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(e))


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


