from ntrprtr.action.ActionBase import ActionBase

class EqualsAction(ActionBase):
    def __init__(self):
        super().__init__()

    def process(self, action, _bytes):
        b = ""
        result = action["noMatch"]

        endianess = action["endianess"]

        if(endianess == "big"):
            b = _bytes.hex()
        elif(endianess == "little"):
            b = self._cnvrtr.toLittleEndian(_bytes.hex(" "))


        for i in range(0, len(action["cmp"])):
            if(b == action["cmp"][i]["value"].lower()):
                result = action["cmp"][i]["description"]
        return result