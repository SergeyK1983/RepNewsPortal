class NewsException(Exception):
    pass


class NewsExceptionFilterCensor(NewsException):
    """
    Для фильтра censor
    """
    @staticmethod
    def type_check(var):
        if not isinstance(var, str):
            raise NewsExceptionFilterCensor("фильтр censor: ожидался тип 'str' ...")
