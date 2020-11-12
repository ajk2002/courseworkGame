import pygame as pg  # imports the pygame module, I change it to pg for ease of use
import sys
from settings import *  # imports everything from the settings file
from sprites import *
from os import path  # so that we know where files we want to retrieve are stored
import json



class Game:
    def __init__(self):  # this initialises all the attributes
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.question = -1
        self.font = pg.font.Font('freesansbold.ttf', 32)
        self.correct_answer = 0

        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)  # this is where the game folder is located
        self.map_data = []  # it will store all the map data
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:  # opens "map.txt" and allows us to read from it.
            for line in f:  # reads through each line in the text file
                self.map_data.append(line)  # and stores it in the map data variable.
        with open("data.json") as load_questions:#opens and then closes json file after usage.
            self.questions = json.load(load_questions)


    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):  # function to quit the game
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()




    def draw_grid(self):
        for x in range(0, WIDTH,
                       TILESIZE):  # draws a line, every 32 pixels along, until it reaches the end of the screen
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT,
                       TILESIZE):  # draws a line, every 32 pixels down, until it reaches the end of the screen
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw_UI(self):
        pg.draw.rect(self.screen, BLACK, (0, 0, WIDTH, TILESIZE * 3))
        pg.draw.rect(self.screen, BLACK, (0, HEIGHT - TILESIZE * 3, WIDTH, TILESIZE * 3))
        pg.draw.rect(self.screen, BLUE, (0, HEIGHT - TILESIZE * 3, 200, 200))
        pg.draw.rect(self.screen, RED, (440, HEIGHT - TILESIZE * 3, 200, 200))
        pg.draw.rect(self.screen, LIGHTGREY, (824, HEIGHT - TILESIZE * 3, 200, 200))


    def draw_question(self):
        current_question = self.questions["questions"][self.questions["order"][self.question]]["question"]
        answers = self.questions["questions"][self.questions["order"][self.question]]["answer"]
        questions_text = self.font.render(current_question, True, WHITE)
        self.screen.blit(questions_text, (WIDTH // 2, 0))

        answers = answers[3 - self.correct_answer:3] + answers[0:3 - self.correct_answer] # randomizes the answer selection, self.correct_answer = correct index
        for answer in range(len(answers)):
            answers_text = self.font.render(answers[answer], True, WHITE)
            answers_rect = answers_text.get_rect()
            self.screen.blit(answers_text, (answer * WIDTH // len(answers) + 100, HEIGHT - TILESIZE * 2))

    def draw(self):  # everything within this function will be drawn on the screen
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_UI()

        pg.display.flip()  # flips the display each time a new frame comes around.

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()  # quits the game
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()


# create the game object
g = Game()  # creates the instance of the game classss

while True:
    g.new()
    g.run()
