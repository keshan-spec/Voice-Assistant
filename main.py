from classes.SpeechRecognition import SpeechRecognition
from classes.Translator import Translate

tr = Translate()
recognition = SpeechRecognition()


def user_command(inp):
    commands = ['open', 'stop', 'chrome', 'google', 'translate', 'set', 'language']
    s = inp.lower().split(" ")
    if s[0] in commands:
        print(f"Command match '{s[0]}'")
        if s[0] == 'language':
            print(f"Setting language {tr.LANGUAGES[s[1]]}")
            tr.set_defaults(tr.LANGUAGES[s[1]])
        if s[0] == 'translate':
            translated = tr.translate(inp)
            print(translated)
            recognition.speak(translated['text'])


while True:
    command = recognition.listen()
    if command:
        user_command(command)
    if command == 'quit':
        break
