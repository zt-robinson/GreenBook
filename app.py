from flask import Flask, render_template, redirect, url_for, request
import sqlite3
import os
from datetime import datetime, timedelta
import sys
sys.path.append(os.path.dirname(__file__))
from scripts.tournaments.utilities.generate_tournament_field import get_tournament_field
import pytz
import random
import math
from config import PLAYER_DB_PATH, COURSE_DB_PATH, TOURNAMENT_DB_PATH
import pandas as pd

app = Flask(__name__)

# In-memory simulation state (for demo; will move to persistent storage later)
sim_state = {}

def get_all_players():
    conn = sqlite3.connect(PLAYER_DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM players ORDER BY tour_rank ASC')
    players = cur.fetchall()
    conn.close()
    return players

def get_all_courses():
    conn = sqlite3.connect(COURSE_DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM courses ORDER BY name ASC')
    courses = cur.fetchall()
    conn.close()
    return courses

def get_counts():
    """Get counts for the home page statistics"""
    conn_p = sqlite3.connect(PLAYER_DB_PATH)
    cur_p = conn_p.cursor()
    cur_p.execute('SELECT COUNT(*) FROM players')
    player_count = cur_p.fetchone()[0]
    conn_p.close()

    conn_c = sqlite3.connect(COURSE_DB_PATH)
    cur_c = conn_c.cursor()
    cur_c.execute('SELECT COUNT(*) FROM courses')
    course_count = cur_c.fetchone()[0]
    conn_c.close()
    return player_count, course_count

def country_to_flag(country):
    # Simple mapping for common countries; fallback to empty string
    flags = {
        'USA': '🇺🇸', 'United States': '🇺🇸', 'England': '🇬🇧', 'Canada': '🇨🇦', 'Australia': '🇦🇺',
        'Ireland': '🇮🇪', 'New Zealand': '🇳🇿', 'Japan': '🇯🇵', 'Spain': '🇪🇸', 'Germany': '🇩🇪',
        'Sweden': '🇸🇪', 'France': '🇫🇷', 'Italy': '🇮🇹', 'Netherlands': '🇳🇱', 'Denmark': '🇩🇰',
        'Norway': '🇳🇴', 'Finland': '🇫🇮', 'Austria': '🇦🇹', 'Switzerland': '🇨🇭', 'Belgium': '🇧🇪',
        'Portugal': '🇵🇹', 'Brazil': '🇧🇷', 'Mexico': '🇲🇽', 'Argentina': '🇦🇷', 'Chile': '🇨🇱',
        'Colombia': '🇨🇴', 'Czech Republic': '🇨🇿', 'Poland': '🇵🇱', 'Hungary': '🇭🇺', 'Turkey': '🇹🇷',
        'Romania': '🇷🇴', 'Croatia': '🇭🇷', 'Slovenia': '🇸🇮', 'Slovakia': '🇸🇰', 'Lithuania': '🇱🇹',
        'Latvia': '🇱🇻', 'Estonia': '🇪🇪', 'Iceland': '🇮🇸', 'Indonesia': '🇮🇩', 'Vietnam': '🇻🇳',
        'Philippines': '🇵🇭', 'French Canada': '🇨🇦', 'Belgium (Dutch)': '🇧🇪',
        # Add more as needed
    }
    return flags.get(country, '')

def country_to_flag_iso(country):
    mapping = {
        'USA': 'us',
        'England': 'gb',
        'Scotland': 'gb-sct',  # Use 'gb-sct' if you have the SVG, else fallback to 'gb'
        'Ireland': 'ie',
        'Australia': 'au',
        'Canada': 'ca',
        'Japan': 'jp',
        'Germany': 'de',
        'Sweden': 'se',
        'New Zealand': 'nz',
        'France': 'fr',
        'Italy': 'it',
        'Netherlands': 'nl',
        'Denmark': 'dk',
        'Norway': 'no',
        'Finland': 'fi',
        'Austria': 'at',
        'Switzerland': 'ch',
        'Belgium': 'be',
        'Portugal': 'pt',
        'Brazil': 'br',
        'Mexico': 'mx',
        'Argentina': 'ar',
        'Chile': 'cl',
        'Colombia': 'co',
        'Czech Republic': 'cz',
        'Poland': 'pl',
        'Hungary': 'hu',
        'Turkey': 'tr',
        'Romania': 'ro',
        'Croatia': 'hr',
        'Slovenia': 'si',
        'Slovakia': 'sk',
        'Lithuania': 'lt',
        'Latvia': 'lv',
        'Estonia': 'ee',
        'Iceland': 'is',
        'Indonesia': 'id',
        'Vietnam': 'vn',
        'Philippines': 'ph',
        'French Canada': 'ca',
        'Belgium (Dutch)': 'be',
    }
    return mapping.get(country, '')

@app.route('/')
def home():
    player_count, course_count = get_counts()
    return render_template('home.html', player_count=player_count, course_count=course_count)

@app.route('/player-history')
def player_history():
    # Pagination logic
    page = request.args.get('page', 1, type=int)
    per_page = 25
    players = get_all_players()
    players = [dict(player) for player in players]  # Convert to dicts for mutability
    total_players = len(players)
    total_pages = (total_players + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    players_page = players[start:end]
    # Add the new public fields to each player
    for player in players_page:
        player['events'] = 0  # Will be calculated from tournament participation later
        player['tour_championship_points'] = 0
        player['points_behind_lead'] = 0
        player['wins'] = player.get('career_wins', 0)  # Use existing career_wins for now
    return render_template('players.html', players=players_page, country_to_flag_iso=country_to_flag_iso, page=page, total_pages=total_pages)

@app.route('/courses')
def courses():
    conn = sqlite3.connect(COURSE_DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    # Load elevation data
    elev_df = pd.read_csv('data/cities_with_elevation.csv')
    cur.execute('''
        SELECT c.id, c.name, c.location, c.city, c.state_country, c.total_yardage as yardage, c.total_par as par, c.prestige_level as prestige, c.est_year,
               c.slope_rating, c.course_rating,
               cc.green_speed, cc.hazard_density, cc.rough_length, cc.narrowness_factor,
               cc.elevation, cc.terrain_difficulty, cc.turf_firmness, cc.design_strategy
        FROM courses c
        LEFT JOIN course_characteristics cc ON c.id = cc.course_id
        ORDER BY c.name
    ''')
    courses = cur.fetchall()
    print('DEBUG: courses fetched from DB:', courses)
    courses = [dict(row) for row in courses]
    if courses:
        print('DEBUG: first course dict:', courses[0])
    for course in courses:
        cur.execute('''
            SELECT hole_number, par, handicap, yardage
            FROM holes 
            WHERE course_id = ? 
            ORDER BY hole_number
        ''', (course['id'],))
        holes = cur.fetchall()
        course['holes'] = [dict(hole) for hole in holes]
        course['total_par'] = sum(hole['par'] for hole in course['holes'])
        course['slope_rating'] = course.get('slope_rating')
        course['course_rating'] = course.get('course_rating')
        # Elevation lookup
        city = course.get('city')
        state = course.get('state_country')
        elev_row = elev_df[(elev_df['city'] == city) & (elev_df['state'] == state)]
        if not elev_row.empty:
            elev_ft = elev_row.iloc[0]['elevation_ft']
            try:
                elev_ft = int(round(float(elev_ft)))
                elev_ft = max(0, elev_ft)  # Clamp negative to zero
                course['display_elevation'] = f"{elev_ft:,} ft"
            except Exception:
                print(f"DEBUG: Could not parse elevation for {city}, {state}: {elev_row.iloc[0]['elevation_ft']}")
                course['display_elevation'] = 'N/A'
        else:
            print(f"DEBUG: No elevation found for {city}, {state}")
            course['display_elevation'] = 'N/A'
        # Rough length: 2 to 4.5 inches
        rough_length = course.get('rough_length') or 0.2
        course['display_rough'] = f"{round(2 + (rough_length - 0.2) / 0.7 * 2.5, 1)} in"
        # Green speed: 10.5 to 13.5 ft
        green_speed = course.get('green_speed') or 0.3
        course['display_stimp'] = f"{round(10.5 + (green_speed - 0.3) / 0.7 * 3, 1)} ft"
        # Turf firmness: thresholds
        turf_firmness = course.get('turf_firmness') or 0.3
        if turf_firmness < 0.5:
            course['display_firmness'] = 'Soft'
        elif turf_firmness < 0.7:
            course['display_firmness'] = 'Medium'
        else:
            course['display_firmness'] = 'Firm'
        # Terrain type: thresholds
        terrain = course.get('terrain_difficulty') or 0.1
        if terrain < 0.3:
            course['display_terrain'] = 'Flat'
        elif terrain < 0.6:
            course['display_terrain'] = 'Moderate'
        else:
            course['display_terrain'] = 'Hilly'
    conn.close()
    return render_template('courses.html', courses=courses)

@app.route('/schedule')
def schedule():
    import sqlite3
    import os
    tournaments_db_path = os.path.join(os.path.dirname(__file__), 'data/golf_tournaments.db')
    courses_db_path = os.path.join(os.path.dirname(__file__), 'data/golf_courses.db')

    # Fetch tournaments and schedule with new columns
    tconn = sqlite3.connect(tournaments_db_path)
    tconn.row_factory = sqlite3.Row
    tcur = tconn.cursor()
    tcur.execute('''
        SELECT t.*, s.start_date, s.round_1_start, s.round_2_start, s.round_3_start, s.round_4_start
        FROM tournaments t
        JOIN tournament_schedule s ON t.id = s.tournament_id
        ORDER BY t.season_number, t.week_number
    ''')
    tournaments = [dict(row) for row in tcur.fetchall()]
    tconn.close()

    # Fetch courses
    cconn = sqlite3.connect(courses_db_path)
    cconn.row_factory = sqlite3.Row
    ccur = cconn.cursor()
    ccur.execute('SELECT id, name FROM courses')
    courses = {row['id']: row['name'] for row in ccur.fetchall()}
    cconn.close()

    def format_ampm(timestr):
        try:
            dt = datetime.strptime(timestr, '%H:%M')
            hour = dt.hour
            minute = dt.minute
            suffix = 'a' if hour < 12 else 'p'
            hour12 = hour % 12
            if hour12 == 0:
                hour12 = 12
            return f"{hour12}:{minute:02d}{suffix}"
        except Exception:
            return timestr

    for t in tournaments:
        t['course_name'] = courses.get(t['course_id'], 'Unknown')
        # Defensive: handle missing or None start_date
        if t['start_date']:
            try:
                dt = datetime.strptime(t['start_date'], '%Y-%m-%d')
                t['start_date_formatted'] = dt.strftime('%B %d, %Y').replace(' 0', ' ')
            except Exception as e:
                t['start_date_formatted'] = t['start_date']
        else:
            t['start_date_formatted'] = 'None'
        # Format round times
        t['round_1_start_fmt'] = format_ampm(t['round_1_start'])
        t['round_2_start_fmt'] = format_ampm(t['round_2_start'])
        t['round_3_start_fmt'] = format_ampm(t['round_3_start'])
        t['round_4_start_fmt'] = format_ampm(t['round_4_start'])

    return render_template('schedule.html', tournaments=tournaments)

def get_local_round_time(start_date, round_time_str, course_timezone):
    """Convert round time to local timezone"""
    try:
        from zoneinfo import ZoneInfo  # Python 3.9+
        tz = ZoneInfo(course_timezone)
    except ImportError:
        import pytz
        tz = pytz.timezone(course_timezone)
    
    dt_naive = datetime.strptime(f"{start_date} {round_time_str}", '%Y-%m-%d %H:%M')
    dt_local = tz.localize(dt_naive)
    return dt_local

def get_signature_event_1_field():
    """
    Custom field logic for Signature Event #1 provisional field.
    Uses the new events database structure.
    """
    import sqlite3
    import os
    from pathlib import Path
    
    # Use the new events database
    db_path = Path(__file__).parent / "data" / "events.db"
    if not db_path.exists():
        print(f"[ERROR] Events database not found at {db_path}")
        return []
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    field = set()  # Use set to avoid duplicates
    FIELD_SIZE = 75  # Cap at 75 players
    
    print("Generating Signature Event #1 field...")
    
    # Priority 1: Winners of all events from Season 10
    print("Priority 1: Season 10 event winners")
    cursor.execute("""
        SELECT event_name, "1" as winner 
        FROM events 
        WHERE season = 10 
        ORDER BY season_event
    """)
    season_10_winners = cursor.fetchall()
    print(f"Found {len(season_10_winners)} Season 10 events")
    
    for event_name, winner in season_10_winners:
        field.add(winner)
        print(f"  {event_name}: {winner}")
    
    print(f"Priority 1 total: {len(field)} players")
    
    # Priority 2: Top 5 from Season 10 final standings
    print("Priority 2: Season 10 final standings top 5")
    cursor.execute("""
        SELECT "1", "2", "3", "4", "5" 
        FROM season_standings 
        WHERE season = 10
    """)
    season_10_top5 = cursor.fetchone()
    
    if season_10_top5:
        for player in season_10_top5:
            field.add(player)
        print(f"Season 10 top 5: {season_10_top5}")
        print(f"Priority 2 total: {len(field)} players")
    
    # Priority 3: Winners of majors and continental championships from seasons 6-9
    print("Priority 3: Major and Continental winners from seasons 6-9")
    cursor.execute("""
        SELECT season, event_name, "1" as winner 
        FROM events 
        WHERE (type = 'Major' OR type = 'Mini Major') 
        AND season BETWEEN 6 AND 9
        ORDER BY season, season_event
    """)
    major_continental_winners = cursor.fetchall()
    
    for season, event_name, winner in major_continental_winners:
        field.add(winner)
        print(f"  Season {season} {event_name}: {winner}")
    
    print(f"Priority 3 total: {len(field)} players")
    
    # Priority 4: Past Signature Event #1 winners (seasons 1-9)
    print("Priority 4: Past Signature Event #1 winners")
    cursor.execute("""
        SELECT season, "1" as winner 
        FROM events 
        WHERE event_code = 'SIG_1' AND season BETWEEN 1 AND 9
        ORDER BY season
    """)
    past_signature_winners = cursor.fetchall()
    
    for season, winner in past_signature_winners:
        field.add(winner)
        print(f"  Season {season}: {winner}")
    
    print(f"Priority 4 total: {len(field)} players")
    
    # Priority 5: Top players from Season 10 standings (fill remaining spots)
    print("Priority 5: Top players from Season 10 standings")
    cursor.execute("""
        SELECT "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
               "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
               "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
               "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
               "41", "42", "43", "44", "45", "46", "47", "48", "49", "50",
               "51", "52", "53", "54", "55", "56", "57", "58", "59", "60",
               "61", "62", "63", "64", "65", "66", "67", "68", "69", "70",
               "71", "72", "73", "74", "75"
        FROM season_standings 
        WHERE season = 10
    """)
    season_10_top75 = cursor.fetchone()
    
    if season_10_top75:
        for player in season_10_top75:
            if len(field) >= FIELD_SIZE:  # Cap at 75 players
                break
            field.add(player)
    
    print(f"Final field size: {len(field)} players")
    
    # Convert to sorted list of player dicts (sorted by last name)
    field_list = sorted(list(field), key=lambda name: name.split()[-1] if name else '')
    field_dicts = [{'name': name} for name in field_list]
    
    conn.close()
    return field_dicts

@app.route('/tournament/<int:tournament_id>')
def tournament_detail(tournament_id):
    """Show tournament details, field, and leaderboard"""
    import sqlite3
    import os
    
    tournaments_db_path = os.path.join(os.path.dirname(__file__), 'data/golf_tournaments.db')
    courses_db_path = os.path.join(os.path.dirname(__file__), 'data/golf_courses.db')
    
    # Get tournament details
    tconn = sqlite3.connect(tournaments_db_path)
    tconn.row_factory = sqlite3.Row
    tcur = tconn.cursor()
    tcur.execute('''
        SELECT t.*, s.start_date, s.round_1_start, s.round_2_start, s.round_3_start, s.round_4_start
        FROM tournaments t
        JOIN tournament_schedule s ON t.id = s.tournament_id
        WHERE t.id = ?
    ''', (tournament_id,))
    tournament = tcur.fetchone()
    tconn.close()
    
    if not tournament:
        return "Tournament not found", 404
    
    tournament = dict(tournament)
    
    # Fetch course info from courses DB
    cconn = sqlite3.connect(courses_db_path)
    cconn.row_factory = sqlite3.Row
    ccur = cconn.cursor()
    ccur.execute('SELECT name, location FROM courses WHERE id = ?', (tournament['course_id'],))
    course = ccur.fetchone()
    cconn.close()
    if course:
        tournament['course_name'] = course['name']
        tournament['course_location'] = course['location']
    else:
        tournament['course_name'] = 'Unknown'
        tournament['course_location'] = 'Unknown'

    # Map tournament_type to user-friendly string
    type_map = {
        'regular': 'Standard Tour Event',
        'open': 'Open Tournament',
        'invitational': 'Invitational Tournament',
        'major': 'Major Championship',
    }
    tournament['type_display'] = type_map.get(tournament['tournament_type'], tournament['tournament_type'].title())

    # Format purse amount for display
    tournament['purse_amount_formatted'] = "{:,}".format(int(round(tournament.get('purse_amount', 0))))
    
    # Format dates and times
    # Defensive: handle missing or None start_date
    if tournament['start_date']:
        try:
            dt = datetime.strptime(tournament['start_date'], '%Y-%m-%d')
            tournament['start_date_formatted'] = dt.strftime('%B %d, %Y').replace(' 0', ' ')
        except Exception as e:
            tournament['start_date_formatted'] = tournament['start_date']
    else:
        tournament['start_date_formatted'] = 'None'

    # Compute timezone-aware ISO string for Boston (America/New_York)
    try:
        # from datetime import datetime  # <-- REMOVE THIS LINE
        try:
            from zoneinfo import ZoneInfo  # Python 3.9+
            ny_tz = ZoneInfo('America/New_York')
            dt_naive = datetime.strptime((tournament['start_date'] or '2025-01-01') + ' ' + tournament['round_1_start'], '%Y-%m-%d %H:%M')
            dt_ny = dt_naive.replace(tzinfo=ny_tz)
        except ImportError:
            import pytz
            ny_tz = pytz.timezone('America/New_York')
            dt_naive = datetime.strptime((tournament['start_date'] or '2025-01-01') + ' ' + tournament['round_1_start'], '%Y-%m-%d %H:%M')
            dt_ny = ny_tz.localize(dt_naive)
        tournament['start_iso_ny'] = dt_ny.isoformat()
    except Exception as e:
        tournament['start_iso_ny'] = ''
    
    def format_ampm(timestr):
        try:
            dt = datetime.strptime(timestr, '%H:%M')
            hour = dt.hour
            minute = dt.minute
            suffix = 'a' if hour < 12 else 'p'
            hour12 = hour % 12
            if hour12 == 0:
                hour12 = 12
            return f"{hour12}:{minute:02d}{suffix}"
        except Exception:
            return timestr
    
    tournament['round_1_start_fmt'] = format_ampm(tournament['round_1_start'])
    tournament['round_2_start_fmt'] = format_ampm(tournament['round_2_start'])
    tournament['round_3_start_fmt'] = format_ampm(tournament['round_3_start'])
    tournament['round_4_start_fmt'] = format_ampm(tournament['round_4_start'])
    
    # Get course name and location
    cconn = sqlite3.connect(courses_db_path)
    cconn.row_factory = sqlite3.Row
    ccur = cconn.cursor()
    ccur.execute('SELECT name, location FROM courses WHERE id = ?', (tournament['course_id'],))
    course = ccur.fetchone()
    if course:
        tournament['course_name'] = course['name']
        tournament['location'] = course['location']
    else:
        tournament['course_name'] = 'Unknown'
        tournament['location'] = ''
    cconn.close()
    
    # PHASE LOGIC: Provisional vs Finalized
    today = datetime.now().date()
    start_date = datetime.strptime(tournament['start_date'], '%Y-%m-%d').date()
    days_until_start = (start_date - today).days
    show_provisional = days_until_start > 1
    provisional_qualifiers = []
    if show_provisional:
        if tournament['name'] == "Signature Event #1":
            # Use custom logic for Signature Event #1
            provisional_qualifiers = get_signature_event_1_field()
        else:
            # Existing logic for other events
            all_players = get_all_players()
            sorted_players = sorted(all_players, key=lambda p: p['name'].split()[-1].lower())
            field_size = tournament.get('field_size', 156)
            provisional_qualifiers = sorted_players[:field_size]
        # Split into 2 columns for better spacing
        col_count = 2
        col_length = (len(provisional_qualifiers) + col_count - 1) // col_count
        qualifier_columns = [provisional_qualifiers[i*col_length:(i+1)*col_length] for i in range(col_count)]
    else:
        # Get tournament field
        field = get_tournament_field(tournament_id)
        # Group players by group_number, sort each group by last name
        from collections import defaultdict
        import re
        grouped_field = defaultdict(list)
        for player in field:
            name_parts = re.split(r'\\s+', player['name'].strip())
            last_name = name_parts[-1] if name_parts else player['name']
            player['last_name'] = last_name
            grouped_field[player['group_number']].append(player)
        sorted_groups = []
        for group_num in sorted(grouped_field.keys()):
            group_players = sorted(grouped_field[group_num], key=lambda p: p['last_name'])
            # Always get tee_time from the first player in the group (DB is correct)
            tee_time = group_players[0]['tee_time'] if group_players else ''
            sorted_groups.append({'group_number': group_num, 'players': group_players, 'tee_time': tee_time})
        # Debug print to verify group order and tee times
        print("DEBUG: Groups passed to template:")
        for g in sorted_groups:
            print(f"  Group {g['group_number']}: {g['tee_time']}")
    # Remove the payout_structure query and use points_to_winner from the tournament record
    winner_points = tournament.get('points_to_winner', 0)
    
    # Use cut line from new database columns
    cut_line_type = tournament.get('cut_line_type', 'position')
    cut_line_value = tournament.get('cut_line_value', 65)
    
    if cut_line_type == 'none':
        cut_line = 'No Cut'
    elif cut_line_type == 'position':
        cut_line = str(cut_line_value) if cut_line_value is not None else 'Unknown'
    else:
        cut_line = 'Standard'
    
    print(f"DEBUG: tournament['start_date_formatted'] = {tournament['start_date_formatted']}")

    # Generate weather forecast
    weather_forecast = generate_weather_forecast(tournament['course_id'], tournament['start_date'], 4)

    return render_template('tournament_detail.html', tournament=tournament, groups=sorted_groups if not show_provisional else [], provisional_qualifiers=provisional_qualifiers, qualifier_columns=qualifier_columns if show_provisional else None, country_to_flag_iso=country_to_flag_iso, winner_points=winner_points, cut_line=cut_line, show_provisional=show_provisional, weather_forecast=weather_forecast)

@app.route('/standings')
def standings():
    """Display real Season 10 final standings from the database"""
    # Connect to both databases
    seasons_db_path = os.path.join(os.path.dirname(__file__), 'data/golf_seasons.db')
    seasons_conn = sqlite3.connect(seasons_db_path)
    players_conn = sqlite3.connect(PLAYER_DB_PATH)
    
    seasons_conn.row_factory = sqlite3.Row
    players_conn.row_factory = sqlite3.Row
    
    try:
        # Get Season 10 standings
        seasons_cur = seasons_conn.cursor()
        seasons_cur.execute('''
            SELECT rank as final_rank, tour_points as total_season_points, 
                   events_played, wins, top_10s, money_earned, player_id
            FROM season_standings
            WHERE season_number = 10
            ORDER BY rank ASC
            LIMIT 100
        ''')
        
        standings_data = [dict(row) for row in seasons_cur.fetchall()]
        
        # Get player details from players database
        if standings_data:
            player_ids = [row['player_id'] for row in standings_data]
            q_marks = ','.join(['?'] * len(player_ids))
            
            players_cur = players_conn.cursor()
            players_cur.execute(f'''
                SELECT id, name, nationality
                FROM players 
                WHERE id IN ({q_marks})
            ''', player_ids)
            
            player_details = {row[0]: {'name': row[1], 'nationality': row[2]} 
                            for row in players_cur.fetchall()}
            
            # Merge player details into standings data
            for row in standings_data:
                player_info = player_details.get(row['player_id'], {})
                row['name'] = player_info.get('name', 'Unknown')
                row['nationality'] = player_info.get('nationality', 'Unknown')
        
        return render_template('standings.html', standings=standings_data)
        
    finally:
        seasons_conn.close()
        players_conn.close()

def generate_weather_forecast(course_id, start_date, num_rounds=4):
    """
    Generate realistic weather forecast for tournament rounds based on course monthly averages.
    If the tournament is more than 1 week away, use monthly averages with small unique random variations for each round (static per page load).
    """
    try:
        courses_db_path = os.path.join(os.path.dirname(__file__), 'data/golf_courses.db')
        conn = sqlite3.connect(courses_db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        weather_forecast = []
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        today = datetime.now()
        days_until_start = (start_dt.date() - today.date()).days
        
        for round_num in range(num_rounds):
            round_date = start_dt + timedelta(days=round_num)
            month = round_date.month
            cur.execute('''
                SELECT cloud_cover, wind_speed, rain_probability, humidity, 
                       min_temp, mean_temp, max_temp
                FROM course_monthly_weather 
                WHERE course_id = ? AND month = ?
            ''', (course_id, month))
            row = cur.fetchone()
            if not row:
                weather_forecast.append({
                    'temp': 70,
                    'humidity': 50,
                    'wind': 10,
                    'rain_prob': 20,
                    'cloud_cover': 30,
                    'icon': '☀️'
                })
                continue
            if days_until_start > 7:
                # Iterative static forecast: round 1 = monthly avg, rounds 2-4 drift from previous round
                if round_num == 0:
                    temp = max(32, min(100, row['mean_temp']))
                    wind = max(0, row['wind_speed'])
                    rain_prob = max(0, min(100, row['rain_probability']))
                    humidity = max(20, min(100, row['humidity']))
                    cloud_cover = max(0, min(100, row['cloud_cover']))
                else:
                    prev = weather_forecast[-1]
                    temp = max(32, min(100, prev['temp'] + random.uniform(-2, 2)))
                    wind = max(0, prev['wind'] + random.uniform(-1, 1))
                    rain_prob = max(0, min(100, prev['rain_prob'] + random.uniform(-3, 3)))
                    humidity = max(20, min(100, prev['humidity'] + random.uniform(-3, 3)))
                    cloud_cover = max(0, min(100, prev['cloud_cover'] + random.uniform(-3, 3)))
            else:
                # Dynamic forecast: use larger variance as before
                base_temp = row['mean_temp']
                temp = max(32, min(100, base_temp + random.uniform(-5, 5)))
                base_wind = row['wind_speed']
                wind = max(0, base_wind + random.uniform(-2, 2))
                base_rain = row['rain_probability']
                rain_prob = max(0, min(100, base_rain + random.uniform(-10, 10)))
                base_humidity = row['humidity']
                humidity = max(20, min(100, base_humidity + random.uniform(-10, 10)))
                base_cloud = row['cloud_cover']
                cloud_cover = max(0, min(100, base_cloud + random.uniform(-15, 15)))
            # Determine weather icon
            if rain_prob > 60:
                icon = '🌧️'
            elif rain_prob > 30:
                icon = '🌦️'
            elif cloud_cover > 70:
                icon = '☁️'
            elif cloud_cover > 40:
                icon = '⛅'
            else:
                icon = '☀️'
            weather_forecast.append({
                'temp': round(temp, 1),
                'humidity': round(humidity, 0),
                'wind': round(wind, 1),
                'rain_prob': round(rain_prob, 0),
                'cloud_cover': round(cloud_cover, 0),
                'icon': icon
            })
        conn.close()
        return weather_forecast
    except Exception as e:
        print(f"Error generating weather forecast: {e}")
        return [
            {'temp': 70, 'humidity': 50, 'wind': 10, 'rain_prob': 20, 'cloud_cover': 30, 'icon': '☀️'},
            {'temp': 68, 'humidity': 55, 'wind': 12, 'rain_prob': 25, 'cloud_cover': 40, 'icon': '⛅'},
            {'temp': 65, 'humidity': 75, 'wind': 15, 'rain_prob': 60, 'cloud_cover': 80, 'icon': '🌧️'},
            {'temp': 72, 'humidity': 50, 'wind': 10, 'rain_prob': 15, 'cloud_cover': 25, 'icon': '☀️'}
        ]



if __name__ == '__main__':
    app.run(debug=True) 