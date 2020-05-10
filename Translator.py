"""
Translator Author<https://github.com/keshan-spec/>
"""
from googletrans import Translator
from googletrans.constants import LANGCODES


class Translate:
    def __init__(self):
        self.LANGUAGES = LANGCODES
        self.translator = Translator()
        self.default_dest = 'en'
        self.default_src = 'auto'

    def translate(self, text, verbose=False):
        try:
            output = self.translator.translate(text, src=self.default_src, dest=self.default_dest)
            if not output.pronunciation:
                output.pronunciation = self._pronunciation(output.text)
            if verbose:
                for item in vars(output).items():
                    if not hasattr(item[1], 'items'):
                        print(item)
            return {"text": output.text, "pronouciation": output.pronunciation}
        except ValueError:
            print("[ERR] : The provided language(s) are invalid")
            return

    def _pronunciation(self, text):
        return self.translator.translate(text, dest=self.default_dest).pronunciation

    def set_defaults(self, dest, src='auto'):
        self.default_dest = dest
        self.default_src = src


if __name__ == '__main__':
    tr = Translate()
    # for item in tr.LANGUAGES.items():
    #     print(item)
    # lang = input("lang> ")
    tr.set_defaults('ja')
    text = ''
    print("<Type 'q' to quit>\n")
    while True:
        while not text:
            text = input("> ")
        if text == 'q': break
        print(tr.translate(text))
        text = input("> ")
