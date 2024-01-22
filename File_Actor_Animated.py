'''
------------------------------------------------------------------------------.
*** CAVALLI DARIO, CORACHEA NATHAN *******************************************|
***                                                                           |
*** -Actor_Animated                                                           |
***   Classi presenti: Barrell, FiredBarrell, BlueFire, Princess, Donkey;     |
***                                                                           |
***   Classi per il movimento degli oggetti non comandati dall'utente.        |
                                                                              |
------------------------------------------------------------------------------
'''


from File_Actor import Arena, Actor

class Barrell(Actor):
    def __init__(self,arena, x, y):
        self._x, self._y, self._dx, self._dy = x, y, 2, 2
        self._w, self._h = 12, 10
        self._speed, self._speed_ladder, self._g = 3, 1, 0.4
        arena.add(self)
        self._lx, self._ly, self._lw, self._lh = 0, 0, 0, 0
        self._px, self._py, self._pw, self._ph = 0, 0, 0, 0
        self._arena = arena
        self._landed=False
        self._pfire=False
        self._falling=False
        self._new_barrell = False
        self._blue = False
        self._time_barrell = time.clock() + 1
        self._remdx = 0
        

    def move(self):
        self._landed = False
        arena_w, arena_h = self._arena.size()
        self._y+=self._dy
        self._x+=self._dx

        if not self._landed:   # gravity and arena limits
            self._dy+=self._g
            self._dy = min(self._dy, 2*2)   
        if self._x>=arena_w-self._w:
            self._dx=-self._speed
        elif self._x<= 0 :
            self._dx=self._speed
            
        if (self._x + self._w//2 in (self._lx + self._lw//2, self._lx + self._lw//2 + 1)) and (self._ly < self._y + self._h < self._ly + self._lh):   # condizioni per scendere le scale
            n = random.randint(1, 4)
            if n == 1:
                self._falling = True
        if self._falling:   #movement to go down in stairs
            if self._dx != 0:
                self._remdx = self._dx
            self._dy = self._speed_ladder
            self._dx = 0
            if self._y + self._h > self._ly + self._lh // 2:
                if self._y < self._py:
                    self._falling = False
                    self._dx = - self._remdx
        '''if time.clock() > self._time_barrell + 2.5 and not self._new_barrell:
            donkey.left(True)
        if time.clock() > self._time_barrell + 3 and not self._new_barrell:
            donkey.load(True)
            donkey.left(False)
        if time.clock() > self._time_barrell + 4.5 and not self._new_barrell:
            donkey.right(True)
            donkey.load(False)
        if time.clock() > self._time_barrell + 5 and not self._new_barrell:   # creazione nuovo barrell
            cbarrell()
            self._new_barrell = True
            donkey.right(False)'''
            
            
        if self._pfire:   # creation of firedbarell
            arena.remove(self)
            cfiredbarrell()
        if self._blue:   # creation of blue firedbarrell
            arena.remove(self)
            cbluefire(self._x, self._y - 5)
            


    def collide(self, other):
        self._landed=False
        arena_w, arena_h = self._arena.size()
        xo,yo,wo,ho=other.rect()
        if isinstance(other,Platform):
            self._px, self._py, self._pw, self._ph = xo, yo, wo, ho
            if not self._falling:
                if self._y+self._h>=yo and self._y+self._h<=yo+ho and xo<=self._x+self._w//2<=xo+wo: 
                    self._y=yo-self._h
                    self._landed=True
        if isinstance(other, Firedtank): #if a barrell collides with FiredTank, possible fire.
            self._pfire = True
        if isinstance(other, Ladder):
            self._lx, self._ly, self._lw, self._lh = xo, yo, wo, ho
        if isinstance(other, FiredBarrell):
            self._blue = True
            arena.remove(other)
                

    def rect(self) ->(int, int, int, int):
        if self._falling:
            self._w, self._h = 15, 10
        else:
            self._w, self._h = 12, 10
        return self._x, self._y, self._w, self._h

    def symbol(self)-> (int,int):
        if self._falling:
            if self._y%2 == 0:
                return 96, 259
            else:
                return 96, 270
        else:
            if self._x%4==0:
                return 66, 258
            elif self._x%4==1:
                return 66, 270
            elif self._x%4==2:
                return 81, 258
            else:
                return 81, 270


        
class FiredBarrell(Actor):
    def __init__(self,arena, x, y):
        self._x, self._y, self._dx, self._dy = x, y, 2, 2
        self._w, self._h = 14, 16
        self._speed, self._speed_ladd_up, self._speed_ladd_down, self._g = 2, -1, 1, 0.4
        arena.add(self)
        self._lx, self._ly, self._lw, self._lh = 0, 0, 0, 0
        self._px, self._py, self._pw, self._ph = 0, 0, 0, 0
        self._arena = arena
        self._landed = False
        self._climbing = False
        self._falling = False
        self._burning_out = False
        self._burned_out = False
        self._start = time.clock() + 1

    def move(self):
        self._landed = False
        arena_w, arena_h = self._arena.size()
        self._y+=self._dy
        self._x+=self._dx
        
        if time.clock() > self._start + 10:   #fire life, after 10 seconds the flame will end.
            self._burning_out = True
            if self._dx > 0:
                self._speed = 1
                self._dx = min(self._dx, self._speed)
            else:
                self._speed = -1
                self._dx = max(self._dx, self._speed)
        if time.clock() > self._start + 15:
            self._burned_out = True
            if time.clock() > self._start + 15.2:
                arena.remove(self)

        if self._y < 66:   
            self._climbing = False
            self._falling = True

        if not self._landed:   #gravity and arena limits
            self._dy+=self._g
            self._dy = min(self._dy, 2*2)   
        if self._x>=arena_w-self._w:
            self._dx=-self._speed
        elif self._x<= 0 :
            self._dx=self._speed
            
        if (self._x + self._w//2 == self._lx + self._lw//2 + 1) and (self._ly < self._y < self._ly + self._lh) and not self._falling:   # condizioni per poter salire sulle scale
            n = random.randint(1, 2)
            if n == 1:
                self._climbing = True
        if (self._x + self._w//2 == self._lx + self._lw//2 + 1) and (self._ly < self._y + self._h < self._ly + self._lh) and not self._climbing: # condizione per poter scendere dalle scale
            n = random.randint(1, 3)
            if n == 1:
                self._falling = True
        if self._climbing:   #movement to go up
            self._dy = self._speed_ladd_up
            self._dx = 0
            if self._y + self._h < self._ly + self._lh // 2:
                if self._y + self._h < self._py:
                    self._climbing = False
                    self._dx = random.choice([self._speed, -self._speed])
        if self._falling:   # movimento to go down
            self._dy = self._speed_ladd_down
            self._dx = 0
            if self._y + self._h // 2> self._ly + self._lh // 2:
                if self._y < self._py:
                    self._falling = False
                    self._dx = random.choice([self._speed, -self._speed])

            
    def collide(self, other):
        self._landed=False
        arena_w, arena_h = self._arena.size()
        xo,yo,wo,ho=other.rect()
        if isinstance(other,Platform):
            self._px, self._py, self._pw, self._ph = xo, yo, wo, ho
            if not self._falling and not self._climbing:
                if self._y+self._h>=yo and self._y+self._h<=yo+ho and xo<=self._x+self._w//2<=xo+wo: 
                    self._y=yo-self._h
                    self._landed=True
        if isinstance(other, Firedtank):
            arena.remove(self)
        if isinstance(other, Ladder):
            self._lx, self._ly, self._lw, self._lh = xo, yo, wo, ho
        if isinstance(other, Barrell):
            aren.remove(other)
            

            
    def rect(self) ->(int, int, int, int):
        if self._burned_out:
            self._w, self._h = 16, 7
        return self._x, self._y, self._w, self._h

    def symbol(self)-> (int,int):
        if not self._burning_out:
            if self._x%32 in range(0, 15):
                return 133, 221
            else:
                return 159, 221
        elif self._burned_out:
            return 197, 228
        else:
            if self._x%32 in range(0, 15):
                return 113, 221
            else:
                return 180, 221


class BlueFire(FiredBarrell):
    
    def rect(self) ->(int, int, int, int):
        self._w, self._h = 16, 12
        return self._x, self._y, self._w, self._h

    def symbol(self)-> (int,int):
        if not self._burning_out:
            if self._x%32 in range(0, 15):
                return 114, 240
            else:
                return 176, 240
        elif self._burned_out:
            return 197, 226
        else:
            if self._x%32 in range(0, 15):
                return 133, 240
            else:
                return 158, 240


class Princess(Actor):
    def __init__(self,arena,x,y):
        self._x = x
        self._y = y
        self._w = 30
        self._h = 22
        self._end = 0
        self._finished = False
        arena.add(self)
        self._count = 0
        self._arena = arena

    def move(self):
        if self._finished:
            self._w = 15
            if time.clock() > self._end + 0.5:
                if self._count == 3:
                    self._count += 1
                    self._end = time.clock() + 1
                else:
                    self._count += 1
                    self._end = time.clock()

    def collide(self,other):
        xo,yo,wo,ho=other.rect()
        if isinstance(other,Mario):
            if self._x+self._w>=xo:
                self._finished = True

    def rect(self) ->(int, int, int, int):
        return self._x, self._y, self._w, self._h

    def symbol(self)->(int,int):
        if self._finished:
            #animation of saved princess
            if self._count == 1:
                return 158, 126
            elif self._count == 2:
                return 184, 126
            elif self._count == 3:
                return 158, 126
            elif self._count == 4:
                return 184, 126
            else:
                return 184, 126
        else:
            return 184, 126

    
class Donkey(Actor):
    def __init__(self,arena,x,y):
        self._x = x
        self._y = y
        self._w = 40
        self._h = 32
        self._count = 0
        self._end = 0
        self._dead_n = 1
        self._roar = False
        self._load = False
        self._right = False
        self._left = False
        self._dead = False
        arena.add(self)
        self._arena = arena

    def move(self):
        if self._roar or self._dead:
            if time.clock() > self._end + 0.5:
                self._count += 1
                self._end = time.clock()  

    def load(self, boolean):
        self._load = boolean
        self._roar = False

    def right(self, boolean):
        self._right = boolean
        
    def left(self, boolean):
        self._left = boolean
        
    def roar(self, boolean):
        self._roar = boolean
        self._left, self._right, self._load = False, False, False
        
    def dead(self, boolean):
        self._dead = boolean
        self._left, self._right, self._load = False, False, False

    def collide(self):
        pass

    def rect(self) ->(int, int, int, int):
        if self._roar:
            self._w, self._h = 46, 32
        elif self._dead:
            self._w, self._h = 47, 32
            if self._dead_n == 1:
                self._y += 3
                self._dead_n += 1
        elif self._load:
            self._w, self._h = 40, 32
        elif self._right or self._left:
            self._w, self._h = 43, 32
        return self._x, self._y, self._w, self._h

    def symbol(self)->(int,int):
        if self._roar:
            if self._count == 1:
                return 58, 152
            elif self._count == 2:
                return 202, 152
            elif self._count == 3:
                return 58, 152
            elif self._count == 4:
                return 202, 152
            else:
                self._count = 0
                self._end = 0
                self._roar = False
                return 202, 152
        elif self._dead:
            if self._count == 1:
                return 108, 187
            elif self._count == 2:
                return 5, 192
            elif self._count == 3:
                return 202, 190
            else:
                return 58, 190
        elif self._left:
            return 9, 152
        elif self._load:
            return 158, 152
        elif self._right:
            return 254, 152
        else:
            return 108, 152
