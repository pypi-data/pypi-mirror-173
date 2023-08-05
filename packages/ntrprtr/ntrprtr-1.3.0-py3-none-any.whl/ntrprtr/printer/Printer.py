from ntrprtr.action.ActionType import ActionType

class Printer():
    def __init__(self) -> None:
        pass

    def print(self, result):
        for r in result:
            print("")
            print("--> " + r[1])
            print("    --------------")
            if(r[2] != ActionType.HEXDUMP):
                print("    " + r[3].hex(" ").upper())
                print("    --------------")
                print("    " + r[4])
            else:
                print("    Hexdump")
                print("    --------------")
                print("")
                dump = r[4].split("\n")
                for l in dump:
                    print("    " + l)
           