from ntrprtr.action.ActionBase import ActionBase

class BitEqualsAction(ActionBase):
    def __init__(self):
        super().__init__()

    def process(self, action, _bytes):
        bits = ""
        result = action["noMatch"]
        
        endianess = action["endianess"]
        if(endianess == "big"):
            bits = self._cnvrtr.hexToBin(_bytes.hex())
        elif(endianess == "little"):
            bits = self.__hexToLittleEndianToBin(_bytes)
        
        # Always fill up zeros to represent all given bytes, even if 
        # they are zero
        bits = bits.rjust(len(_bytes)*8, "0")

        for i in range(0, len(action["cmp"])):
            if(bits == action["cmp"][i]["value"]):
                result = " ".join(bits[i:i+4] for i in range(0, len(bits), 4)) + "\n--------------\n" + action["cmp"][i]["description"]

        return result

    def __hexToLittleEndianToBin(self, byteArr):
        le = self._cnvrtr.toLittleEndian(byteArr.hex(" "))
        return str(self._cnvrtr.hexToBin(le))