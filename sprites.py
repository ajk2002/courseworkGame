import pygame as pg
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE #multiplied by tilesize so it can be spawned in the right location on the map.
        self.vx,self.vy = 0,0

    def get_keys(self): # this function will assign each key with a movement
        self.vx, self.vy = 0,0 # originally set to 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYERSPEED # moves to the left with a speed 300.
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYERSPEED # moves to the right with a speed 300.
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYERSPEED # moves to the up with a speed 300.
        if keys[pg.K_DOWN] or keys[pg.K_a]:
            self.vy = PLAYERSPEED # moves to the down with a speed 300.
        if self.vx != 0 and self.vy != 0:
            self.vx /= 1.414
            self.vy /= 1.414

    def collide_with_walls(self, dir):
        if dir == "x":
            hits = pg.sprite.spritecollide(self,self.game.walls, False) # checks if player collides with wall in x axis.
            if hits:
                if self.vx > 0: # means you are moving to the right
                    self.x = hits[0].rect.left - self.rect.width # places you right next to the left handside of the wall.
                if self.vx < 0: #means you are moving to the left
                    self.x = hits[0].rect.right# places you right next to the right handside of the wall.
                self.vx = 0 #set to zero as player shouldn't move if they collide.
                self.rect.x = self.x # keeps players position where its curently located
        if dir == "y":
            hits = pg.sprite.spritecollide(self,self.game.walls, False) # checks if player collides with wall in x axis.
            if hits:
                if self.vy > 0: # means you are moving up
                    self.y = hits[0].rect.top - self.rect.height # places you right next to the bottom of the wall.
                if self.vy < 0: #means you are moving down
                    self.y = hits[0].rect.bottom# places you right next to the top of the wall.
                self.vy = 0 #set to zero as player shouldn't move if they collide.
                self.rect.y = self.y # keeps players position where its curently located

    def update(self): # makes sure that each time a new frame comes, the images and events keep getting updated.
        self.get_keys()  # call this function so that player movement is updated.
        self.x += self.vx * self.game.dt  # dt is used so you can move at a consistent speed.
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls("x")#checks for collisions on x-axis
        self.rect.y = self.y
        self.collide_with_walls("y")# checks for collisions on the y-axis



class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):# initialises all the attributes
        self.groups = game.all_sprites, game.walls # adds the wall sprite into a group with all the sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))# each wall object is going to be the size of 1 tile
        self.image.fill(GREEN)# green colour
        self.rect = self.image.get_rect() # gets the rectangular area of the surface
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE