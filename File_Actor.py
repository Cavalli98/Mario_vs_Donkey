'''
-----------------------------------------.
*** CAVALLI DARIO, CORACHEA NATHAN ******|
***                                      |
*** -Actor                               |
***   Classi presenti: Actor, Arena;     |
***                                      |
***   Classi di base del gioco.          |
***                                      |
-----------------------------------------
'''


class Actor():

    def move(self):
        raise NotImplementedError('Abstract method')

    def collide(self, other: 'Actor'):
        raise NotImplementedError('Abstract method')

    def rect(self) -> (int, int, int, int):
        raise NotImplementedError('Abstract method')

    def symbol(self) -> (int, int):
        raise NotImplementedError('Abstract method')



class Arena():

    def __init__(self, width: int, height: int):
        self._w, self._h = width, height
        self._actors = []

    def add(self, a: Actor):
        if a not in self._actors:
            self._actors.append(a)

    def remove(self, a: Actor):
        if a in self._actors:
            self._actors.remove(a)

    def move_all(self):
        actors = list(reversed(self._actors))
        for a in actors:
            previous_pos = a.rect()
            a.move()
            if a.rect() != previous_pos:  
                for other in actors:
                    if other is not a and self.check_collision(a, other):
                            a.collide(other)
                            other.collide(a)

    def check_collision(self, a1: Actor, a2: Actor) -> bool:
        x1, y1, w1, h1 = a1.rect()
        x2, y2, w2, h2 = a2.rect()
        return (y2 < y1 + h1 and y1 < y2 + h2
            and x2 < x1 + w1 and x1 < x2 + w2
            and a1 in self._actors and a2 in self._actors)

    def actors(self) -> list:
        return list(self._actors)

    def size(self) -> (int, int):
        return (self._w, self._h)
