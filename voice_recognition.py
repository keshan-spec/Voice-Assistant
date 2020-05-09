import time
import soundfile as sf
import sounddevice as sd
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from scipy.io.wavfile import write


class SpeechRecognition():
    def __init__(self):
        self.mic = sr.Microphone()
        self.r = sr.Recognizer()  # obtain source from the microphone

    def speech_to_text(self, audio):
        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            print("[+] You said : " + self.r.recognize_google(audio))
            self.listen()
        except sr.UnknownValueError:
            print("[-] Sorry, could not understand audio")
            time.sleep(1)
            self.listen()
        except sr.RequestError as e:
            print(
                "[-] Could not request results from Google Speech Recognition service; {0}".format(e))
            time.sleep(1)
            self.listen()
        except KeyboardInterrupt:
            print("[-] You stopped the program")

    # listens for audio from the mic
    # Speech recognition module
    def listen(self):
        try:
            with self.mic as source:
                print("Listening...")
                self.r.adjust_for_ambient_noise(source)
                src = self.r.listen(source)
            self.speech_to_text(src)
        except KeyboardInterrupt:
            print('[-] You stopped the program')
            return
        except AssertionError:
            print('[-] Error')

    # records the audio and saves it to a .wav file
    # sound device module
    def record(self):
        fs = 44100  # Sample rate
        seconds = 3  # Duration of recording
        audio_path = 'output.wav'  # audio path to save
        try:
            print("Listening: ")
            myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            sd.wait()  # Wait until recording is finished
            write(audio_path, fs, myrecording)  # Save as WAV file
            data, fs = sf.read(audio_path)  # Extract audio data and sampling rate from file
            sf.write(audio_path, data, fs)  # Save as FLAC file at correct sampling rate
            src = sr.AudioFile(audio_path)  # obtain source from the audio
            self.speech_to_text(src)
        except KeyboardInterrupt:
            print('[-] You stopped the program')
            return

    @staticmethod
    def speak(text):
        filename = "speak/audio.mp3"
        tts = gTTS(text)
        tts.save(filename)
        playsound(filename)


# speech class obj
speech = SpeechRecognition()
speech.listen()
