#######################################################
#													
# Author:      Cosima Manughian-Peter
# Date:        September 21, 2015
# Class:       CECS 424 MW
# Assignment:  Lab 2
# Purpose:     Determine all possible moves a player
#              can make given a certain chess board
# File name:   lab2.py
#
#######################################################


### Initialize the chess board ###

# Lower case = white player / player 1
# Upper case = black player / player 2
# P  = pawn
# R  = rook
# B  = bishop
# KN = knight
# Q  = queen
# KI = king

NUM_COLS = 8
NUM_ROWS = 8

chess_board = \
  [['R','KN','','Q','KI','','','R'],\
  ['','B','','P','','P','','P'],\
  ['','','P','B','','KN','',''],\
  ['P','','','','P','','',''],\
  ['','','','p','','','',''],\
  ['','p','kn','q','','kn','',''],\
  ['p','','p','','p','','p',''],\
  ['r','','b','','ki','b','','r']]


# Yields each piece on the board that 
# belongs to the current player in 
# row-major order   
def player_pieces( board, player ):

   # Iterate over spots on the board
   # and check if it belongs to this player
   for row in range(NUM_ROWS):
      for col in range(NUM_COLS):

        # If we found a piece belonging to current player
        if not board[row][col].isupper() and player == 1 \
           and board[row][col] != '' or \
	       board[row][col].isupper() and player == 2 \
	   and board[row][col] != '':

              # Yield the type of piece and coordinates
              yield ( board[row][col], (row,col) )

# walk function:
#######################################################
# Given all the directions and steps, it finds possible
# moves for a player's piece.
#
# To move in a direction:
#   N:   row - 1      
#   NE:  row-1, col+1  
#   E:   col+1
#   SE:  row+1, col+1 
#   S:   row+1
#   SE:  row+1, col-1  
#   SW:  row+1, col-1  
#   W:   col-1
#   NW:  row-1, col-1
#
#   "directions" is a tuple of tuples of all the directions
#   a piece can move. The tuple indicating direction will
#   have how much to inc/decrement in a row or column, i.e.  
#
#   For a rook, the tuple would be 
#   ((1,0),(0,1),(-1,0),(0,-1))
########################################################
def walk( directions, num_steps, start, board, player ):

      curr_pos_row = start[0]
      curr_pos_col = start[1]

      # For each direction
      for dir in directions:

         # Reset position to start
         # when we reset the direction
         curr_pos_row = start[0]
         curr_pos_col = start[1]

         # For each square in this direction
         # check if it's a possible move
         for sq in range(num_steps):

            # If the next square has your own piece on it
            # that means we cannot go any further in this direction
            # and the next square must not be the end of the board
            if (curr_pos_row + dir[0] < NUM_ROWS) and (curr_pos_row + dir[0] >= 0) and \
               (curr_pos_col + dir[1] < NUM_COLS) and (curr_pos_col + dir[1] >= 0) and \
               (    board[ curr_pos_row+dir[0] ][ curr_pos_col+dir[1] ] != ''   ) and \
               (   (board[ curr_pos_row+dir[0] ][ curr_pos_col+dir[1] ].isupper() and player == 2) or \
               (not board[ curr_pos_row+dir[0] ][ curr_pos_col+dir[1] ].isupper() and player == 1) ):
               break

            # Inc/decrement current position in this direction
            # to start/keep walking in this direction
            curr_pos_row += dir[0]
            curr_pos_col += dir[1]

            #First make sure we don't go off the board
            if curr_pos_row > 7 or curr_pos_col > 7 or \
               curr_pos_row < 0 or curr_pos_col < 0:
               break

            # If square is an empty or enemy square
            # then it's a possible move
            if (board[ curr_pos_row ][ curr_pos_col ] == '') or \
               (board[ curr_pos_row ][ curr_pos_col ].isupper() and player  == 1)  or \
               (not board[ curr_pos_row ][ curr_pos_col ].isupper() and player  == 2):


                  # Yield start position and this square.
                  # It's a possible move.
                  yield ( start, (curr_pos_row, curr_pos_col) )

            # If the previous square was an enemy,
            # we cannot move in this direction anymore
            if (    board[ curr_pos_row ][ curr_pos_col ] != ''   ) and \
               (   (board[ curr_pos_row ][ curr_pos_col ].isupper() and player == 1) or \
               (not board[ curr_pos_row ][ curr_pos_col ].isupper() and player == 2) ):
               break


# Returns a reference to whichever of the six
# move functions should be used to calculate
# the moves for this piece
def moves_function( piece ):


    def move_pawn( board, player, start_pos ):

        moves_list = []

        # Pawns have four possible moves:

        # Pawn in any position can move one
        # square forward if that square is empty

        # Check for player 1
        if player == 1 and start_pos[0]-1 >= 0:

            # If first square (north) is empty, it's a move
            if board[ start_pos[0]-1 ][ start_pos[1] ] == '':
               moves_list.append( ( start_pos, (start_pos[0]-1, start_pos[1]) ) )

            # Pawn can move diagonally left or
            # right one square if square is
            # occupied by an enemy


            #Check range of columns first
            if start_pos[1]+1 < NUM_COLS and start_pos[1]-1 >= 0:

               #Check diagonally right (NE)
               if board[ start_pos[0]-1 ][ start_pos[1]+1].isupper() and \
                  board[ start_pos[0]-1 ][ start_pos[1]+1] != '':
                  moves_list.append( ( start_pos, (start_pos[0]-1, start_pos[1]+1) ) )

               #Check diagonally left (NW)
               if board[ start_pos[0]-1 ][ start_pos[1]-1].isupper() and \
                  board[ start_pos[0]-1 ][ start_pos[1]-1] != '':
                  moves_list.append( ( start_pos, (start_pos[0]-1, start_pos[1]-1) ) )

        # Check for player 2     
        elif player == 2 and start_pos[0]+1 < NUM_ROWS:

            # If first square (south) is empty, it's a move
            if board[ start_pos[0]+1 ][ start_pos[1] ] == '':
               moves_list.append( ( start_pos, (start_pos[0]+1, start_pos[1]) ) )

            # Pawn can move diagonally left or
            # right one square if square is
            # occupied by an enemy

            #Check range of columns first
            if start_pos[1]+1 < NUM_COLS and start_pos[1]-1 >= 0:

               #Check diagonally right (SE)
               if not board[ start_pos[0]+1 ][ start_pos[1]+1].isupper() and \
                      board[ start_pos[0]+1 ][ start_pos[1]+1] != '':
                  moves_list.append( ( start_pos, (start_pos[0]+1, start_pos[1]+1) ) )

               #Check diagonally left (SW)
               if not board[ start_pos[0]+1 ][ start_pos[1]-1].isupper() and \
                      board[ start_pos[0]+1 ][ start_pos[1]-1] != '':
                  moves_list.append( ( start_pos, (start_pos[0]+1, start_pos[1]-1) ) )


        # Pawn in initial position can
        # move two squares forward if both
        # of the two squares are empty

        # If player 1 pawn in intial position,
        # walk north and add possible move to list
        if player == 1 and start_pos[0] == 6:

            # If first and second square are empty,
            # square two is a move
            if board[ start_pos[0]-1 ][ start_pos[1] ] == '' and \
               board[ start_pos[0]-2 ][ start_pos[1] ] == '':
               moves_list.append( ( start_pos, (start_pos[0]-2, start_pos[1]) ) )


        # If player 2 pawn in initial position,
        # walk south and add possible move to list
        elif player == 2 and start_pos[0] == 1:

            # If first and second square are empty,
            # square two is a move          
            if board[ start_pos[0]+1 ][ start_pos[1] ] == '' and \
               board[ start_pos[0]+2 ][ start_pos[1] ] == '':
               moves_list.append( ( start_pos, (start_pos[0]+2, start_pos[1]) ) )

        return moves_list


    def move_rook( board, player, start_pos ):

        max_possible_steps = 7
        rook_directions    = ((1,0),(0,-1),(0,1),(-1,0))
        moves_list         = []

        # Append possible move to the list
        for pos in walk( rook_directions, max_possible_steps, start_pos, board, player ):
           moves_list.append( pos )

        return moves_list


    def move_bishop( board, player, start_pos ):

        max_possible_steps   = 7
        bishop_directions    = ((1,1),(-1,1),(-1,-1),(1,-1))
        moves_list           = []

        # Append possible move to the list
        for pos in walk( bishop_directions, max_possible_steps, start_pos, board, player ):
           moves_list.append( pos )

        return moves_list


    def move_knight( board, player, start_pos ):

        # Knights move in L shapes, two squares
        # horizontally and one square vertically
        # or two squares vertically and one
        # horizontally. They can leap over pieces.

        knight_directions  = ((-2,-1), (-2,1), (2,-1),(2,1),
                              (-1,-2), (1,-2), (-1,2), (1,2))
        curr_pos_row       = start_pos[0]
        curr_pos_col       = start_pos[1]
        moves_list         = []

        # For each direction
        for dir in knight_directions:

           # Restart from initial position
           curr_pos_row = start_pos[0]
           curr_pos_col = start_pos[1]

           # Inc/decrement current position in this direction
           curr_pos_row += dir[0]
           curr_pos_col += dir[1]

           # Check if end square is within range
           if curr_pos_row >= 0 and curr_pos_row < NUM_ROWS and \
              curr_pos_col >= 0 and curr_pos_col < NUM_COLS:

               # If square is an empty or enemy square
               # then it's a possible move
               if (board[ curr_pos_row ][ curr_pos_col ] == '') or \
                  (board[ curr_pos_row ][ curr_pos_col ].isupper() and player  == 1)  or \
                  (not board[ curr_pos_row ][ curr_pos_col ].isupper() and player  == 2):

                     # Append start position and this square.
                     # It's a possible move.
                     moves_list.append( (start_pos, (curr_pos_row, curr_pos_col)) )

        return moves_list


    def move_king( board, player, start_pos ):

        max_possible_steps = 1
        king_directions    = ((1,0),(0,-1),(0,1),(-1,0),(1,1),(-1,1),(-1,-1),(1,-1))
        moves_list         = []

        # Append possible move to the list
        for pos in walk( king_directions, max_possible_steps, start_pos, board, player ):
           moves_list.append( pos )

        return moves_list


    def move_queen( board, player, start_pos ):

        max_possible_steps  = 7
        queen_directions    = ((1,0),(0,-1),(0,1),(-1,0),(1,1),(-1,1),(-1,-1),(1,-1))
        moves_list          = []

        # Append possible move to the list
        for pos in walk( queen_directions, max_possible_steps, start_pos, board, player ):
           moves_list.append( pos )

        return moves_list

    # Determine which nested function to return
    # based on the piece
    if piece.lower() == 'p':
       move_piece = move_pawn
    elif piece.lower() == 'r':
       move_piece = move_rook
    elif piece.lower() == 'b':
       move_piece = move_bishop
    elif piece.lower() == 'kn':
       move_piece = move_knight
    elif piece.lower() == 'ki':
       move_piece = move_king
    elif piece.lower() == 'q':
       move_piece = move_queen
    else:
       print("Piece to move is not valid")

    return move_piece



# Returns a list of all possible moves for the current
# player on the current board
def possible_moves( board, player ):

   piece_list = []
   trans_list = []
   all_moves  = []

   # Uses sequence from player_pieces to iterate
   # through each of the player's pieces on the board

   # Yields a tuple of the the type of piece (0)
   # and its coordinates (1).
   for piece in player_pieces( board, player ):

      # For each piece call the moves_function
      # to retrieve appropriate move function
      move_curr_piece = moves_function( piece[0] )

      # Obtain list of possible moves for this piece
      piece_list = move_curr_piece( board, player, piece[1] )

      # Translate them to match the actual board
      trans_list = translate_coordinates( piece_list )

      # Merge moves for each piece into a list to return
      all_moves.append( trans_list )

   return all_moves


# Given the list of moves, translate the coordinates
# to match an actual chess board:
# Columns: A  B  C  D  E  F  G  H
# Rows from bottom to top: 1 - 8
def translate_coordinates( moves ):

   translated_list = []

   cols = {
       'A': 0,
       'B': 1,
       'C': 2,
       'D': 3,
       'E': 4,
       'F': 5,
       'G': 6,
       'H': 7
   }

   rows = {

       1: 7,
       2: 6,
       3: 5,
       4: 4,
       5: 3,
       6: 2,
       7: 1,
       8: 0
   }

   # One move is a tuple of two tuples:
   # the start and end positions
   start_col = ''
   end_col   = ''
   start_row = ''
   end_row   = ''

   for move in moves:

      # Translate columns
      for key, value in cols.items():
            # Start position column
            if move[0][1] == value:
                start_col = key
            # End position column
            if move[1][1] == value:
                end_col = key

      # Translate rows
      for key, value in rows.items():
            # Start position row
            if move[0][0] == value:
                start_row = str(key)
            # End position row
            if move[1][0] == value:
                end_row = str(key)

      move_translated = start_col + start_row + " to " +\
                        end_col + end_row

      translated_list.append( move_translated )

   return translated_list


print("\nPlayer 1's moves (white): ")
for m in possible_moves( chess_board, 1 ):
    if m:
       print(m)

print("\nPlayer 2's moves (black): ")
for m in possible_moves( chess_board, 2 ):
    if m:
       print(m)



