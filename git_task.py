import os
import enchant
from pathlib import Path

class CaesarsCipher:
    def __init__(self):
        self._message = ''
        self._key = None
        self.__symbols = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                          'abcdefghijklmnopqrstuvwxyz'
                          '1234567890 !?.')

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, new_key):
        if -1 < new_key < len(self.__symbols):
            self._key = new_key
        else:
            raise ValueError(f'Значение ключа должно находиться в диапазоне:'
                             f'от 0 до {len(self.__symbols) - 1}')

    def encrypt(self, message: str):
        encrypted_text = ''
        for i in message:
            symbol_index = self.__symbols.find(i)
            symbol_index += self._key
            if symbol_index >= len(self.__symbols):
                symbol_index -= len(self.__symbols)
            encrypted_text += self.__symbols[symbol_index]
        return encrypted_text

    def decrypt(self, message):
        decrypted_text = ''
        for symb in message:
            symbol_index = self.__symbols.find(symb)
            symbol_index -= self._key
            decrypted_text += self.__symbols[symbol_index]
        return decrypted_text


if __name__ == '__main__':

    directory_user = Path(input('Введите путь к папке для записи файла: '))
    if not directory_user.exists():
        print(f'Папка {str(directory_user)} не существует')
        exit()
    folder_path = str(directory_user)
    os.chdir(folder_path)

    # Контент для записи в файл, если программа не выявит расшифровок.
    content = ['пусто']

    cipher = CaesarsCipher()
    d = enchant.Dict('en_US')
    text_enc = input('Что нужно расшифровать: ')

    # Список вариантов расшифрованного текста с пробелами,
    # которые прошли отбор по условиям ниже.
    list_passwords_with_space = []

    # И список всех паролей, если ни одного подходящего не найдено.
    list_all_passwords = []

    for cipher.key in range(66):
        text_dec = cipher.decrypt(text_enc)

        # Длину пароля не рассматриваю. Допускается что весь текст
        # может быть паролем.
        #
        # Исходим из того что пробел в пароле маловероятен!
        # Значит в зашифрованном тексте, если пробел есть
        # то может быть только для разделения слов и пароля.
        #
        # 1 - Проверяем есть ли пробел в расшифрованном тексте. Если
        # есть, то нас интересует:

        # A -  комбинация из существующих в природе слов и
        # несуществующих - здесь вероятно скрыт пароль.
        # B - Только набор существующих слов, пароль где-то в этих
        # словах.
        # C - Набор из нескольких только несуществующих слов написанных
        # через пробел исключаем.

        if ' ' in text_dec:

            # Разделим слова по пробелу и отсортируем на существующие и
            # не существующие.
            list_text_dec = text_dec.split()
            list_wrong_word = []
            list_correct_word = []

            for i in range(len(list_text_dec)):
                if d.check(str(list_text_dec[i])):
                    # При проверке слова из одной буквы, определяет
                    # это слово как существующее, в том числе с точками,
                    # поэтому...
                    if (len(list_text_dec[i]) > 1
                            and '.' not in list_text_dec[i]):
                        list_correct_word.append(list_text_dec[i])
                    # Артикль 'a' оставим.
                    elif list_text_dec[i] == 'a':
                        list_correct_word.append(list_text_dec[i])
                    # Отфильтрованные единичные буквы с точкой,
                    # проходящие проверку орфографии добавим в список
                    # не существующих слов.
                    elif '.' in list_text_dec[i]:
                        list_wrong_word.append(list_text_dec[i])

                else:
                    list_wrong_word.append(list_text_dec[i])

            if len(list_correct_word) > 0 and len(list_wrong_word) > 0:
                # Пусть не существующих слов может быть больше чем одно,
                # ведь в комментариях к паролю может быть допущена
                # грамматическая ошибка.
                # Выведем и такие в качестве варианта.
                list_passwords_with_space.append(f'Ключ: {cipher.key},'
                                                 f'Расшифровка: {text_dec}.'
                                                 f' Возможные пароли:'
                                                 f'{', '
                                                 .join(list_wrong_word)}')

                print(f'Ключ: {cipher.key}, расшифровка: {text_dec}. '
                      f'Возможно ваш пароль {list_wrong_word}')

            elif len(list_correct_word) > 0 and len(list_wrong_word) == 0:
                list_passwords_with_space.append(text_dec)
                print(f'Ключ: {cipher.key}, расшифровка: {text_dec}.')

            content = list_passwords_with_space

    # Если отсутствуют допустимые расшифровки с пробелами, не будет
    # выведено никаких сообщений, поэтому создадим на этот случай еще
    # один проход и выведем все варианты
    if len(list_passwords_with_space) == 0:
        for cipher.key in range(66):
            text_dec = cipher.decrypt(text_enc)
            list_all_passwords.append(text_dec)
            content = list_all_passwords

            # Вывод в консоль всех паролей.
            print(f'Ключ: {cipher.key}, расшифровка: {text_dec}.')

    with open('password.txt', 'w', encoding='utf-8') as file:
        file.writelines(content)



