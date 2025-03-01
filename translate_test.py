from googletrans import Translator
import asyncio

from_lang = str(input("Choose 'from' language: (or 'enter' to English)\n") or "en")
to_lang = str(input("Choose 'to' language (or 'enter' to Russian):\n") or "ru")
translate_text = str(input("\nType text to translate:\n") or "Hello world")

async def main():
    translator = Translator()
    
    async def translate(
            from_lang: str, 
            to_lang: str,
            translate_text: str = "Hello world"
        ):
        
        result = await translator.translate(text=translate_text, dest=to_lang, src=from_lang)
        return result
        
    translated = await translate(
            from_lang=from_lang,
            to_lang=to_lang,
            translate_text=translate_text
        )
    print(translated.text)
    
asyncio.run(main())