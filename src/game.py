import pygame
from settings import *
from board import *
from utilities import *
import AI
from AI import *
import inspect
import math
import numpy as np
import time

class Game:
    def __init__(self, screen, player, engine):
        self._screen = screen
        self._end = False
        self._winner = None
        self._moveCount = 0
        self._board = Board(self._screen)
        self._pieces = Pieces(self._screen)
        self._backButton = Button(self._screen, 'red', BUTTON_MENU_FONT, "Back", (150, 75), (50, 50))
        self._restartButton = Button(self._screen, 'red', BUTTON_MENU_FONT, "Restart", (150, 75), (220, 50))
        self._closeButton = Button(self._screen, 'red', BUTTON_MENU_FONT, "Close", (150, 75), (WIDTH - 200, 50))
        self._stopButton = Button(self._screen, 'red', BUTTON_MENU_FONT, "Stop", (150, 75), (WIDTH - 375, 50))
        self._mainMenuButton = []
        self._mainMenuButton.append(Button(self._screen, 'blue', BUTTON_MENU_FONT, "AI vs AI", (200, 100), ((WIDTH - 200)*0.4, (HEIGHT - 100)*0.4)))
        self._mainMenuButton.append(Button(self._screen, 'blue', BUTTON_MENU_FONT, "Player vs AI", (200, 100), ((WIDTH - 200)*0.5, (HEIGHT - 100)*0.4)))
        self._mainMenuButton.append(Button(self._screen, 'blue', BUTTON_MENU_FONT, "Player vs Player", (200, 100), ((WIDTH - 200)*0.6, (HEIGHT - 100)*0.4)))
        
        self._aiOptionButton = []
        self._aiList = []
        for i in range(len(inspect.getmembers(AI, inspect.isclass))):      
            self._aiOptionButton.append(Button(self._screen, 'blue', BUTTON_MENU_FONT, inspect.getmembers(AI, inspect.isclass)[i][0], (300, 100), ((WIDTH - 200)*0.4, (HEIGHT - 100)*(0.4+i*0.1))))
        
        self._loopNum = 0
        self._gameMode = 0
        self._engine = engine
        self._playerNum = len(player)
        self._player = player
        self._currentPlayer = self._player[0]
        self._clickedPiece = None
        self._selectedPiece = None
    
        self.setCurrentState()
        self.setLegalMoves()
        
    @property
    def screen(self):
        return self._screen
    
    @property
    def end(self):
        return self._end

    @property
    def board(self):
        return self._board

    @property
    def pieces(self):
        return self._pieces

    @property
    def player(self):
        return self._player

    @property
    def currentPlayer(self):
        return self._currentPlayer
        
    @currentPlayer.setter
    def currentPlayer(self, player):
        self._currentPlayer = player

    @property
    def clickedPiece(self):
        return self._clickedPiece

    @clickedPiece.setter
    def clickedPiece(self, position):
        if position == None:
            self._clickedPiece = None
        else:
            x, y = position
            for row in range(BOARD_HEIGHT):
                for col in range(BOARD_WIDTH):
                    circle_x, circle_y = getPixelCoordinates(row, col)
                    if math.sqrt((circle_x - x - CELL_SIZE/10)**2 + (circle_y - y)**2) < CIRCLE_RADIUS:
                        self._clickedPiece = row, col
                        break
    @property
    def selectedPiece(self):
        return self._selectedPiece
    
    @selectedPiece.setter
    def selectedPiece(self, value):
        self._selectedPiece = value
        
    def loop(self):
        if self._loopNum == 0:
            return self.mainMenuLoop()
        elif self._loopNum == 1:
            return self.gamePlayLoop()
        elif self._loopNum == 2:
            return self.AIMenuLoop()
        # return True
    
    def gamePlayLoop(self):
        self.screen.fill(WHITE)
        self.drawGamePlay()
        if not self._end:
            if self._currentPlayer.isAI:
                time.sleep(SLEEP_DURATION)
                self._currentPlayer.ai.move()
                self._moveCount += 1
                self.updateBoardState()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self._closeButton.rect.collidepoint(event.pos):
                            return False
                        elif self._stopButton.rect.collidepoint(event.pos):
                            self.restart()
                            self._end = True
            else:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self._backButton.rect.collidepoint(event.pos):
                            self.restart()
                            self._loopNum = 0
                        elif self._closeButton.rect.collidepoint(event.pos):
                            return False
                        elif self._restartButton.rect.collidepoint(event.pos):
                            self.restart()
                        elif self.handleClick(event.pos):
                            self.humanMove()
                            self._moveCount += 1
                            self.updateBoardState()
                    elif event.type == pygame.QUIT:
                        return False
        
        else:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self._backButton.rect.collidepoint(event.pos):
                        self.restart()
                        self._loopNum = 0
                    elif self._restartButton.rect.collidepoint(event.pos):
                        self.restart()
                    elif self._closeButton.rect.collidepoint(event.pos):
                        return False
                elif event.type == pygame.QUIT:
                    return False
        return True

    def mainMenuLoop(self):
        self.screen.fill(WHITE)
        titleText = pygame.font.Font(size=int(WIDTH*0.05)).render(
            "Two Player Chinese Checkers", True, 'green')
        titleTextRect = titleText.get_rect()
        titleTextRect.center = (WIDTH*0.5, HEIGHT*0.25)
        self.screen.blit(titleText, titleTextRect)
        
        for btn in self._mainMenuButton:
            btn.draw()
        self._closeButton.draw()
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self._mainMenuButton[0].rect.collidepoint(event.pos):
                    self._gameMode = 0
                    for i in range(self._playerNum):
                        self._player[i].isAI = True
                    self._loopNum = 1
                elif self._mainMenuButton[1].rect.collidepoint(event.pos):
                    self._gameMode = 1
                    self._player[0].isAI = False
                    self._player[1].isAI = True
                    self._loopNum = 1
                elif self._mainMenuButton[2].rect.collidepoint(event.pos):
                    self._gameMode = 2
                    for i in range(self._playerNum):
                        self._player[i].isAI = False
                    self._loopNum = 1
                elif self._closeButton.rect.collidepoint(event.pos):
                    return False
                    
            elif event.type == pygame.QUIT:
                return False

        return True
    
    def AIMenuLoop(self):
        self.screen.fill(WHITE)
        titleText = pygame.font.Font(size=int(WIDTH*0.08)).render(
            "Chinese Checkers", True, 'green')
        titleTextRect = titleText.get_rect()
        titleTextRect.center = (WIDTH*0.5, HEIGHT*0.25)
        self.screen.blit(titleText, titleTextRect)
        
        for btn in self._aiOptionButton:
            btn.draw()
        
        self._backButton.draw()
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self._backButton.rect.collidepoint(event.pos):
                    self._loopNum = 0
                else:
                    for i in self._aiOptionButton:
                        if i.rect.collidepoint(event.pos):
                            i.color = 'green'
                            self._loopNum = 1
                    
            elif event.type == pygame.QUIT:
                return False
            
        return True
        
    def drawGamePlay(self):
        self.board.drawBoard()
        self.pieces.drawPieces()
        self.drawPlayers()
        self.drawLegalMoves()
        text_surface = GAME_STATUS_FONT.render(self._player[0].name + " vs " + self._player[1].name, True, BLACK)
        text_rect = text_surface.get_rect(topleft = (WIDTH - 565, 200))
        self._screen.blit(text_surface, text_rect)
        text_surface = GAME_STATUS_FONT.render(self._currentPlayer.name, True, self._currentPlayer.color)
        text_rect = text_surface.get_rect(topleft = (WIDTH - 485, 230))
        self._screen.blit(text_surface, text_rect)
        text_surface = GAME_STATUS_FONT.render(str(self._moveCount), True, BLACK)
        text_rect = text_surface.get_rect(topleft = (WIDTH - 485, 260))
        self._screen.blit(text_surface, text_rect)
        self._backButton.draw()
        self._restartButton.draw()
        self._closeButton.draw()
        self._stopButton.draw()
        
        pygame.display.flip()
        
    def drawPlayers(self):
        for i in range(self._playerNum):
            for row, col in self._player[i].boardPos:
                x, y = getPixelCoordinates(row, col)
                pygame.draw.circle(self._screen, self._player[i].color, (int(x), int(y)), CIRCLE_RADIUS)
                pygame.draw.circle(self._screen, BLACK, (int(x), int(y)), CIRCLE_RADIUS, 2)
                row, col = boardToEngine((row,col))
                self.drawCoordinates(f"{row},{col}", (int(x), int(y)))
        return
    
    def drawLegalMoves(self):
        if self._selectedPiece:
            for i,j in self._currentPlayer.legalMoves:
                if self._selectedPiece[1] == i:
                    for row, col in j:
                        x, y = getPixelCoordinates(row, col)
                        pygame.draw.circle(self._screen, "green", (int(x), int(y)), CIRCLE_RADIUS, 2)
                    return
    
    def drawCoordinates(self, text, position):
        text_surface = CORDINATES_FONT.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=position)
        self._screen.blit(text_surface, text_rect)
    
    def handleClick(self, pos):
        self.clickedPiece = pos
        print(self.clickedPiece)
        if self.clickedPiece in self._board.board:
            if self.clickedPiece in self._currentPlayer.boardPos:
                self._selectedPiece = (self._currentPlayer.color, self.clickedPiece)
                print(f"Select piece: {(self._selectedPiece[0], boardToEngine(self._selectedPiece[1]))}")
                # print(f"Select piece:  {self._selectedPiece}")
                for i, moves in self._currentPlayer.legalMoves:
                    if self._selectedPiece[1] == i:
                        movesE = []
                        for move in moves:
                            movesE.append(boardToEngine(move))
                        # print(f"current legal moves: {movesE}")
                        # print(f"legal moves : {moves}")
                return 0
            if self._selectedPiece:
                for i, moves in self._currentPlayer.legalMoves:
                    if self._selectedPiece[1] == i and self.clickedPiece in moves:
                        self.movePiece()
                        return 1
    
    def movePiece(self):
        # fprint(f"move to {boardToEngine(self.clickedPiece)}")
        # print(f"move to {self.clickedPiece}")
        self._currentPlayer.removePiece(self._selectedPiece[1])
        self._currentPlayer.addPiece(self.clickedPiece)
        self.clickedPiece = None
        self._selectedPiece = None
    
    def humanMove(self):
        mtx = np.zeros((9, 9), dtype=np.bool)
        for pos in self._currentPlayer.boardPos:
            row, col = boardToEngine(pos)
            mtx[row, col] = True
        self._engine.update_state(mtx)
        return
    
    def updateBoardState(self):
        if self._engine.game_state[2] == True:
            self._currentPlayer = self._player[1]
        else:
            self._currentPlayer = self._player[0]
        self.setLegalMoves()
        self.setCurrentState()
        if self._engine.is_goal():
            self._end = True
            self._winner = self._currentPlayer
            print(f"It's goal: {self._engine.game_state}")

    def setCurrentState(self):
        self._player[0].enginePos.clear()
        self._player[1].enginePos.clear()
        self._player[0].boardPos.clear()
        self._player[1].boardPos.clear()
        
        self._player[0].enginePos = list(zip(*np.where(self._engine.p1_mask)))
        self._player[1].enginePos = list(zip(*np.where(self._engine.p2_mask)))
        
        for pos in self._player[0].enginePos:
            self._player[0].boardPos.append(engineToBoard(pos))
        for pos in self._player[1].enginePos:
            self._player[1].boardPos.append(engineToBoard(pos))
            
    def setLegalMoves(self):
        self._player[0].legalMoves.clear()
        self._player[1].legalMoves.clear()
        for i in range(len(self._player[0].enginePos)):
            x = list(zip(*np.where(self._engine.actions()[0][i])))
            lm = []
            for j in x:
                lm.append(engineToBoard(j))
            self._player[0].legalMoves = (engineToBoard(self._engine.actions()[1][i]), lm)
        
        initial_state_p2 = list(self._engine.game_state)
        initial_state_p2[2] = True
        initial_state_p2 = tuple(initial_state_p2)
        for i in range(len(self._player[1].enginePos)):
            x = list(zip(*np.where(self._engine.actions(initial_state_p2)[0][i])))
            lm = []
            for j in x:
                lm.append(engineToBoard(j))
            self._player[1].legalMoves = (engineToBoard(self._engine.actions(initial_state_p2)[1][i]), lm)
        return
    
    def restart(self):
        self._engine.p1_mask = self._engine.goal_map_p1.T
        self._engine.p2_mask = np.copy(self._engine.goal_map_p1)
        self._engine.is_p2_turn = False
        self._end = False
        self._moveCount = 0
        self._winner = None
        self.updateBoardState()
    