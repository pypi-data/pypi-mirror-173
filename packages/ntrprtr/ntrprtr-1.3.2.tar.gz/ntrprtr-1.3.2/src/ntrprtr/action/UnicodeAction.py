from ntrprtr.action.ActionBase import ActionBase

class UnicodeAction(ActionBase):
    def __init__(self):
        super().__init__()

    def process(self, action, _bytes):
        return _bytes.decode("utf-8")