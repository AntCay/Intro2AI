class Player:
    def __init__(self, no, color, isai, ai=None):
        self._color = color
        self._no = no
        self._enginePos = []
        self._boardPos = []
        self._legalMoves = []
        self._isAI = isai
        self._ai = ai
        if isai:
            self._name = ai.__class__.__name__
        else:
            self._name = "Player " + str(no)
    
    @property
    def color(self):
        return self._color
    
    @property 
    def ai(self):
        return self._ai
    
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

    @property
    def name(self):
        return self._name
    
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
        if value:
            self._name = self._ai.__class__.__name__
        else:
            self._name = "Player " + str(self._no)
        self._isAI = value
    
    @ai.setter
    def ai(self, value):
        self._ai  = value
    
    @name.setter
    def name(self, value):
        self._name = value

        
        
        
        