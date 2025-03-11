import pygame
from settings import *
from board import Board
from pieces import Pieces
from player import Player
from utilities import *
from engine import Engine
from AI import AI
import math
import numpy as np
import time

class Game:
    def __init__(self, screen, playerNumber=2):
        self._screen = screen
        self._end = False
        self._winner = None
        self._board = Board(self._screen)
        self._pieces = Pieces(self._screen)
        self._engine = Engine()
        self._playerNum = playerNumber
        self._player = []
        for i in range(self._playerNum):
            self._player.append(Player(i, COLORS[i]))
        self._player[1].isAI = True
        self._player[0].isAI = True
        self._currentPlayer = self._player[0]
        self._clickedPiece = None
        self._selectedPiece = None
        
        self._ai = {}
        for i in range(self._playerNum):
            if self._player[i].isAI:
                self._ai.update({self._player[i]  : (AI(self._engine))})
    
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
    
    def draw(self):
        self.screen.fill(WHITE)
        self.board.drawBoard()
        self.pieces.drawPieces()
        self.drawPlayers()
        self.drawLegalMoves()
        font = pygame.font.SysFont(None, 28)
        if self._currentPlayer.isAI:
            text_surface = font.render("AI ", True, self._currentPlayer.color)
        else :
            text_surface = font.render("Player 1 ", True, self._currentPlayer.color)
        text_rect = text_surface.get_rect(topleft = (WIDTH - 385, 140))
        self._screen.blit(text_surface, text_rect)
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
                
    def movePiece(self):
        # fprint(f"move to {boardToEngine(self.clickedPiece)}")
        # print(f"move to {self.clickedPiece}")
        self._currentPlayer.removePiece(self._selectedPiece[1])
        self._currentPlayer.addPiece(self.clickedPiece)
        self.clickedPiece = None
        self._selectedPiece = None
        self.humanMove()
    
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
                return
            if self._selectedPiece:
                for i, moves in self._currentPlayer.legalMoves:
                    if self._selectedPiece[1] == i and self.clickedPiece in moves:
                        self.movePiece()
                        return
    
    def humanMove(self):
        mtx = np.zeros((9, 9), dtype=np.bool)
        for pos in self._currentPlayer.boardPos:
            row, col = boardToEngine(pos)
            mtx[row, col] = True
        self._engine.update_state(mtx)
        if self._engine.is_goal():
            self._end = True
            self._winner = self._currentPlayer
            print(f"It's goal: {self._engine.game_state}")
            return
        
        # print(f"current state: {self._engine.game_state}")

        if self._engine.game_state[2] == True:
            self._currentPlayer = self._player[1]
        else:
            self._currentPlayer = self._player[0]
        self.setLegalMoves()
            
        return
        
    def drawCoordinates(self, text, position):
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=position)
        self._screen.blit(text_surface, text_rect)
    
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
            
    def AIMove(self):
        time.sleep(SLEEP_DURATION)
        # print("AI Moved")
        self._ai[self._currentPlayer].randomMove()
        if self._engine.is_goal():
            self._end = True
            self._winner = self._currentPlayer
            # print(f"It's goal: {self._engine.game_state}")
            return
        
        # print(f"current state: {self._engine.game_state}")
        if self._engine.game_state[2] == True:
            self._currentPlayer = self._player[1]
        else:
            self._currentPlayer = self._player[0]
        self.setCurrentState()
        self.setLegalMoves()
    