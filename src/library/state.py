class State():
    SPIN_TEXT = ['?','S','D','T','Q']
    def __init__(self, 
                 filename='',
                 path='',
                 geom='',
                 state=0,
                 nstates=30,
                 spin=0):

        self.filename = filename
        self.path = path
        self.geomName = geom
        self.state = state
        self.nstates = nstates
        self.spin = spin
        self.data = {}

    @staticmethod
    def sub(item) -> str:
        #This might break things
        SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        return str(item).translate(SUB)
    
    def getText(self, style='') -> str:
        if self.geomName=='':
            text = self.filename
        else:
            text = self.geomName
        
        if style == 'a': #shortened, or simplified style
            return f"{State.SPIN_TEXT[self.spin]}{State.sub(self.state)}->{State.SPIN_TEXT[self.spin]}N/{State.sub(text)}"
        
        # elif style == 'd': # difference style
        #     return f"{State.SPIN_TEXT[self.spin]}{State.sub(self.state)}/{State.sub(text)}"
        
        else: # default style
            return f"{State.SPIN_TEXT[self.spin]}{State.sub(self.state)}/{State.sub(text)}"
        
