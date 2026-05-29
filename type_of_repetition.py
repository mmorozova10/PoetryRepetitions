from transcription import make_transcription
from collections import Counter
from itertools import combinations

VOWELS = ('U0', 'U', 'O0', 'O', 'A0', 'A', 'E0', 'E', 'Y0', 'Y', 'I0', 'I')


class PoemRepetitions:
    """
    Класс для поиска повторов внутри любой строки стихотворения.
    """

    def __init__(self, filename: str) -> None:
        """
        Инициализирующий метод.
        :param filename: имя файла со стихотворением
        """
        with open(filename, 'r') as file:
            self.lines = file.readlines()
        self.transcription = []
        for line in self.lines:
            self.transcription.append(make_transcription(line))

    def __str__(self) -> str:
        """
        Возвращает строку с каждой строкой стихотворния и ее транскрипцией.
        :return: str
        """
        str_result = ''
        for i in range(len(self.lines)):
            if self.lines[i].split():
                transcription = ' '.join(self.transcription[i])
                str_result += self.lines[i] + transcription + '\n'
        return str_result

    def check_repetitions(self, index_of_line: int) -> bool:
        """
        Ищет повторы в выбранной строке и выводит на экран.
        :param index_of_line: номер строки
        :return: True если есть повтор, False иначе
        """
        if self.lines[index_of_line].split():
            print(self.lines[index_of_line].strip())
            print('Транскрипция: ' + ' '.join(self.transcription[index_of_line]))
            print(print_transcription_no_cons(self.transcription[index_of_line]))
            transcription_only_cons = [phoneme for phoneme in self.transcription[index_of_line] if
                                       phoneme not in VOWELS]
            transcription_only_cons = delete_palatalization(transcription_only_cons)
            phonemes = Counter(transcription_only_cons)
            repetitions = search_repetitions(transcription_only_cons, phonemes)
            if repetitions:
                print_all_repetitions(self.transcription[index_of_line], transcription_only_cons, repetitions)
                print()
                return True
            else:
                print()
                return True
        else:
            print('Пустая строка')
            return False


def find_all_sublist_indices(line: list, comb: set) -> list:
    """
    Функция для поиска всех подсписков списка line, являщихся перестановками множества comb
    :param line: список фонем транскрипции строки стихотворения
    :param comb: множество фонем, перестановки которых нужно найти
    :return: список из (индекс-вхождения, подстрока), если есть повторение длины больше 1
    """
    result = list()
    n = len(comb)
    for i in range(len(line) - n + 1):
        if set(line[i:i + n]) == comb:
            result.append((i, line[i:i + n]))

    # проверка на то, что повторение длины больше 1
    if len(result) > 1:
        return result
    else:
        return []


def choose_sequence(list_of_sublists: list) -> list:
    """
    В списке повторений ищет те, что не пересекаются внутри строки.
    :param list_of_sublists: список повторений из (индекс-вхождения, подстрока)
    :return: список повторений из (индекс-вхождения, подстрока), где расстояние между индексами вхождения больше, чем длина подстроки
    """
    if not list_of_sublists:
        return []

    result = [list_of_sublists[0]]
    comb_length = len(list_of_sublists[0][1])

    for i in list_of_sublists:
        if i[0] - result[-1][0] >= comb_length:
            result.append(i)

    if len(result) > 1:
        return result
    else:
        return []


def search_repetitions(line_transcription: list, counter_of_phonemes: Counter) -> dict:
    """
    Вычисляет все перестановки всех длин от 2 до len_repetition раз из фонем, встречаемых в строке
    более, чем len_repetition раз, и находит их вхожения в транскрипцию
    :param line_transcription: транскрипция без гласных
    :param counter_of_phonemes: количество вхождений  в транскрипцию каждой фонемы, вычисленное с помощью Counter()
    """
    counter_only_repeated_phonemes = [x[0] for x in counter_of_phonemes.most_common() if x[1] >= 2]
    result = dict()
    for len_comb in range(2, len(counter_only_repeated_phonemes) + 1):
        combinations_of_phonemes = combinations(counter_only_repeated_phonemes, len_comb)
        for comb in combinations_of_phonemes:
            comb1 = set(comb)
            entries = choose_sequence(find_all_sublist_indices(line_transcription, comb1))  # поиск вхождений
            result[comb] = entries
    return result


def delete_palatalization(line_transcription: list) -> list:
    """
    Убирает из элементов транскрипции все обозначения палатализации согласных.
    :param line_transcription: транскрипция
    :return: транскрипция (список) без палатализации и ударения
    """
    result = []
    for element in line_transcription:
        if element[-1] == '0':
            result.append(element[:-1])
        else:
            result.append(element)
    return result


def print_transcription_no_cons(original_transcription: list) -> str:
    """
    Функция для вывода транскрипции без согласных
    :param original_transcription: транскрипция
    :return: строка с согласными фонемами через нижний прочерк на месте гласных, разделенные пробелами
    """
    result = []
    for i in original_transcription:
        if i in VOWELS:
            result.append('_' * len(i))
        else:
            result.append(i)
    return 'Без гласных:  ' + ' '.join(result) + '\n'


def print_all_repetitions(original_transcription: list, transcription_no_cons: list, repetitions: dict) -> None:
    """
    Функция для вывода на экран всех повторов
    :param original_transcription: полная транскрипция (список фонем)
    :param transcription_no_cons: транскрипция без согласных (список фонем)
    :param repetitions: список повторов
    """
    for repetition in repetitions.items():
        result = ''
        list_rep_res = []
        list_repetitions = ['_'] * len(transcription_no_cons)
        if repetition[1]:
            for pair in repetition[1]:
                for i, el in enumerate(pair[1]):
                    list_repetitions[pair[0] + i] = el
            q = 0
            for i in original_transcription:
                if i in VOWELS:
                    list_rep_res.append('_' * len(i))
                elif list_repetitions[q] == transcription_no_cons[q]:
                    list_rep_res.append(i)
                    q += 1
                else:
                    list_rep_res.append('_' * len(i))
                    q += 1
            result += 'Повтор:       ' + ' '.join(list_rep_res)
            print(result)


filename = input("Введите имя файла: ")
if filename:
    poem = PoemRepetitions(filename)
else:
    poem = PoemRepetitions('texts/poems/test.txt')

index = input("Введите номер строки: ")
if index:
    poem.check_repetitions(int(index))
else:
    for line_index in range(len(poem.lines)):
        poem.check_repetitions(line_index)
