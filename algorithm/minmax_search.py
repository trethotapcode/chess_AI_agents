from core.chessRules import Rules

KING_SCORE = 100
QUEEN_SCORE = 9
ROOK_SCORE = 5
BISHOP_SCORE = 3
KNIGHT_SCORE = 3
PAWN_SCORE = 1

def get_score_of_state(board, color):
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
                    score += QUEEN_SCORE
                elif cell.piece_type == 'Rook':
                    score += ROOK_SCORE 
                elif cell.piece_type == 'Bishop':
                    score += BISHOP_SCORE
                elif cell.piece_type == 'Knight':
                    score += KNIGHT_SCORE
                elif cell.piece_type == 'Pawn':
                    score += PAWN_SCORE
            else:
                if cell.piece_type == 'King':
                    score -= KING_SCORE 
                elif cell.piece_type == 'Queen':
                    score -= QUEEN_SCORE
                elif cell.piece_type == 'Rook':
                    score -= ROOK_SCORE 
                elif cell.piece_type == 'Bishop':
                    score -= BISHOP_SCORE
                elif cell.piece_type == 'Knight':
                    score -= KNIGHT_SCORE 
                elif cell.piece_type == 'Pawn':
                    score -= PAWN_SCORE 

    return score

def min_max_search(game, color, max_height, alpha=float('-inf'), beta=float('inf'), maximum_player = True):
    if max_height == 0:
        return get_score_of_state(game.board.board, color), None
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