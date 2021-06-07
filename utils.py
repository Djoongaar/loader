import re

import numpy
import pymorphy2
from nltk import word_tokenize
from nltk.corpus import stopwords
from sklearn.base import TransformerMixin

morph = pymorphy2.MorphAnalyzer()
stopWords = stopwords.words("russian")


def tokenize_lemmatize(name):
    """
    Превращает строку лемматиированных токенов из строки текста
    :param name: строка на русском
    :return: строку из лемм токенов
    """
    pattern = re.compile(r'[^а-яё ]')
    words = word_tokenize(re.sub(pattern, '', name.lower().strip()))
    tokens = [morph.parse(word)[0].normal_form for word in words if (word not in stopWords and len(word) > 3)]
    # tokens = [morph.parse(word)[0].normal_form for word in words]
    return ' '.join(tokens)


class ArrayTransformer(TransformerMixin):

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X, y=None, **fit_params):
        return X.toarray()


def num_to_type(num):
    """ Преобразует числовой признак в категориальный в графе type"""
    if isinstance(num, numpy.int64):
        if num == 1:
            return 'Искусственное сооружение'
        if num == 2:
            return 'Дорога'
        if num == 3:
            return 'Прочее'
        return None
    elif isinstance(num, numpy.ndarray):
        return num[0]
    else:
        return num


def num_to_cat(num):
    """ Преобразует числовой признак в категориальный в графе category"""
    if isinstance(num, numpy.int64):
        if num == 1:
            return 'Строительство'
        if num == 2:
            return 'Капитальный ремонт'
        if num == 3:
            return 'Проектирование'
        if num == 4:
            return 'Содержание'
        if num == 5:
            return 'Закупка'
        if num == 6:
            return 'Оснащение / улучшение / ППР сооружений'
        if num == 7:
            return 'Строительный контроль'
        return None
    elif isinstance(num, numpy.ndarray):
        return num[0]
    else:
        return num
