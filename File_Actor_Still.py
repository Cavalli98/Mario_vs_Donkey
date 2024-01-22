'''
-----------------------------------------------------------------.
*** CAVALLI DARIO, CORACHEA NATHAN ******************************|
***                                                              |
*** -Actor_Still                                                 |
***   Classi presenti: Platform, Ladder, Ladder_Broken;          |
***                    FiredTank, Still_Barrell;                 |
***                                                              |
***   Classi per la creazione del campo da gioco.  Tutti immobili.               |
***                                                              |
-----------------------------------------------------------------
'''



from File_Actor import Arena, Actor

class Platform(Actor):

    def __init__(self, arena, x, y, w, h):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._arena = arena
        arena.add(self)

    def move(self):
        pass

    def collide(self, other):
        pass
        
    def rect(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        return 0,0


    
class Ladder(Actor):
    def __init__(self, arena, x, y, w, h):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._arena = arena
        arena.add(self)

    def move(self):
        pass

    def collide(self, other):
        pass
        
    def rect(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        return 0,0


class Ladder_Broken(Ladder):
    pass



class Firedtank(Actor):
    def __init__(self,arena,x,y):
        self._x = x
        self._y = y
        self._w = 15
        self._h = 22
        arena.add(self)
        self._arena = arena

    def move(self):
        pass

    def collide(self):
        pass

    def rect(self) ->(int, int, int, int):
        return self._x, self._y, self._w, self._h

    def symbol(self)->(int,int):
        import random
        a=random.choice([0, 1])
        if a==0:
            return 125,255
        else:
            return 144,255

class Still_Barrell(Actor):
    def __init__(self, arena, x, y, w, h):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._arena = arena
        arena.add(self)

    def move(self):
        pass

    def collide(self, other):
        pass
        
    def rect(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        return 113, 264
