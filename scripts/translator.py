import json

class Translator:
    def __init__(self, default_language="en", current_lang: str="en"):
        self.translations = {}
        self.default_language = default_language
        self.current_language = current_lang
    
    def set_language(self, language):
        self.current_language = language

    def load_translations(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            self.translations = json.load(file)

    def translate(self, key, current_language=None):
        if current_language == None:
            current_language = self.current_language
        translated_text = self.translations.get(current_language, {}).get(key, self.translations.get(self.default_language, {}).get(key, f"Translation missing: {key}"))
        return translated_text