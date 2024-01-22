'''
--------------------------------------------------------.
*** CAVALLI DARIO, CORACHEA NATHAN *********************|
***                                                     |
*** -Mario vs Donkey - Main                             |
***                                                     |
***   Game;                                             | 
***   Muoversi con le Frecce o con le letter AWSD;      |
***   Saltare con lo Spazio;                            |
***   Usare il martello premendo M;                     |
***   Si muore se ci si scontra con un nemico;          |
***   Si vince se si raggiune la Principessa Peach;     |
***   F5 per iniziare una nuova partita.                |
***                                                     |
--------------------------------------------------------
'''


import game2d
import random
import time
from File_Actor import Arena, Actor
from File_Map_Still import platforms, ladders, m_elements, l_elements
from File_Actor_Still import Platform, Ladder, Firedtank, Still_Barrell
from File_Actor_Animated import Barrell, FiredBarrell, BlueFire, Princess, Donkey
from File_Actor_Jumper import Jumper, Mario

def update():
    global begin, good_end, bad_end, play
    global finish_bad,finish_good
    mario_finish, finish_good, finish_bad = mario.finished()
    if not play:
        game2d.image_blit(starter_image, (0,0))
    else:
        if not mario_finish:
            t = time.clock() - begin
            if t > 5.3:
                donkey.right(False)
                cbarrell()
                begin = time.clock()
            elif t > 5:
                 donkey.load(False)
                 donkey.right(True)
            elif t > 4:
                donkey.left(False)
                donkey.load(True)
            elif t > 3.5:
                donkey.left(True)
            
        if not mario_finish:
            arena.move_all()
        else:
            mario.move()
            princess.move()
            donkey.move()
        game2d.image_blit(image,(0,0))
        for a in arena.actors():
            xr, yr, wr, hr = a.rect()
            xs, ys= a.symbol()
            game2d.image_blit(sprites,(xr,yr),area=(xs,ys,wr,hr))
            if xs == -1 and ys == -1:
                if finish_bad:
                    bad_end = True
                elif finish_good:
                    good_end = True

        #At the end of the game
        if bad_end:
            game2d.image_blit(image,(0,0))
            game2d.image_blit(game_over, (30, 16))
            game2d.image_blit(game_over2, (30, 118))
            game2d.image_blit(donkey_won, (43, 140))
            
        if good_end:
            game2d.image_blit(image,(0,0))
            game2d.image_blit(you_won, (11, -10))
            game2d.image_blit(mario_won, (80, 105))
        
        
def keydown(code):  #Keyboard instructions
    global play
    if code == "Space":
        mario.jump()
    elif code == "ArrowRight" or code == "KeyD":
        mario.go_right()    
    elif code == "ArrowLeft" or code == "KeyA":
        mario.go_left()
    elif code == "ArrowUp" or code == "KeyW":
        mario.go_up()
    elif code == "ArrowDown" or code == "KeyS":
        mario.go_down()
    elif code == "KeyM":
        mario.thor(True)
    elif code == "Enter":
        if not play:
            play = True
            game2d.audio_play(hurryup)

def keyup(code):
    if code != "Space" and code != "KeyM":
        mario.stay()
        game2d.audio_pause(walk)
    mario.onRelease(code)

def audioend(boolean,boolean2):
    if boolean:
        game2d.audio_play(win)
    elif  boolean2:
        game2d.audio_play(die)

def audiothor ():
    game2d.audio_play(thor)
    game2d.audio_play(usehammer)

def audiojump():
    game2d.audio_play(jump)

def audiowalk():
    game2d.audio_play(walk,True)
    

def drawhearts():
     game2d.image_blit(sprites,(105,23),area=(206,268,15,12))

def cbarrell():  #function to create a new barrell, used in Class Barrell
    Barrell(arena,50,70)

def cfiredbarrell():  #create firedbarrell, used in Class Barrell
    import random
    a=random.choice([1,2])
    if a==1 or a==2:
        FiredBarrell(arena,26,220)
        game2d.audio_play(fire)

def cbluefire(x, y):  #create bluefire, used in Class Barrell
    BlueFire(arena, x, y)
    game2d.audio_play(bluefire)
    
    

arena=Arena(224,256)   #creation of Arena, Platforms and ladders
for c in platforms:
    c=Platform(arena,c[1],c[2],c[3],c[4])
    m_elements.append(c)
for d in ladders:
    d=Ladder(arena,d[1],d[2],d[3],d[4])
    l_elements.append(d)

starter_image = game2d.image_load("dk_pagina_iniziale.png")
image = game2d.image_load("dk_background.png")
sprites = game2d.image_load("dk_sprites(modified).png")
game_over = game2d.image_load("dk_game_over.png")
game_over2 = game2d.image_load("dk_game_over2.png")
you_won = game2d.image_load("dk_you_won.png")
mario_won = game2d.image_load("dk_mario_won.png")
donkey_won = game2d.image_load("dk_donkey_won.png")
walk, jump,goup= game2d.audio_load("audio_walking.wav") , game2d.audio_load("audio_jump.wav"), game2d.audio_load("audio_goup.wav")
die, win = game2d.audio_load("audio_die.wav") , game2d.audio_load("audio_win.wav")
bluefire = game2d.audio_load("audio_bluefire.wav")
hurryup = game2d.audio_load("audio_hurryup.wav")
thor,usehammer = game2d.audio_load("audio_thor.wav"),game2d.audio_load("audio_usehammer.wav")
fire = game2d.audio_load("audio_fire.wav")
game2d.canvas_init(arena.size())
mario = Mario(arena,30,235)
firedtank = Firedtank(arena,10,225)
donkey = Donkey(arena,10,52)
princess = Princess(arena,90,32)
barile1 = Still_Barrell(arena, 0, 54, 10, 16)
barile2 = Still_Barrell(arena, 0, 70, 10, 16)
play = False
finish_bad, finish_good = False, False
good_end = False
bad_end = False
begin = time.clock()

def main():
    donkey.roar(True)
    game2d.set_interval(update, 1000//30)
    game2d.handle_keyboard(keydown, keyup)
    
main()





