from chess.pgn import read_game

# Specify the name of your file here
pgn_file_path = 'tournament.pgn'

# Open and read the file with the players to be filtered
def fetch_players_to_filter():
    try:
        with open('players_to_filter.txt', 'r', encoding='utf-8') as f:
            players_to_filter = [line.strip() for line in f.readlines()]
            return players_to_filter
    except:
        return False

def swap_name_surname(full_name):
    # Split the string by comma
    parts = full_name.split(',')
    
    # Ensure that the string contains two parts: surname and name
    if len(parts) != 2:
        return full_name  # If not, return the original string
    
    # Remove extra spaces around the name and surname
    surname = parts[0].strip()
    name = parts[1].strip()
    
    # Return the string in the format "Name Surname"
    return f"{name} {surname}"

def parse_pgn_to_wikicode(file_path):
    players_to_filter = fetch_players_to_filter()
    matches = []
    with open(file_path, 'r', encoding='utf-8') as file:
        while True:
            game = read_game(file)
            if game is None:
                break
            # Metadata extraction
            date = game.headers.get("Date", "Unknown")
            if '.' in date:
                date = date.replace('.', '-')
            white = game.headers.get("White", "Unknown")
            black = game.headers.get("Black", "Unknown")
            result = game.headers.get("Result", "Unknown")
            eco = game.headers.get("ECO", "Unknown")
            moves = game.end().board().fullmove_number
            # Check if either player is one of the players to filter
            if players_to_filter:
                if white not in players_to_filter and black not in players_to_filter:
                    continue
            # Determining the winner
            if result == "1-0":
                winner = "1"
            elif result == "0-1":
                winner = "2"
            else:
                winner = "0"
            # Formatting in Wiki format
            match_record = f"""|{{{{Match
    |finished=true
    |date={date}
    |opponent1={{{{1Opponent|{swap_name_surname(white)}|flag=}}}}
    |opponent2={{{{1Opponent|{swap_name_surname(black)}|flag=}}}}
    |map1={{{{Map|winner={winner}|white=1|eco={eco}|length={moves}}}}}
}}}}"""
            matches.append(match_record)
    return matches

# Converting data from PGN
for match in parse_pgn_to_wikicode(pgn_file_path):
    print(match)

