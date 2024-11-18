import pytest
import enchant
from git_task import CaesarsCipher


@pytest.mark.parametrize('message, key, result',
                         [('The password to my mailbox is fBIvqX5yjw',
                           10, ['The password to my mailbox is fBIvqX5yjw']),
                          ('1he pasword to my mailbox is H34hdgG5',
                           45, ['1he pasword to my mailbox is H34hdgG5']),
                          ('The paSsword   qwer1423F',
                           65, ['The paSsword   qwer1423F']),
                          ('password 123456789',
                           18, ['password 123456789']),
                          ('password',
                           9, [])])
def test_key_search(message, key, result):
    cipher = CaesarsCipher()
    cipher.key = key
    d = enchant.Dict('en_US')
    text_enc = cipher.encrypt(message)

    list_passwords_with_space = []

    for cipher.key in range(66):
        text_dec = cipher.decrypt(text_enc)

        if ' ' in text_dec:

            list_text_dec = text_dec.split()
            list_wrong_word = []
            list_correct_word = []

            for i in range(len(list_text_dec)):

                if d.check(str(list_text_dec[i])):
                    if (len(list_text_dec[i]) > 1
                            and '.' not in list_text_dec[i]):
                        list_correct_word.append(list_text_dec[i])

                    elif list_text_dec[i] == 'a':
                        list_correct_word.append(list_text_dec[i])

                    elif '.' in list_text_dec[i]:
                        list_wrong_word.append(list_text_dec[i])

                else:
                    list_wrong_word.append(list_text_dec[i])

            if len(list_correct_word) > 0 and len(list_wrong_word) > 0:
                list_passwords_with_space.append(text_dec)

            elif len(list_correct_word) > 0 and len(list_wrong_word) == 0:
                list_passwords_with_space.append(text_dec)

    assert list_passwords_with_space == result
