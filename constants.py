# constants.py

# ---------------------
# UI-переводы (интерфейс)
# ---------------------
UI_TRANSLATIONS = {
    'ru': {
        'window_title': 'Переводчик',
        'source_placeholder': 'Введите текст для перевода...',
        'target_placeholder': 'Перевод появится здесь...',
        'history_title': 'История переводов',
        'clear_history': 'Очистить историю',
        'language_selector_title': 'Выбор языка',
        'source_language': 'Исходный язык',
        'target_language': 'Целевой язык',
        'search_placeholder': 'Поиск языка...',
        'copy_message': 'Текст скопирован в буфер обмена',
        'clear_message': 'Текст очищен',
        'translation_started': 'Выполняется перевод...',
        'translation_completed': 'Перевод завершен',
        'translation_error': 'Ошибка перевода: {}',
        'playback_error': 'Ошибка воспроизведения: {}',
        'playback_started': 'Воспроизведение...',
        'delete_confirmation': 'Вы уверены, что хотите удалить эту запись?',
        'clear_confirmation': 'Вы уверены, что хотите очистить всю историю переводов?',
        'yes': 'Да',
        'no': 'Нет',
        'interface_language': 'Язык интерфейса:',
        'tts_not_supported': 'Озвучка не поддерживается для этого языка',
        'language_detection': 'Определение языка',
        'language_detection_message': 'Определен язык: {}. Хотите использовать его для перевода?',
        'language_not_supported': 'Определенный язык не поддерживается переводчиком',
        'language_detection_failed': 'Не удалось определить язык текста',
        'invalid_language': 'Неверный язык',
        'no_history': 'Нет данных',
        'no_text': 'Нет текста для озвучивания',
        'tts_not_supported': 'Этот язык не поддерживает озвучку',

    },
    'en': {
        'window_title': 'Translator',
        'source_placeholder': 'Enter text to translate...',
        'target_placeholder': 'Translation will appear here...',
        'history_title': 'Translation History',
        'clear_history': 'Clear History',
        'language_selector_title': 'Select Language',
        'source_language': 'Source Language',
        'target_language': 'Target Language',
        'search_placeholder': 'Search language...',
        'copy_message': 'Text copied to clipboard',
        'clear_message': 'Text cleared',
        'translation_started': 'Translation in progress...',
        'translation_completed': 'Translation completed',
        'translation_error': 'Translation error: {}',
        'playback_error': 'Playback error: {}',
        'playback_started': 'Playing...',
        'delete_confirmation': 'Are you sure you want to delete this entry?',
        'clear_confirmation': 'Are you sure you want to clear all translation history?',
        'yes': 'Yes',
        'no': 'No',
        'interface_language': 'Interface language:',
        'tts_not_supported': 'Text-to-speech is not supported for this language',
        'language_detection': 'Language Detection',
        'language_detection_message': 'Detected language: {}. Would you like to use it for translation?',
        'language_not_supported': 'The detected language is not supported by the translator',
        'language_detection_failed': 'Could not detect the language of the text',
        'invalid_language': 'Invalid language',
        'no_history': 'No data',
        'no_text': 'No text to speak',
        'tts_not_supported': 'This language is not supported for speech synthesis',
    }
}

# ------------------------------------
# Список языков для выпадающего списка
# ------------------------------------

LANGUAGES = {
    'af': {'ru': 'Африкаанс', 'en': 'Afrikaans'},
    'sq': {'ru': 'Албанский', 'en': 'Albanian'},
    'am': {'ru': 'Амхарский', 'en': 'Amharic'},
    'ar': {'ru': 'Арабский', 'en': 'Arabic'},
    'hy': {'ru': 'Армянский', 'en': 'Armenian'},
    'az': {'ru': 'Азербайджанский', 'en': 'Azerbaijani'},
    'eu': {'ru': 'Баскский', 'en': 'Basque'},
    'be': {'ru': 'Белорусский', 'en': 'Belarusian'},
    'bn': {'ru': 'Бенгальский', 'en': 'Bengali'},
    'bs': {'ru': 'Боснийский', 'en': 'Bosnian'},
    'bg': {'ru': 'Болгарский', 'en': 'Bulgarian'},
    'ca': {'ru': 'Каталанский', 'en': 'Catalan'},
    'ceb': {'ru': 'Цебуано', 'en': 'Cebuano'},
    'zh-cn': {'ru': 'Китайский (упрощённый)', 'en': 'Chinese (Simplified)'},
    'zh-tw': {'ru': 'Китайский (традиционный)', 'en': 'Chinese (Traditional)'},
    'co': {'ru': 'Корсиканский', 'en': 'Corsican'},
    'hr': {'ru': 'Хорватский', 'en': 'Croatian'},
    'cs': {'ru': 'Чешский', 'en': 'Czech'},
    'da': {'ru': 'Датский', 'en': 'Danish'},
    'nl': {'ru': 'Голландский', 'en': 'Dutch'},
    'en': {'ru': 'Английский', 'en': 'English'},
    'eo': {'ru': 'Эсперанто', 'en': 'Esperanto'},
    'et': {'ru': 'Эстонский', 'en': 'Estonian'},
    'fi': {'ru': 'Финский', 'en': 'Finnish'},
    'fr': {'ru': 'Французский', 'en': 'French'},
    'fy': {'ru': 'Фризский', 'en': 'Frisian'},
    'gl': {'ru': 'Галисийский', 'en': 'Galician'},
    'ka': {'ru': 'Грузинский', 'en': 'Georgian'},
    'de': {'ru': 'Немецкий', 'en': 'German'},
    'el': {'ru': 'Греческий', 'en': 'Greek'},
    'gu': {'ru': 'Гуджарати', 'en': 'Gujarati'},
    'ht': {'ru': 'Гаитянский креольский', 'en': 'Haitian Creole'},
    'ha': {'ru': 'Хауса', 'en': 'Hausa'},
    'haw': {'ru': 'Гавайский', 'en': 'Hawaiian'},
    'he': {'ru': 'Иврит', 'en': 'Hebrew'},
    'hi': {'ru': 'Хинди', 'en': 'Hindi'},
    'hmn': {'ru': 'Хмонг', 'en': 'Hmong'},
    'hu': {'ru': 'Венгерский', 'en': 'Hungarian'},
    'is': {'ru': 'Исландский', 'en': 'Icelandic'},
    'ig': {'ru': 'Игбо', 'en': 'Igbo'},
    'id': {'ru': 'Индонезийский', 'en': 'Indonesian'},
    'ga': {'ru': 'Ирландский', 'en': 'Irish'},
    'it': {'ru': 'Итальянский', 'en': 'Italian'},
    'ja': {'ru': 'Японский', 'en': 'Japanese'},
    'jw': {'ru': 'Яванский', 'en': 'Javanese'},
    'kn': {'ru': 'Каннада', 'en': 'Kannada'},
    'kk': {'ru': 'Казахский', 'en': 'Kazakh'},
    'km': {'ru': 'Кхмерский', 'en': 'Khmer'},
    'ko': {'ru': 'Корейский', 'en': 'Korean'},
    'ku': {'ru': 'Курдский', 'en': 'Kurdish'},
    'ky': {'ru': 'Киргизский', 'en': 'Kyrgyz'},
    'lo': {'ru': 'Лаосский', 'en': 'Lao'},
    'la': {'ru': 'Латынь', 'en': 'Latin'},
    'lv': {'ru': 'Латвийский', 'en': 'Latvian'},
    'lt': {'ru': 'Литовский', 'en': 'Lithuanian'},
    'lb': {'ru': 'Люксембургский', 'en': 'Luxembourgish'},
    'mk': {'ru': 'Македонский', 'en': 'Macedonian'},
    'mg': {'ru': 'Малагасийский', 'en': 'Malagasy'},
    'ms': {'ru': 'Малайский', 'en': 'Malay'},
    'ml': {'ru': 'Малаялам', 'en': 'Malayalam'},
    'mt': {'ru': 'Мальтийский', 'en': 'Maltese'},
    'mi': {'ru': 'Маори', 'en': 'Maori'},
    'mr': {'ru': 'Маратхи', 'en': 'Marathi'},
    'mn': {'ru': 'Монгольский', 'en': 'Mongolian'},
    'my': {'ru': 'Бирманский', 'en': 'Myanmar'},
    'ne': {'ru': 'Непальский', 'en': 'Nepali'},
    'no': {'ru': 'Норвежский', 'en': 'Norwegian'},
    'ny': {'ru': 'Ньянджа', 'en': 'Nyanja'},
    'or': {'ru': 'Ория', 'en': 'Odia'},
    'ps': {'ru': 'Пушту', 'en': 'Pashto'},
    'fa': {'ru': 'Персидский', 'en': 'Persian'},
    'pl': {'ru': 'Польский', 'en': 'Polish'},
    'pt': {'ru': 'Португальский', 'en': 'Portuguese'},
    'pa': {'ru': 'Пенджабский', 'en': 'Punjabi'},
    'ro': {'ru': 'Румынский', 'en': 'Romanian'},
    'ru': {'ru': 'Русский', 'en': 'Russian'},
    'sm': {'ru': 'Самоанский', 'en': 'Samoan'},
    'gd': {'ru': 'Шотландский гэльский', 'en': 'Scots Gaelic'},
    'sr': {'ru': 'Сербский', 'en': 'Serbian'},
    'st': {'ru': 'Сесото', 'en': 'Sesotho'},
    'sn': {'ru': 'Шона', 'en': 'Shona'},
    'sd': {'ru': 'Синдхи', 'en': 'Sindhi'},
    'si': {'ru': 'Сингальский', 'en': 'Sinhala'},
    'sk': {'ru': 'Словацкий', 'en': 'Slovak'},
    'sl': {'ru': 'Словенский', 'en': 'Slovenian'},
    'so': {'ru': 'Сомали', 'en': 'Somali'},
    'es': {'ru': 'Испанский', 'en': 'Spanish'},
    'su': {'ru': 'Сунданский', 'en': 'Sundanese'},
    'sw': {'ru': 'Суахили', 'en': 'Swahili'},
    'sv': {'ru': 'Шведский', 'en': 'Swedish'},
    'tl': {'ru': 'Тагальский', 'en': 'Tagalog'},
    'tg': {'ru': 'Таджикский', 'en': 'Tajik'},
    'ta': {'ru': 'Тамильский', 'en': 'Tamil'},
    'tt': {'ru': 'Татарский', 'en': 'Tatar'},
    'te': {'ru': 'Телугу', 'en': 'Telugu'},
    'th': {'ru': 'Тайский', 'en': 'Thai'},
    'tr': {'ru': 'Турецкий', 'en': 'Turkish'},
    'tk': {'ru': 'Туркменский', 'en': 'Turkmen'},
    'uk': {'ru': 'Украинский', 'en': 'Ukrainian'},
    'ur': {'ru': 'Урду', 'en': 'Urdu'},
    'ug': {'ru': 'Уйгурский', 'en': 'Uyghur'},
    'uz': {'ru': 'Узбекский', 'en': 'Uzbek'},
    'vi': {'ru': 'Вьетнамский', 'en': 'Vietnamese'},
    'cy': {'ru': 'Валлийский', 'en': 'Welsh'},
    'xh': {'ru': 'Коса', 'en': 'Xhosa'},
    'yi': {'ru': 'Идиш', 'en': 'Yiddish'},
    'yo': {'ru': 'Йоруба', 'en': 'Yoruba'},
    'zu': {'ru': 'Зулу', 'en': 'Zulu'},
}