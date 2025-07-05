import os

# Get the absolute path to the greenbook directory
GREENBOOK_DIR = os.path.dirname(os.path.abspath(__file__))

# Database paths
PLAYER_DB_PATH = os.path.join(GREENBOOK_DIR, 'data', 'golf_players.db')
COURSE_DB_PATH = os.path.join(GREENBOOK_DIR, 'data', 'golf_courses.db')
TOURNAMENT_DB_PATH = os.path.join(GREENBOOK_DIR, 'data', 'golf_tournaments.db')

# Print debug info
print(f'DEBUG: GREENBOOK_DIR = {GREENBOOK_DIR}')
print(f'DEBUG: PLAYER_DB_PATH = {PLAYER_DB_PATH}')
print(f'DEBUG: COURSE_DB_PATH = {COURSE_DB_PATH}')
print(f'DEBUG: TOURNAMENT_DB_PATH = {TOURNAMENT_DB_PATH}') 