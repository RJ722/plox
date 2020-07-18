class ParseException(Exception):
    pass


class RuntimeException(Exception):
    def __init__(self, token, *args, **kwargs):
        self.token = token
        super().__init__(*args, **kwargs)
