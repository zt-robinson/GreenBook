import sqlite3
import os
import random
from datetime import datetime

def generate_tournament_field(tournament_id, field_size):
    """Generate a tournament field based on qualification rules"""
    
    # Database paths
    players_db_path = os.path.join(os.path.dirname(__file__), '../../data/golf_players.db')
    tournaments_db_path = os.path.join(os.path.dirname(__file__), '../../data/golf_tournaments.db')
    
    # Connect to databases
    players_conn = sqlite3.connect(players_db_path)
    players_conn.row_factory = sqlite3.Row
    tournaments_conn = sqlite3.connect(tournaments_db_path)
    tournaments_conn.row_factory = sqlite3.Row
    
    players_cur = players_conn.cursor()
    tournaments_cur = tournaments_conn.cursor()
    
    # Get tournament info
    tournaments_cur.execute('''
        SELECT t.*, s.start_date 
        FROM tournaments t 
        JOIN tournament_schedule s ON t.id = s.tournament_id 
        WHERE t.id = ?
    ''', (tournament_id,))
    tournament = tournaments_cur.fetchone()
    
    if not tournament:
        print(f"❌ Tournament {tournament_id} not found")
        return False
    
    print(f"🎯 Generating field for: {tournament['name']}")
    print(f"   Field size: {field_size}")
    print(f"   Tournament type: {tournament['tournament_type']}")
    
    # Get all players with their status
    players_cur.execute('''
        SELECT id, name, tour_card_status, exempt_thru, world_rank, 
               recent_performance, career_wins, major_wins
        FROM players 
        ORDER BY name
    ''')
    all_players = [dict(row) for row in players_cur.fetchall()]
    
    # For Year Zero, all players should have Full status
    # In a real implementation, we'd check their actual status
    field_players = []
    
    # Step 1: Get players with Full/Exempt/Lifetime status
    eligible_players = [p for p in all_players if p.get('tour_card_status') in ['Full', 'Exempt', 'Lifetime']]
    print(f"   Players with Full/Exempt/Lifetime status: {len(eligible_players)}")
    
    # For Year Zero, randomly select from all players
    if len(eligible_players) >= field_size:
        field_players = random.sample(eligible_players, field_size)
    else:
        # Take all eligible players, then fill with random selection
        field_players = eligible_players.copy()
        remaining_players = [p for p in all_players if p not in field_players]
        needed = field_size - len(field_players)
        if needed > 0:
            additional_players = random.sample(remaining_players, min(needed, len(remaining_players)))
            field_players.extend(additional_players)
    
    print(f"   Final field size: {len(field_players)}")
    
    # Randomize the field_players list
    random.shuffle(field_players)

    # Assign players to groups of 3, sequentially, with tee times starting at 09:00 and incrementing by 3 minutes per group
    group_number = 1
    minutes_offset = 0
    for i in range(0, len(field_players), 3):
        group_players = field_players[i:i+3]
        hours = 9 + (minutes_offset // 60)
        minutes = minutes_offset % 60
        tee_time = f"{hours:02d}:{minutes:02d}"
        for group_position, player in enumerate(group_players, start=1):
            entry_method = 'full_status' if player.get('tour_card_status') in ['Full', 'Exempt', 'Lifetime'] else 'random_selection'
            tournaments_cur.execute('''
                INSERT INTO tournament_fields 
                (tournament_id, player_id, entry_method, starting_position, group_number, group_position, tee_time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                tournament_id,
                player['id'],
                entry_method,
                i + group_position,
                group_number,
                group_position,
                tee_time
            ))
        group_number += 1
        minutes_offset += 3
    
    tournaments_conn.commit()
    players_conn.close()
    tournaments_conn.close()
    
    print(f"✅ Field generated successfully!")
    print(f"   Players in field: {len(field_players)}")
    print(f"   Groups: {len(field_players) // 3 + (1 if len(field_players) % 3 else 0)}")
    
    return True

def get_tournament_field(tournament_id):
    """Get the current field for a tournament"""
    
    tournaments_db_path = os.path.join(os.path.dirname(__file__), '../../data/golf_tournaments.db')
    players_db_path = os.path.join(os.path.dirname(__file__), '../../data/golf_players.db')
    
    tournaments_conn = sqlite3.connect(tournaments_db_path)
    tournaments_conn.row_factory = sqlite3.Row
    players_conn = sqlite3.connect(players_db_path)
    players_conn.row_factory = sqlite3.Row
    
    tournaments_cur = tournaments_conn.cursor()
    players_cur = players_conn.cursor()
    
    # Get field (player IDs and group info)
    tournaments_cur.execute('''
        SELECT * FROM tournament_fields
        WHERE tournament_id = ?
        ORDER BY starting_position
    ''', (tournament_id,))
    field_rows = [dict(row) for row in tournaments_cur.fetchall()]
    
    # Get all player details
    player_ids = [row['player_id'] for row in field_rows]
    if not player_ids:
        return []
    q_marks = ','.join(['?'] * len(player_ids))
    players_cur.execute(f'''SELECT id, name, country, world_rank, tour_card_status FROM players WHERE id IN ({q_marks})''', player_ids)
    player_details = {row['id']: dict(row) for row in players_cur.fetchall()}
    
    # Merge player details into field
    for row in field_rows:
        p = player_details.get(row['player_id'], {})
        row['name'] = p.get('name', 'Unknown')
        row['country'] = p.get('country', '')
        row['world_rank'] = p.get('world_rank', 0)
        row['tour_card_status'] = p.get('tour_card_status', '')
    
    tournaments_conn.close()
    players_conn.close()
    
    # Sort alphabetically by player name
    field_rows.sort(key=lambda x: x['name'])
    return field_rows

if __name__ == "__main__":
    # Generate field for Standard tournament (tournament ID 28)
    success = generate_tournament_field(28, 156)
    
    if success:
        print("\n📋 Current field:")
        field = get_tournament_field(28)
        for i, player in enumerate(field[:10]):  # Show first 10 players
            print(f"   {i+1:3d}. {player['name']} ({player['country']}) - Group {player['group_number']}, Tee: {player['tee_time']}")
        if len(field) > 10:
            print(f"   ... and {len(field) - 10} more players") 