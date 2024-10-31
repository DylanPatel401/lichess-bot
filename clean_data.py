def filter_normal_games(input_file, output_file):
  """
  Reads a PGN file, filters games with normal termination, and writes them to a new file in the same format, including moves.

  Args:
      input_file (str): Path to the input PGN file.
      output_file (str): Path to the output file where filtered games will be written.
  """

  with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    lines = infile.readlines()
    is_game = False
    for i in range(len(lines)):
        line = lines[i]
        if line.startswith('[Event'):
            is_game = True
            outfile.write(line)
        elif line.startswith('[Termination "Normal"]') and is_game:
            is_game = False
            outfile.write(line)
            # Write the next two lines after the termination line so the game moves is written
            outfile.write(lines[i+1])
            outfile.write(lines[i+2])
            outfile.write('\n')
        elif is_game:
            outfile.write(line)


input_file = "C:\\Users\\Dylan Patel\\Desktop\\lichess-bot\\lichess_db_standard_rated_2013-01.pgn"
output_file = "filtered_normal_games.pgn"
filter_normal_games(input_file, output_file)

print(f"Filtered games written to: {output_file}")