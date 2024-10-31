def filter_normal_games(input_file, output_file):
  """
  Reads a PGN file, filters games with normal termination, and writes them to a new file in the same format.

  Args:
      input_file (str): Path to the input PGN file.
      output_file (str): Path to the output file where filtered games will be written.
  """

  with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    is_game = False
    for line in infile:
      if line.startswith('[Event'):
        is_game = True
        outfile.write(line)  # Write the event line
      elif line.startswith('[Termination "Normal"]') and is_game:
        is_game = False
        outfile.write(line)  # Write the termination line
        outfile.write('\n')  # Add a newline to separate games
      elif is_game:
        outfile.write(line)  # Write other lines of the game

# Example usage
input_file = "C:\\Users\\Dylan Patel\\Desktop\\lichess-bot\\lichess_db_standard_rated_2013-01.pgn"
output_file = "filtered_normal_games.pgn"  # Change this to desired output filename
filter_normal_games(input_file, output_file)

print(f"Filtered games written to: {output_file}")