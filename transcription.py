import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import re
from russian_g2p.russian_g2p.Accentor import Accentor
from russian_g2p.russian_g2p.Grapheme2Phoneme import Grapheme2Phoneme

my_accentor = Accentor()
my_transcriptor = Grapheme2Phoneme()

latin_symbols_translator = str.maketrans('', '', 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')

def add_accents(line: str) -> str:
    """
    Расставляет ударения
    :param line: строка произведения
    :return: строка произведения с отмеченными ударениями
    """
    list_of_lists = []
    words = line.lower().split()
    for word in words:
        list_of_lists.append([word])
    p = my_accentor.do_accents(list_of_lists)
    result = ''
    for word in p[0]:
        result += word + ' '
    return result

def make_transcription(line: str) -> list:
    """
    Убирает ненужные символы (латиницу), делит по знакам препинания и создает общую транскрипцию
    :param line: строка произведения
    :return: список фонем
    """
    # убирает латиницу
    removed_latin_symbols = line.translate(latin_symbols_translator)
    # делит по пунктуационным символам
    parts = re.split(r'[\W_]+', removed_latin_symbols)
    list_transcription = []
    # записывает транскрипцию в итоговый список
    for part in parts:
        if part.split():
            part = add_accents(part)
            list_transcription += my_transcriptor.phrase_to_phonemes(part)
    return list_transcription