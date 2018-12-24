from random import choice
from string import ascii_letters


class StringHelper(object):
    @staticmethod
    def get_random_ascii_string(length):
        return ''.join(choice(ascii_letters) for i in range(length))