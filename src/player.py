class Player:
    def __init__(self, no, color):
        self._color = color
        self._no = no
        self._enginePos = []
        self._boardPos = []
        self._legalMoves = []
        self._isAI = False
    
    @property
    def color(self):
        return self._color
    
    @property
    def enginePos(self):
        return self._enginePos
    
    @property
    def boardPos(self):
        return self._boardPos

    @property
    def legalMoves(self):
        return self._legalMoves
    
    @property
    def isAI(self):
        return self._isAI
    
    def removePiece(self, position):
        self._boardPos.remove(position)
    
    def addPiece(self, position):
        self._boardPos.append(position)

    @enginePos.setter
    def enginePos(self, value):
        self._enginePos = value

    @boardPos.setter
    def boardPos(self, value):
        self._boardPos = value
    
    @legalMoves.setter
    def legalMoves(self, value):
        self._legalMoves.append(value)
        
    @isAI.setter
    def isAI(self, value):
        self._isAI = value
        
        