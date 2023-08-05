from cnvrtr.Converter import Converter
from ntrprtr.action.ActionType import ActionType



class Printer():
    def __init__(self) -> None:
        self._cnvrtr = Converter(nonAsciiPlaceholder=".")

    def print(self, result):
        for r in result:
            print("")
            print("--> " + r[1])
            print("    --------------")
            if(r[2] == ActionType.HEXDUMP):
                print("    Hexdump")
                print("    --------------")
                print("")
                dump = r[4].split("\n")
                for l in dump:
                    print("    " + l)
            elif(r[2] == ActionType.BITEQUALS):
                print("    " + r[3].hex(" ").upper())
                print("    --------------")
                dump = r[4].split("\n")
                for l in dump:
                    print("    " + l)
            else: 
                print("    " + r[3].hex(" ").upper())
                print("    --------------")
                print("    " + r[4])
           