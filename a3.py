#Shahriar Arefin
import random
import os
import time

class TicTacToe:
    def __init__(self):
        self.current_player = 1
        self.gameBoard = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.AI = 1

    def getAI(self):
        return self.AI

    def setAI(self, turn):
        if turn == 1:
            return self.AI
        else:
            #AI goes second
            self.AI = 2
            return self.AI

    def copyGameState(self):
        copyGame = TicTacToe()
        copyGame.current_player = self.current_player
        copyGame.gameBoard = self.gameBoard[:]
        copyGame.AI = self.AI
        return copyGame

    def getgameBoard(self):
        return self.gameBoard

    def current_player(self):
        return self.current_player

    def switch_player(self):
        if (self.current_player == 1):
            self.current_player = 2
        else:
            self.current_player = 1
        return self.current_player

    def perform_move(self, player, index):
        self.gameBoard[index] = player

    def Is_game_still_running(self):
        if self.check_state() == -1:
            return True
        else:
            return False

    def check_state(self):
        #state = 0 for draw  #state = 1 if player 1 wins  #state = 2 if player 2 wins 
        #state = -1 game still going on
        state = -1
        win, player = self.if_Winning_State()
        if win == True:
            state = player
        elif win == False:
            if player == 0:
                state = player #draw
            else:
                state = -1
        else:
            state = -1

        return state


    def empty_space(self):
        empty_space = True
        if 0 not in self.gameBoard:
            empty_space = False
        return empty_space


    def if_Winning_State(self):
        #check row
        if (self.gameBoard[0] == self.gameBoard[1] == self.gameBoard[2]) and (self.gameBoard[0] != 0):
            return (True, self.gameBoard[0])

        elif (self.gameBoard[3] == self.gameBoard[4] == self.gameBoard[5]) and (self.gameBoard[3] != 0):
            return (True,  self.gameBoard[3])

        elif (self.gameBoard[6] == self.gameBoard[7] == self.gameBoard[8]) and (self.gameBoard[6] != 0):
            return True, self.gameBoard[6]
        #check column   
        elif (self.gameBoard[0] == self.gameBoard[3] == self.gameBoard[6]) and (self.gameBoard[0] != 0):
            return (True, self.gameBoard[0])

        elif (self.gameBoard[1] == self.gameBoard[4] == self.gameBoard[7]) and (self.gameBoard[1] != 0):
            return (True, self.gameBoard[1])

        elif (self.gameBoard[2] == self.gameBoard[5] == self.gameBoard[8]) and (self.gameBoard[2] != 0):
            return (True, self.gameBoard[2])
        #check diagonal
        elif (self.gameBoard[0] == self.gameBoard[4] == self.gameBoard[8]) and (self.gameBoard[0] != 0):
            return (True, self.gameBoard[0])

        elif (self.gameBoard[2] == self.gameBoard[4] == self.gameBoard[6]) and (self.gameBoard[2] != 0):
            return (True, self.gameBoard[2])

        elif self.empty_space() == False:
            return (False, 0)

        else:
            return (False, -1)

    def display_board(self):
        board = ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ']
        for i in range(9):
            if self.gameBoard[i] == 1:
                board[i] = ' X '
            if self.gameBoard[i] == 2:
               board[i] = ' O '

        print("------------")
        print('|' + board[0] + '|' + board[1] + '|' + board[2] + '|')
        print("------------")
        print('|' + board[3] + '|' + board[4] + '|' + board[5] + '|')
        print("------------")
        print('|' + board[6] + '|' + board[7] + '|' + board[8] + '|')
        print("------------")

    def Legal_Moves(self):
        legal_moves = []
        for i in range(9):
            if self.gameBoard[i] == 0:
                legal_moves.append(i)

        return legal_moves

    
class MonteCarloTreeSearch(object):

    def __init__(self, game, randomPLayOutNUM):
        self.game = game #game to be played Tic-Tac-Toe
        self.gameBoard = self.game.getgameBoard()
        self.state = self.game.Is_game_still_running() #get state of game if it's still running
        self.randomPLayOutNUM = randomPLayOutNUM

    def make_move(self):
        legal_moves = self.game.Legal_Moves() # get list of legal moves

        win_count = {}
        for move in legal_moves:
            win_count[move] = 0
        for move in legal_moves:
            for i in range(self.randomPLayOutNUM):
                win_count[move] = win_count[move] + self.random_PLay_Out(move)

        
        AI_move_choice = legal_moves[0]
        current_score = win_count[AI_move_choice]
        for move in win_count:
            if win_count[move] >= current_score:
                AI_move_choice = move
                current_score = win_count[move]

        self.game.perform_move(self.game.current_player, int(AI_move_choice))


    def random_PLay_Out(self, move):
        Current_game = self.game.copyGameState()
        Current_game.perform_move(Current_game.current_player, move)
        Current_game.switch_player()
        winning_state = False
        running = Current_game.Is_game_still_running()
        while running == True:
            legal_moves = Current_game.Legal_Moves() #get legal moves based on current game state
            if len(legal_moves) == 0:
                break
            random_move = random.choice(legal_moves) #choose a random move
            Current_game.perform_move(Current_game.current_player, int(random_move))
            Current_game.switch_player()
            running = Current_game.Is_game_still_running()


        state = Current_game.check_state()
        # loss = 0
        # win = 1
        # draw = .9
        loss = 0
        win = 2
        draw = 5
        if state == 0:
            return draw
        elif Current_game.getAI() == state:
            return win
        else:
            return loss



def player_input(legal_moves):
    print('\nHere is the number for the corresponding tile:\n')
    print('0 1 2 \n3 4 5 \n6 7 8\n')
    player_move = -1
    while True:

        try:
            player_move = input('Choose your next move... ')
            player_move = int(player_move)
        except ValueError:
            print("An exception occurred, choose an integer")
            continue
        
        if player_move in legal_moves:
            break
        else:
            print("Box Already filled, choose another one, BE SMART ! -_-")
    return player_move

def play_game():
    ticTacToe = TicTacToe()
    AI = MonteCarloTreeSearch(ticTacToe, 8000) 
    print("Do you want to go first('X') or go second('O')?")
    correct_input = False
    while correct_input == False:
        HUman_player = input("Type 1 for first, 2 for second:  ")
        
        try:
            HUman_player = int(HUman_player)
        except ValueError:
            print("An exception occurred, choose an integer")

        if HUman_player == 1  or HUman_player == 2:
            correct_input = True
        else:
            print("Wrong Input, You must enter 1 or 2.. BE SMART ! -_-")

    if HUman_player == 1:
        ticTacToe.setAI(turn = 2) #AI goes second
        ticTacToe.display_board()
        player_move = player_input(ticTacToe.Legal_Moves())
    else:
        ticTacToe.setAI(turn = 1) #AI goes first
        print("Computer's Turn....")
        AI.make_move()
        ticTacToe.switch_player()
        ticTacToe.display_board()
        player_move = player_input(ticTacToe.Legal_Moves())

    game_state = ticTacToe.Is_game_still_running()
    while game_state == True:
        ticTacToe.perform_move(ticTacToe.current_player, int(player_move))
        ticTacToe.display_board()
        ticTacToe.switch_player()
        print("Computer's Turn....")
        AI.make_move()
        game_state = ticTacToe.Is_game_still_running()
        if game_state == True:
            ticTacToe.switch_player()
            ticTacToe.display_board()
            player_move = player_input(ticTacToe.Legal_Moves())
            ticTacToe.perform_move(ticTacToe.current_player, int(player_move))
            game_state = ticTacToe.Is_game_still_running()

    ticTacToe.display_board()
    print("state =", ticTacToe.check_state())
    if ticTacToe.check_state() == 1:
        if HUman_player == 1:
            print ("CONGRAGULATIONS YOU WIN !!")
        else:
            print ("LOL YOU LOST, COMPUTER WON !!")

    elif ticTacToe.check_state() == 2:
        if HUman_player == 2:
            print ("CONGRAGULATIONS YOU WIN !!")
        else:
            print ("LOL YOU LOST, COMPUTER WON !!")
    else:
        print("It's a DRAW, good effort")



if __name__ == '__main__':
    print("TIC TAC TOE Game:")
    print("-----------------\n")
    play_game()