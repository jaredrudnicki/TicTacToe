import pygame, sys

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)



# A Tile represents a single piece on a TicTacToe Board.
# A Tile has a size and a location on the board.
# A Tile can either be empty (' ') or filled with an X('x') or and O('o').
class Tile:
    def __init__(self, screen, pos):
        self.screen = screen
        self.height = 30
        self.width = 30
        #play is a space x or an o
        self.player = ' '
        self.pos = pos

    def make_x(self):
        self.player = 'x'

    def make_o(self):
        self.player = 'o'

    def draw(self):
        text_surface = myfont.render(self.player, False, red)
        self.screen.blit(text_surface, self.pos)

# A Game draws the board and  maintains the rules of TicTacToe.
# It switches the players turn and makes sure users cannot click a Tile already been played.
# A Game also detects whether win/loss/tie.
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((300,300))
        self.turn = 0
        self.tiles = [Tile(self.screen, (50,50)), Tile(self.screen, (150,50)), Tile(self.screen, (250,50)),
            Tile(self.screen, (50,150)), Tile(self.screen, (150,150)), Tile(self.screen, (250,150)),
             Tile(self.screen, (50,250)), Tile(self.screen, (150,250)), Tile(self.screen, (250,250))]

    def draw(self):
        pygame.draw.line(self.screen, red, (100,0), (100,300))
        pygame.draw.line(self.screen, red, (200,0), (200,300))
        pygame.draw.line(self.screen, red, (0,100), (300,100))
        pygame.draw.line(self.screen, red, (0,200), (300,200))
        for tile in self.tiles:
            tile.draw()

    def is_open(self, tile_number):
        return self.tiles[tile_number].player == ' '

    def move(self, pos):
        x = pos[0]
        y = pos[1]
        tile = 0
        if x < 100:
            if y < 100:
                tile = 0
            elif y < 200:
                tile = 3
            else:
                tile = 6
        elif x < 200:
            if y < 100:
                tile = 1
            elif y < 200:
                tile = 4
            else:
                tile = 7
        else:
            if y < 100:
                tile = 2
            elif y < 200:
                tile = 5
            else:
                tile = 8
                
        if self.is_open(tile):
            if self.turn % 2 == 0:
                self.tiles[tile].make_x()
            else:
                self.tiles[tile].make_o()
            self.turn = self.turn + 1

    def get_winner(self):
        winner = ' '
        options = [[self.tiles[0], self.tiles[1], self.tiles[2]],
                   [self.tiles[3], self.tiles[4], self.tiles[5]],
                   [self.tiles[6], self.tiles[7], self.tiles[8]],
                   [self.tiles[0], self.tiles[3], self.tiles[6]],
                   [self.tiles[1], self.tiles[4], self.tiles[7]],
                   [self.tiles[2], self.tiles[5], self.tiles[8]],
                   [self.tiles[0], self.tiles[4], self.tiles[8]],
                   [self.tiles[2], self.tiles[4], self.tiles[6]]]
        
        for option in options:
            if option[0].player == option[1].player and option[1].player == option[2].player:
                if option[1].player == 'x':
                    winner = 'x'
                elif option[1].player == 'o':
                    winner = 'o'
                    
        return winner
    
    def is_game_over(self):
        
        if self.get_winner() == ' ':
            filled = True
            for tile in self.tiles:
                if tile.player == ' ':
                    filled = False
            return filled
        else:
            return True
        
                    

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #change the tile at that location
                    pos = pygame.mouse.get_pos()
                    self.move(pos)
                    if self.is_game_over():
                        g = GameOver(self.get_winner())
                        running = False
                        g.run()
            self.screen.fill(black)
            self.draw()
            pygame.display.update()

# Home represents the home screen of the game. Introduces the game. 
# Directs the user to press Space to continue.
class Home:
    def __init__(self):
        self.screen = pygame.display.set_mode((500,500))

    def draw(self):
        text_surface_1 = myfont.render('WELCOME TO TICTACTOE', False, red)
        text_surface_2 = myfont.render('game created by Jared', False, red)
        text_surface_3 = myfont.render('press space to play', False, red)
        self.screen.blit(text_surface_1, (20,100))
        self.screen.blit(text_surface_2, (20,130))
        self.screen.blit(text_surface_3, (20,250))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False
                        g = Game()
                        g.run()
            self.screen.fill(black)
            self.draw()
            pygame.display.update()

# GameOver represents the end screen. Displays the result of the previous game.
# Allows user to restart a new game by pressing space.
class GameOver:
    def __init__(self, gamestate):
        self.screen = pygame.display.set_mode((500,500))
        self.gamestate = gamestate

    def draw(self):
        if self.gamestate == ' ':
            text_surface = myfont.render('tie!', False, red)
        else:
            text_surface = myfont.render('player ' + self.gamestate + ' wins!', False, red)
        
        text_surface_2 = myfont.render('press space to restart', False, red)

        self.screen.blit(text_surface, (20, 100))
        self.screen.blit(text_surface_2, (20, 250))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False
                        g = Game()
                        g.run()
            self.screen.fill(black)
            self.draw()
            pygame.display.update()
        
#Initialize the home screen upon running the script.
h = Home()
h.run()
