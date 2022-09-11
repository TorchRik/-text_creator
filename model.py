import os
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from collections import Counter
import pickle
import random


def parser(text):
    lines = text.split('\n')
    for line in lines:
        words = line.split()
        for word in words:
            if sum([str(i) in word for i in range(10)]):
                continue
            if word[-1] in (',', '.', ':', ';'):
                yield str.lower(word[:-1])
                yield word[-1]
            else:
                yield str.lower(word)


def get_files_paths(path):
    return [path + '/' + f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


class Model:
    def __init__(self, path_to_save, path_to_train_data=None, text=None, count_word_to_predict=2):
        self._path_to_save = path_to_save
        self._count_word_to_predict = count_word_to_predict
        self._path_to_train_data = path_to_train_data
        self._statistic = dict()
        self._words = set()

    def _fit_by_text(self, text, prefix_counter):
        words = np.array(list(parser(text)))
        self._words.update(words)
        for example in sliding_window_view(words, window_shape=self._count_word_to_predict + 1):
            prefix = tuple(example[:-1])
            word = example[-1]
            if prefix not in self._statistic:
                self._statistic[prefix] = Counter()
            self._statistic[prefix][word] += 1
            prefix_counter[prefix] += 1

    def fit(self, text=None):
        prefix_counter = Counter()
        if self._path_to_train_data is not None:
            for file_name in get_files_paths(self._path_to_train_data):
                with open(file_name, 'r') as file:
                    self._fit_by_text(file.read(), prefix_counter)

        if text is not None:
            self._fit_by_text(text, prefix_counter)

        for prefix in self._statistic:
            for word in self._statistic[prefix]:
                self._statistic[prefix][word] /= prefix_counter[prefix]

    def save_me(self):
        file = open(self._path_to_save, 'wb')
        pickle.dump(self, file)

    def _get_next_word(self, word_prefix):
        p = random.random()
        now = 0
        if word_prefix not in self._statistic:
            return ''
        for word in self._statistic[word_prefix]:
            now += self._statistic[word_prefix][word]
            if now >= p:
                return word

    def generate(self, length, prefix=""):
        text = list(parser(prefix))
        if len(text) < self._count_word_to_predict or \
                tuple(text[-self._count_word_to_predict:]) not in self._statistic:
            prefix = tuple(self._statistic.keys())[random.randint(0, 100)]
            text += prefix
        else:
            prefix = tuple(text[-self._count_word_to_predict:])

        for i in range(length - self._count_word_to_predict):
            next_word = self._get_next_word(prefix)
            prefix = prefix[1:] + (next_word,)
            text.append(next_word)
        return " ".join(text[:length])
