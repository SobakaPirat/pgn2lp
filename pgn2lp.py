from chess.pgn import read_game

# Specify the name of your file here
pgn_file_path = 'tournament.pgn'

def parse_pgn_to_wikicode(file_path):
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
    |opponent1={{{{1Opponent|{white}|flag=}}}}
    |opponent2={{{{1Opponent|{black}|flag=}}}}
    |map1={{{{Map|winner={winner}|white=1|eco={eco}|moves={moves}}}}}
}}}}"""
            matches.append(match_record)
    return matches

# Converting data from PGN
for match in parse_pgn_to_wikicode(pgn_file_path):
    print(match)


