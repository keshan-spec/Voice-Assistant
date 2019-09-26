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
        self.commands = ['open chrome', 'stop',
                         'whats the time', 'chrome', 'google', 'hello']

    def speak(self, text):
        filename = "speak/audio.mp3"
        tts = gTTS(text)
        tts.save(filename)
        playsound(filename)

    # gets the speech and checks for any command
    def user_command(self, inp):
        for command in self.commands:
            if inp.lower() == command:
                if inp.lower() == 'hello':
                    self.speak('Okay bye')
                else:
                    print(command)
                    audio = self.listen()
                    self.speech_to_text(audio)
            else:
                print("[-] No command")
                time.sleep(2)
                audio = self.listen()
                self.speech_to_text(audio)

    def speech_to_text(self, audio):
        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            print("[+] You said : " + self.r.recognize_google(audio))
            self.user_command(self.r.recognize_google(audio))
        except sr.UnknownValueError:
            print("[-] Sorry, could not understand audio")
            time.sleep(2)
            audio = self.listen()
            self.speech_to_text(audio)
        except sr.RequestError as e:
            print(
                "[-] Could not request results from Google Speech Recognition service; {0}".format(e))
            time.sleep(2)
            audio = self.listen()
            self.speech_to_text(audio)
        except KeyboardInterrupt:
            print("[-] You stopped the program")

    # listens for audio from the mic
    # Speech recognition module
    def listen(self):
        with self.mic as source:
            print("Listening...")
            self.r.adjust_for_ambient_noise(source)
            return self.r.listen(source)

    # records the audio and saves it to a .wav file
    # sounddevice module
    def record(self):
        fs = 44100  # Sample rate
        seconds = 3  # Duration of recording
        audio_path = 'audio/output.wav'  # audio path to save
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
            audio = self.listen()
            self.speech_to_text(audio)
        except KeyboardInterrupt:
            print('[-] You stopped the program')


# speech class obj
speech = SpeechRecognition()
audio = speech.listen()
speech.speech_to_text(audio)
