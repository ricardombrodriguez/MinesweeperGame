class Cell:

    def __init__(self,type):
        self.bomb = True if type == "BOMB" else False
        self.flag = False
        self.clicked = False
        self.number = None
