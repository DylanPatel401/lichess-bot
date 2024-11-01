import numpy as np
import chess
import chess.pgn
import io

# Function to create a 12-channel tensor for the current board state
def create_board_tensor(board):
    tensor = np.zeros((8, 8, 12), dtype=int)
    piece_map = {
        chess.PAWN: (0, 6), chess.KNIGHT: (1, 7), chess.BISHOP: (2, 8),
        chess.ROOK: (3, 9), chess.QUEEN: (4, 10), chess.KING: (5, 11)
    }

    # Populate the tensor based on the current board state
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            color_index, piece_index = piece_map[piece.piece_type]
            # Set the appropriate channel for the piece
            if piece.color == chess.WHITE:
                tensor[chess.square_rank(square), chess.square_file(square), color_index] = 1
            else:
                tensor[chess.square_rank(square), chess.square_file(square), piece_index] = 1

    return tensor

# Function to generate state-action pairs for a single game
def generate_state_action_pairs(game):
    board = chess.Board()
    state_action_pairs = []

    # Create the initial board tensor
    state_tensor = create_board_tensor(board)

    # Iterate through the moves in the game
    for move in game.mainline_moves():
        action = (move.from_square, move.to_square)  # Representing the move
        
        # Append the state-action pair with a copy of the current tensor
        state_action_pairs.append((state_tensor.copy(), action))  # Use copy to save current state
        
        # Make the move on the board
        board.push(move)
        # Update the tensor for the new board state
        state_tensor = create_board_tensor(board)  # Update tensor for the new state

    return state_action_pairs

# Example PGN string for a single game
pgn_data = """[Event "Rated Classical game"]
[Site "https://lichess.org/j1dkb5dw"]
[White "BFG9k"]
[Black "mamalak"]
[Result "1-0"]
[UTCDate "2012.12.31"]
[UTCTime "23:01:03"]
[WhiteElo "1639"]
[BlackElo "1403"]
[WhiteRatingDiff "+5"]
[BlackRatingDiff "-8"]
[ECO "C00"]
[Opening "French Defense: Normal Variation"]
[TimeControl "600+8"]
[Termination "Normal"]

1. e4 e6 2. d4 b6 3. a3 Bb7 4. Nc3 Nh6 5. Bxh6 gxh6 6. Be2 Qg5 7. Bg4 h5 8. Nf3 Qg6 9. Nh4 Qg5 10. Bxh5 Qxh4 11. Qf3 Kd8 12. Qxf7 Nc6 13. Qe8# 1-0"""

# Load the PGN data
pgn_io = io.StringIO(pgn_data)
game = chess.pgn.read_game(pgn_io)

# Generate state-action pairs for the game
state_action_pairs = generate_state_action_pairs(game)

# Convert state-action pairs to NumPy arrays for saving
states = np.array([pair[0] for pair in state_action_pairs])  # Board state tensors
actions = np.array([pair[1] for pair in state_action_pairs])  # Actions

# Save the state-action pairs to a NumPy file
np.savez('state_action_pairs.npz', states=states, actions=actions)

# Output the total number of state-action pairs generated
print(f"Total state-action pairs generated: {len(state_action_pairs)}")
# Load the .npz file
loaded_data = np.load('state_action_pairs.npz')

# Print the keys in the loaded data
print("Keys in the NPZ file:", loaded_data.keys())

# Access the states and actions
loaded_states = loaded_data['states']
loaded_actions = loaded_data['actions']

# Print the shapes of the loaded arrays
print(f"Loaded states shape: {loaded_states.shape}")
print(f"Loaded actions shape: {loaded_actions.shape}")

# Optionally, print some of the contents
print("Example state tensor:")
print(loaded_states)  # Print the first state tensor

print("Example action:")

import pandas as pd

# Flatten the state tensors and create a DataFrame
state_flattened = loaded_states.reshape(-1, 96)  # 8x8x12 = 96
df_states = pd.DataFrame(state_flattened)

# Save to CSV
df_states.to_csv('state_action_pairs_states.csv', index=False)

# Save actions to CSV
df_actions = pd.DataFrame(loaded_actions, columns=['from_square', 'to_square'])
df_actions.to_csv('state_action_pairs_actions.csv', index=False)
