'''
-------------------------------------------.
*** CAVALLI DARIO, CORACHEA NATHAN ********|
***                                        |
*** -Actor_Jumper                          |
***   Classi presenti: Jumper, Mario;      |
***                                        |
***   Classi base del mio personaggio.     |
***                                        |
-------------------------------------------
'''


from File_Actor import Arena, Actor

class Jumper(Actor):
    def __init__(self,arena, x, y):
        import random
        self._x = x
        self._y = y
        self._dx = 0
        self._dy = 0
        self._w = 15
        self._h = 15
        self._speed = 3
        self._jump = -3.6
        self._g=0.4
        self._previous_pos = 0
        self._end = 0
        self._count = 0
        self._hammer = 0
        self._hammer_n = 0
        self._hammer_end = 0
        self._lx, self._ly, self._lw, self._lh = 0, 0, 0, 0
        self._landed = False
        self._climbed = False
        self._going_up = False
        self._going_down = False
        self._finished = False
        self._finished_bad = False
        self._finished_good = False
        self._thor = False
        self._f = False

        # if climbing on stairs
        self._climbing = False
        self._ladder_colliding = False
        self._arena = arena
        arena.add(self)

    def move(self):
        arena_w, arena_h = self._arena.size()

        if self._climbing:
            if (self._lx <= self._x + self._w//2 <= self._lx + self._lw) and (self._ly + self._lh >= self._y + self._h >= self._ly ):
                # no gravity if onstair
                if self._going_up:
                    upper_dist =  (self._ly + self._lh) - (self._y)
                    if upper_dist < 9:
                        self._climbing = False
                    self._dy = -self._speed

                elif self._going_down:
                    bottom_dist =  self._ly + self._lh - (self._y + self._h)
                    if bottom_dist < 3:
                        self._climbing = False
                    self._dy = +self._speed
                self._landed = True
            else:
                self._landed = False
                self._climbing = False
                self._dy = 0

        # Falling if moving on ladder
        if self._climbing and self._dx != 0:
            self._climbing = False
            self._going_up = self._going_down = False
            self._dy = 0

        # Apply gravity if not on ladder
        if not self._climbing:
            self._dy = min(self._dy + self._g, self._speed)

        self._y += self._dy
        self._x += self._dx

        
        if self._thor:
            if time.clock() > self._hammer_end + 0.1:
                self._hammer_end = time.clock()
                self._hammer += 1
                audiothor()
                if self._hammer == 2:
                    self._hammer_end = time.clock() + 0.2
                if self._hammer == 3:
                    self._hammer_end =0
                    self._hammer = 0
                    self._thor = False

        # bounding x
        self._x = max(0, self._x)
        self._x = min(arena_w - self._w, self._x)
        self._ladder_colliding = False

        # When the program ends
        if self._finished:
            self._dx = 0
            self._dy = 0
            self._speed = 0
            if time.clock() > self._end + 0.5:
                if self._count == 3:
                    self._count += 1
                    self._end = time.clock() + 2
                else:
                    self._count += 1
                    self._end = time.clock()


    def go_left(self):
        self._dx = - self._speed
        audiowalk()
        self._previous_pos = -1

    def go_right(self):
        self._dx = self._speed
        audiowalk()
        self._previous_pos = +1

    def jump(self):
        if self._landed:
            audiojump()
            self._dy = self._jump
            self._landed=False
        self._going_up=False
        self._going_down = False

    def go_up(self):
        if self._ladder_colliding and (self._lx <= self._x + self._w//2 <= self._lx + self._lw) or self._climbing:
            self._dy = - self._speed
            self._going_up = True
            self._climbing = True

    def go_down(self):
        if self._ladder_colliding and (self._lx <= self._x + self._w//2 <= self._lx + self._lw) or self._climbing:
            self._dy = self._speed
            self._going_down = True
            self._climbing = True
              
    def stay(self):
        self._dx = 0
        self._dy = 0
        if self._climbed and not self._landed:
            self._going_up = True
        elif self._landed:
            self._going_up = False

    def thor(self, boolean):
        self._thor = boolean
                    
        

    def collide(self, other):
        #if collides with other actor
        xo,yo,wo,ho = other.rect()
        arena_w, arena_h = self._arena.size()
        if isinstance(other, Platform):
            if self._y+ self._h < yo+ho and not self._climbing:
                self._y = yo-self._h
                self._landed = True
        if isinstance(other, Ladder):
            self._lx, self._ly, self._lw, self._lh = other.rect()
            self._ladder_colliding = True
        if isinstance(other, Barrell):
            #Mario can win against a barrell using his hammer
            if self._thor:
                arena.remove(other)
                
            else:
                self._finished_bad = True
                self._finished = True
                donkey.roar(True)
                audioend(self._finished_good,self._finished_bad)
        if isinstance(other, Firedtank):
            #Mario will die burnt if collides with a FiredTank
            self._finished_bad = True
            self._finished = True
            self._thor = False
            donkey.roar(True)
            audioend(self._finished_good,self._finished_bad)
        if isinstance(other, FiredBarrell):
            if self._thor:
                arena.remove(other)
            else:
                self._finished_bad = True
                self._finished = True
                donkey.roar(True)
                audioend(self._finished_good,self._finished_bad)
        if isinstance(other, BlueFire):
            #BlueFire wins against Mario, his hammer is useless
            self._finished_bad = True
            self._finished = True
            self._thor = False
            donkey.roar(True)
            audioend(self._finished_good,self._finished_bad)
        if isinstance(other, Donkey):
            self._finished_bad = True
            self._finished = True
            self._thor = False
            donkey.roar(True)
            audioend(self._finished_good,self._finished_bad)
        if isinstance(other, Princess):
            #Mario wins
            self._finished_good = True
            self._finished = True
            self._thor = False
            donkey.dead(True)
            audioend(self._finished_good,self._finished_bad)
            

    def finished(self) ->bool:
        return self._finished, self._finished_good, self._finished_bad

    def rect(self) ->(int, int, int, int):
        #We modified  Mario's weight and height if he's in thor mode
        if self._thor:
            if self._hammer%2 == 0:
                self._w, self._h = 26, 16
                self._hammer_n = 0
            else:
                self._w, self._h = 15, 29
                if self._hammer_n == 0:
                    self._y -= 11
                    self._hammer_n += 1
        else:
            self._w, self._h = 15, 15

        if self._finished_good and not self._f:
            self._y -= 7
            self._f = True

        return self._x, self._y, self._w, self._h

    def symbol(self)-> (int,int):
        if self._finished:
            if self._finished_bad:
                #animation of death
                if self._count == 1:
                    return 217, 107
                elif self._count == 2:
                    return 158, 107
                elif self._count == 3:
                    
                    return 177, 107
                elif self._count == 4:
                    return 197, 107
                else:
                    return -1, -1
                
            elif self._finished_good:
                
                #animation of happy Mario
                if self._count == 1:
                    return 94, 3
                elif self._count == 2:
                    drawhearts()
                    return 136, 3
                elif self._count == 3:
                    return 94, 3
                elif self._count == 4:
                    drawhearts()
                    return 136, 3
                else:
                    return -1, -1
                
        else:
            a= self._landed
            a = not self._climbing
            if self._thor:
                #thor animation
                if self._dx > 0:
                    if self._hammer%2 == 0:
                        return 180, 87
                    else:
                        return 158, 74
                elif self._dx < 0:
                    if self._hammer%2 == 0:
                        return 100, 87
                    else:
                        return 133, 74
                else:
                    if self._previous_pos > self._dx:
                        if self._hammer%2 == 0:
                            return 180, 87
                        else:
                            return 158, 74
                    else:
                        if self._hammer%2 == 0:
                            return 100, 87
                        else:
                            return 133, 74
            else:
                if not a and self._dx == 0:
                    if self._y%16 in range(0,8):
                        return 126, 23
                    else:
                        return 167,23
                elif not a and self._dx >= 0:
                    return 197, 3
                if not a and self._dx < 0:
                    return 94, 3
                
                if a and self._dx > 0:
                    if self._x%16 in range(0,8):
                        return 49, 15
                    else:
                        return 176,4
                elif a and self._dx < 0:
                    if self._x%16 in range(0,8):
                        return 23, 17
                    else:
                        return 115,4
                elif a and self._dx == 0:
                    if self._previous_pos > self._dx:
                        return 158,3
                    else:
                        return 136, 3
                else:
                    return 158,3


        
class Mario(Jumper):
    def onRelease(self, key):
        if key == "KeyA":
            self._dx = 0
        elif key == "KeyD":
            self._dx = 0
        elif key == "KeyW":
            self._going_up = False
        elif key == "KeyS":
            self._going_down = False
