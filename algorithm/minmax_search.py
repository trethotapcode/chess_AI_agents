from core.chessRules import Rules

KING_SCORE = 100
QUEEN_SCORE = 9
ROOK_SCORE = 5
BISHOP_SCORE = 3.5
KNIGHT_SCORE = 3
PAWN_SCORE = 1

KNIGHT_POS_SCORE =  [[1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 2, 2, 2, 2, 2, 2, 1],
                     [1, 2, 3, 3, 3, 3, 2, 1],
                     [1, 2, 3, 4, 4, 3, 2, 1],
                     [1, 2, 3, 4, 4, 3, 2, 1],
                     [1, 2, 3, 3, 3, 3, 2, 1],
                     [1, 2, 2, 2, 2, 2, 2, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1]]

BISHOP_POS_SCORE =  [[4, 3, 2, 1, 1, 2, 3, 4],
                     [3, 4, 3, 2, 2, 3, 4, 3],
                     [2, 3, 4, 3, 3, 4, 3, 2],
                     [1, 2, 3, 4, 4, 3, 2, 1],
                     [1, 2, 3, 4, 4, 3, 2, 1],
                     [2, 3, 4, 3, 3, 4, 3, 2],
                     [3, 4, 3, 2, 2, 3, 4, 3],
                     [4, 3, 2, 1, 1, 2, 3, 4]]

QUEEN_POS_SCORE =   [[1, 1, 1, 3, 1, 1, 1, 1],
                     [1, 2, 3, 3, 3, 1, 1, 1],
                     [1, 4, 3, 3, 3, 4, 2, 1],
                     [1, 2, 3, 3, 3, 2, 2, 1],
                     [1, 2, 3, 3, 3, 2, 2, 1],
                     [1, 4, 3, 3, 3, 4, 2, 1],
                     [1, 2, 3, 3, 3, 1, 1, 1],
                     [1, 1, 1, 3, 1, 1, 1, 1]]

ROOK_POS_SCORE =    [[4, 3, 4, 4, 4, 4, 3, 4],
                     [4, 4, 4, 4, 4, 4, 4, 4],
                     [1, 1, 2, 3, 3, 2, 1, 1],
                     [1, 2, 3, 4, 4, 3, 2, 1],
                     [1, 2, 3, 4, 4, 3, 2, 1],
                     [1, 1, 2, 3, 3, 2, 1, 1],
                     [4, 4, 4, 4, 4, 4, 4, 4],
                     [4, 3, 4, 4, 4, 4, 3, 4]]

WPAWN_POS_SCORE =   [[8, 8, 8, 8, 8, 8, 8, 8],
                     [8, 8, 8, 8, 8, 8, 8, 8],
                     [5, 6, 6, 7, 7, 6, 6, 5],
                     [2, 3, 3, 5, 5, 3, 3, 2],
                     [1, 2, 3, 4, 4, 3, 2, 1],
                     [1, 2, 3, 3, 3, 3, 2, 1],
                     [1, 1, 1, 0, 0, 1, 1, 1],
                     [0, 0, 0, 0, 0, 0, 0, 0]]

BPAWN_POS_SCORE =   [[0, 0, 0, 0, 0, 0, 0, 0],
                     [1, 1, 1, 0, 0, 1, 1, 1],
                     [1, 2, 3, 3, 3, 3, 2, 1],
                     [1, 2, 3, 4, 4, 3, 2, 1],
                     [2, 3, 3, 5, 5, 3, 3, 2],
                     [5, 6, 6, 7, 7, 6, 6, 5],
                     [8, 8, 8, 8, 8, 8, 8, 8],
                     [8, 8, 8, 8, 8, 8, 8, 8]]


def get_score_of_state(game, color):
    if game.check_status(color) == "checkmate":
        return 200
    if game.check_status(color) == "draw":
        return 0
    board = game.board.board
    score = 0

    for i in range(8):
        for j in range(8):
            cell = board[i][j]
            if cell is None:
                continue
            if cell.color == color:
                if cell.piece_type == 'King':
                    score += KING_SCORE
                elif cell.piece_type == 'Queen':
                    score += QUEEN_SCORE + 0.1 * QUEEN_POS_SCORE[i][j]
                elif cell.piece_type == 'Rook':
                    score += ROOK_SCORE + 0.1 * ROOK_POS_SCORE[i][j]
                elif cell.piece_type == 'Bishop':
                    score += BISHOP_SCORE + 0.1 * BISHOP_POS_SCORE[i][j]
                elif cell.piece_type == 'Knight':
                    score += KNIGHT_SCORE + 0.1 * KNIGHT_POS_SCORE[i][j]
                elif cell.piece_type == 'Pawn':
                    score += PAWN_SCORE + 0.1 * (WPAWN_POS_SCORE[i][j] if cell.color == 'white' else BPAWN_POS_SCORE[i][j])
            else:
                if cell.piece_type == 'King':
                    score -= KING_SCORE 
                elif cell.piece_type == 'Queen':
                    score -= QUEEN_SCORE + 0.1 * QUEEN_POS_SCORE[i][j]
                elif cell.piece_type == 'Rook':
                    score -= ROOK_SCORE + 0.1 * ROOK_POS_SCORE[i][j]
                elif cell.piece_type == 'Bishop':
                    score -= BISHOP_SCORE + 0.1 * BISHOP_POS_SCORE[i][j]
                elif cell.piece_type == 'Knight':
                    score -= KNIGHT_SCORE + 0.1 * KNIGHT_POS_SCORE[i][j]
                elif cell.piece_type == 'Pawn':
                    score -= PAWN_SCORE + 0.1 * (WPAWN_POS_SCORE[i][j] if cell.color != 'white' else BPAWN_POS_SCORE[i][j])

    return score

def min_max_search(game, color, max_height, alpha=float('-inf'), beta=float('inf'), maximum_player = True):
    if max_height == 0:
        return get_score_of_state(game, color), None
    moves = []
    for row in game.board.board:
        # cell maybe contains piece or None.
        if maximum_player:
            for cell in row:
                if cell is not None and cell.color == color:
                    valid_moves = game.generate_legal_moves(piece=cell)
                    for element in valid_moves:
                        moves.append((cell, element))
        else:
            for cell in row:
                if cell is not None and cell.color != color:
                    valid_moves = game.generate_legal_moves(piece=cell)
                    for element in valid_moves:
                        moves.append((cell, element))

    if maximum_player:
        maxEval = float('-inf')
        best_move = []

        for move in moves:
            piece = move[0]
            original_position = piece.position
            r_new, c_new = move[1]
            captured_piece = game.board.board[r_new][c_new]
            game.make_move(piece, move[1])
            

            eval, _ = min_max_search(game, color, max_height-1, alpha, beta, False)
            if eval > maxEval:
                best_move = [move]
            elif eval == maxEval:
                best_move.append(move)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            game.board.board[original_position[0]][original_position[1]] = piece
            piece.position = original_position
            game.board.board[r_new][c_new] = captured_piece
            if beta <= alpha:
                break
        return maxEval, best_move

    else:
        minEval = float('inf')
        best_move = []
        for move in moves:
            piece = move[0]
            original_position = piece.position
            r_new, c_new = move[1]
            captured_piece = game.board.board[r_new][c_new]

            game.make_move(piece, move[1])
            
            eval, _ = min_max_search(game, color, max_height-1, alpha, beta, True)
            if eval < minEval:
                best_move = [move]
            elif eval == minEval:
                best_move.append(move)                
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            game.board.board[original_position[0]][original_position[1]] = piece
            piece.position = original_position
            game.board.board[r_new][c_new] = captured_piece
            if beta <= alpha:
                break
        return minEval, best_move