from gtts import gTTS
from playsound import playsound
import tempfile
import os
import gtts.langs

gtts_langs = gtts.lang.tts_langs()

def speak_text(text: str, lang: str, on_status=None):
    if not text.strip():
        return

    current_audio_file = None
    try:
        print(f"Input text: {text!r}")
        print(f"Language: {lang}")

        if lang not in gtts_langs:
            if on_status:
                on_status(f"playback_error: Language code {lang} not supported by gTTS")
            return

        # Используем код языка напрямую, без дополнительных преобразований
        gtts_lang = lang

        # Создаём временный файл
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            current_audio_file = temp_file.name

        if on_status:
            on_status("playback_started")

        # Создаём и сохраняем голос
        tts = gTTS(text=text, lang=gtts_lang)
        tts.save(current_audio_file)

        # Проигрываем
        playsound(current_audio_file)

        print("TEMP FILE PATH:", current_audio_file)
        print("EXISTS:", os.path.exists(current_audio_file))
        print("SIZE:", os.path.getsize(current_audio_file))
        print("IS STRING:", isinstance(current_audio_file, str))

    except Exception as e:
        if on_status:
            on_status(f"playback_error: {e}")
    finally:
        if current_audio_file and os.path.exists(current_audio_file):
            try:
                os.remove(current_audio_file)
            except Exception as e:
                print(f"Failed to remove temp file: {e}")