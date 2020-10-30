class Error(Exception):
    pass

class ShortageError(Error):
    def __init__(self, msg):
        self.msg = msg
