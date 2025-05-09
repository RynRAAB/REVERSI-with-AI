def evaluate_function(grid, player):
    # dans cette fonction d'évaluation, on prend en compte trois paramètres principaux, le nombre de pions, la mobilité et les coins
    opponent = BLACK_TOKEN if player == WHITE_TOKEN else WHITE_TOKEN
    corners = [(0,0), (ROWS-1,0), (0,COLS-1), (ROWS-1,COLS-1)]
    
    # nombre de pions
    player_tokens, opponent_tokens = 0, 0
    for row in range (ROWS):
        for col in range (COLS):
            if grid[row,col] != EMPTY:
                if grid[row,col] == player :
                    player_tokens += 1
                else:
                    opponent_tokens += 1

    # mobilité
    player_moves, opponent_moves = 0, 0
    player_moves = len(get_valid_shots(grid=grid, player=player))
    opponent_moves = len(get_valid_shots(grid=grid, player=opponent))

    # coins
    player_corners, opponent_corners = 0, 0
    for y, x in corners :
        if grid[y,x] == player:
            player_corners += 1
        elif grid[y,x] == opponent:
            opponent_corners += 1

    # cacluls des différents scores
    if player_tokens + opponent_tokens != 0:
        token_score = 100 * (player_tokens - opponent_tokens) / (player_tokens + opponent_tokens)
    else :
        token_score = 0
    
    if player_moves + opponent_moves != 0:
        mobility_score = 100 * (player_moves - opponent_moves) / (player_moves + opponent_moves)
    else : 
        mobility_score = 0
    
    if player_corners + opponent_corners != 0:
        corner_score = 100 * (player_corners - opponent_corners) / (player_corners + opponent_corners)
    else:
        corner_score = 0 
    
    final_score = (50*token_score) + (0*mobility_score) + (0*corner_score)

    return final_score


def evaluate_function(grid, player):
    # dans cette fonction d'évaluation, on prend en compte trois paramètres principaux, le nombre de pions, la mobilité et les coins
    opponent = BLACK_TOKEN if player == WHITE_TOKEN else WHITE_TOKEN
    corners = [(0,0), (ROWS-1,0), (0,COLS-1), (ROWS-1,COLS-1)]
    
    # nombre de cases vides
    empty_cells = 0
    
    # nombre de pions
    player_tokens, opponent_tokens = 0, 0
    for row in range (ROWS):
        for col in range (COLS):
            if grid[row,col] == EMPTY:
                empty_cells += 1
            elif grid[row,col] == player :
                player_tokens += 1
            else:
                opponent_tokens += 1
            

    # nombre de coup possible
    player_moves, opponent_moves = 0, 0
    player_moves = len(get_valid_shots(grid=grid, player=player))
    opponent_moves = len(get_valid_shots(grid=grid, player=opponent))

    # nombre de coins
    player_corners, opponent_corners = 0, 0
    for y, x in corners :
        if grid[y,x] == player:
            player_corners += 1
        elif grid[y,x] == opponent:
            opponent_corners += 1

    # Bonus si des coups prennent directement un coin
    player_moves_list = get_valid_shots(grid=grid, player=player)

    coin_move_bonus = 0
    for move in player_moves_list:
        row, col = move[:2]
        if (row, col) in corners:
            coin_move_bonus += 50  # +50 points par coin capturable
    
    # Cases à côté des coins (dangereuses)
    dangerous_positions = [(0,1), (1,0), (1,1), (0,COLS-2), (1,COLS-1), (1,COLS-2),
                        (ROWS-2,0), (ROWS-1,1), (ROWS-2,1), (ROWS-2,COLS-1), (ROWS-1,COLS-2), (ROWS-2,COLS-2)]

    dangerous_penalty = 0
    for y, x in dangerous_positions:
        if grid[y,x] == player:
            dangerous_penalty -= 30  # -30 points par case dangereuse occupée

    # Bonus si le coups permet d'obtenir beaucoup de pions
    capture_bonus = 0
    for move in player_moves_list:
        row, col = move[:2]
        # simulate shot
        grid_copy = grid.copy()
        play_a_shot(grid=grid_copy, player=player, position=(row,col), number_of_tokens=[2,2])
        opponent_tokens_after = 0
        for r in range (ROWS):
            for c in range (COLS):
                if grid_copy[r, c] == opponent:
                    opponent_tokens_after += 1
        # nombre de pions capturés = différence entre avant et après
        captured = opponent_tokens - opponent_tokens_after
        capture_bonus += captured * 5  # +5 points par pion capturé
    
    # modification des poids en fonction du nombre de cases vides
    if empty_cells > 20:
        # Début ou milieu de partie
        token_weight = 20
        mobility_weight = 60
        corner_weight = 20
    else:
        # Fin de partie
        token_weight = 50
        mobility_weight = 30
        corner_weight = 20
    
    # calcul du poids de chaque case
    position_score = 0
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row, col] == player:
                position_score += POSITION_WEIGHTS[row][col]
            elif grid[row, col] == opponent:
                position_score -= POSITION_WEIGHTS[row][col]



    # cacluls des différents scores
    if player_tokens + opponent_tokens != 0:
        token_score = 100 * (player_tokens - opponent_tokens) / (player_tokens + opponent_tokens)
    else :
        token_score = 0
    
    if player_moves + opponent_moves != 0:
        mobility_score = 100 * (player_moves - opponent_moves) / (player_moves + opponent_moves)
    else : 
        mobility_score = 0
    
    if player_corners + opponent_corners != 0:
        corner_score = 100 * (player_corners - opponent_corners) / (player_corners + opponent_corners)
    else:
        corner_score = 0 
    
    final_score = (token_weight*token_score) + (mobility_weight*mobility_score) + (corner_weight*corner_score) + coin_move_bonus + dangerous_penalty + capture_bonus + position_score

    return final_score