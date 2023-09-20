from django import template
from django.template.defaultfilters import stringfilter
from ..exceptions import *
import os.path
from pathlib import Path


register = template.Library()

path_censor = os.path.join(Path(__file__).resolve().parent.parent, 'file_storage')

with open(os.path.join(path_censor, 'censor.txt'), 'r', encoding='utf8') as f:
    LIST_WORD = f.read().split()


@register.filter(is_safe=True)  # is_safe=True - Безопасная строка
# @stringfilter - преобразовать объект в его строковое значение перед передачей в функцию, чтобы не улететь в ошибку.
# Хотел этот декоратор использовать, чтобы не было ошибки при неправильном применении фильтра,
# но в итоге сделал по заданию.
def censor(value):
    """
    Функция производит цензуру предоставляемого текста (строки) на предмет не цензурных слов. Сравнивает слова со
    списком LIST_WORD, и заменяет найденные, пример: редиска --> р******. Регистр букв не важен.
    На входе проверяет тип, если не соответствует, то возвращает переменную как есть, с сообщением в терминал.
    :param value: 'str'.
    :return: Возвращает строку ('str')
    """
    try:
        NewsExceptionFilterCensor.type_check(value)
    except NewsExceptionFilterCensor as e:
        print(f'{e}')  # Надеюсь, что так корректно.
        return value
    else:
        _list = value.split()
        list_censor = _list.copy()
        for i in LIST_WORD:
            for a, j in enumerate(list_censor):
                j = j.lower()
                if j.find(i) != -1:
                    f = _list[a][:1] + '*' * (len(j) - 1)  # Замена найденного слова на первую букву и ***
                    _list.pop(a)
                    _list.insert(a, f)
        else:
            value = ' '.join(_list)
            list_censor.clear()

        return value
