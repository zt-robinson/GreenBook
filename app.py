from flask import Flask, render_template, redirect, url_for, request
import sqlite3
import os
from datetime import datetime, timedelta
import sys
sys.path.append(os.path.dirname(__file__))
from scripts.generate_tournament_field import get_tournament_field

app = Flask(__name__)

PLAYER_DB_PATH = os.path.join(os.path.dirname(__file__), 'data/golf_players.db')
COURSE_DB_PATH = os.path.join(os.path.dirname(__file__), 'data/golf_courses.db')
print('DEBUG: PLAYER_DB_PATH is', PLAYER_DB_PATH)
print('DEBUG: COURSE_DB_PATH is', COURSE_DB_PATH)

# In-memory simulation state (for demo; will move to persistent storage later)
sim_state = {}

def get_all_players():
    conn = sqlite3.connect(PLAYER_DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM players ORDER BY name ASC')
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

@app.route('/players')
def players():
    players = get_all_players()
    players = [dict(player) for player in players]  # Convert to dicts for mutability
    # Add the new public fields to each player
    for player in players:
        player['tour_rank'] = 0
        player['events'] = 0  # Will be calculated from tournament participation later
        player['tour_championship_points'] = 0
        player['points_behind_lead'] = 0
        player['wins'] = player.get('career_wins', 0)  # Use existing career_wins for now
        player['top_10s'] = 0  # Will be calculated from tournament results later
        player['world_rank'] = 0  # Set all world ranks to 0 for now
    return render_template('players.html', players=players, country_to_flag_iso=country_to_flag_iso)

@app.route('/courses')
def courses():
    conn = sqlite3.connect(COURSE_DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('''
        SELECT c.id, c.name, c.location, c.total_yardage as yardage, c.total_par as par, c.prestige_level as prestige, c.est_year,
               cc.avg_temperature, cc.humidity_level, cc.wind_factor, cc.rain_probability,
               cc.green_speed, cc.hazard_density, cc.rough_length, cc.narrowness_factor,
               cc.elevation_factor
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
        course['slope_rating'] = 120 + int(course['prestige'] * 10) if course['prestige'] else 120
        course['course_rating'] = 70.0 + (course['prestige'] * 0.5) if course['prestige'] else 70.0
        # User-facing conversions
        course['display_temp'] = f"{int(round(course.get('avg_temperature', 0)))}°F"
        course['display_humidity'] = f"{int(round((course.get('humidity_level') or 0) * 100))}%"
        # Elevation: 0.0 = 0 ft, 1.0 = 7724 ft
        elevation_factor = course.get('elevation_factor') or 0
        course['display_elevation'] = f"{int(elevation_factor * 7724)} ft"
        # Print Colorado course elevation for review
        if 'Colorado' in (course.get('location') or '') or 'CO' in (course.get('location') or ''):
            print(f"DEBUG: {course['name']} (Colorado) elevation_factor={elevation_factor}, elevation={int(elevation_factor * 7724)} ft")
        # Rough length: 2 to 4.5 inches
        rough_length = course.get('rough_length') or 0.2
        course['display_rough'] = f"{round(2 + (rough_length - 0.2) / 0.7 * 2.5, 1)} in"
        # Green speed: 10.5 to 13.5 ft
        green_speed = course.get('green_speed') or 0.3
        course['display_stimp'] = f"{round(10.5 + (green_speed - 0.3) / 0.7 * 3, 1)} ft"
        # Rain days: 20 to 180
        rain_prob = course.get('rain_probability') or 0.05
        course['display_rain_days'] = f"{int(20 + (rain_prob - 0.05) / 0.55 * 160)} days/year"
        # Wind speed: 5 to 20 mph
        wind_factor = course.get('wind_factor') or 0.2
        course['display_wind'] = f"{round(5 + (wind_factor - 0.2) / 0.3 * 15, 1)} mph"
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

    # Fetch tournaments and schedule
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
        try:
            dt = datetime.strptime(t['start_date'], '%Y-%m-%d')
            t['start_date_formatted'] = dt.strftime('%B %-d, %Y')
        except Exception:
            t['start_date_formatted'] = t['start_date']
        # Format round times
        t['round_1_start_fmt'] = format_ampm(t['round_1_start'])
        t['round_2_start_fmt'] = format_ampm(t['round_2_start'])
        t['round_3_start_fmt'] = format_ampm(t['round_3_start'])
        t['round_4_start_fmt'] = format_ampm(t['round_4_start'])

    return render_template('schedule.html', tournaments=tournaments)

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
    
    # Map tournament_type to user-friendly string
    type_map = {
        'regular': 'Standard Tour Event',
        'open': 'Open Tournament',
        'invitational': 'Invitational Tournament',
        'major': 'Major Championship',
    }
    tournament['type_display'] = type_map.get(tournament['tournament_type'], tournament['tournament_type'].title())
    
    # Format dates and times
    try:
        dt = datetime.strptime(tournament['start_date'], '%Y-%m-%d')
        tournament['start_date_formatted'] = dt.strftime('%B %-d, %Y')
    except Exception:
        tournament['start_date_formatted'] = tournament['start_date']

    # Compute timezone-aware ISO string for Boston (America/New_York)
    try:
        from datetime import datetime
        try:
            from zoneinfo import ZoneInfo  # Python 3.9+
            ny_tz = ZoneInfo('America/New_York')
            dt_naive = datetime.strptime(tournament['start_date'] + ' ' + tournament['round_1_start'], '%Y-%m-%d %H:%M')
            dt_ny = dt_naive.replace(tzinfo=ny_tz)
        except ImportError:
            import pytz
            ny_tz = pytz.timezone('America/New_York')
            dt_naive = datetime.strptime(tournament['start_date'] + ' ' + tournament['round_1_start'], '%Y-%m-%d %H:%M')
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
    
    # Get course name
    cconn = sqlite3.connect(courses_db_path)
    cconn.row_factory = sqlite3.Row
    ccur = cconn.cursor()
    ccur.execute('SELECT name FROM courses WHERE id = ?', (tournament['course_id'],))
    course = ccur.fetchone()
    tournament['course_name'] = course['name'] if course else 'Unknown'
    cconn.close()
    
    # PHASE LOGIC: Provisional vs Finalized
    today = datetime.now().date()
    start_date = datetime.strptime(tournament['start_date'], '%Y-%m-%d').date()
    days_until_start = (start_date - today).days
    show_provisional = days_until_start > 1
    provisional_qualifiers = []
    if show_provisional:
        # Get all players who would currently qualify (simulate field logic)
        all_players = get_all_players()
        # Sort all players alphabetically by last name (case-insensitive)
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
    # Get winner's tour points from payout_structure
    tconn = sqlite3.connect(tournaments_db_path)
    tconn.row_factory = sqlite3.Row
    tcur = tconn.cursor()
    tcur.execute('SELECT tour_points FROM payout_structure WHERE tournament_id = ? AND finish_position = 1', (tournament_id,))
    row = tcur.fetchone()
    winner_points = row['tour_points'] if row else 0
    tconn.close()
    cut_line = 'Top 65 plus ties'
    return render_template('tournament_detail.html', tournament=tournament, groups=sorted_groups if not show_provisional else [], provisional_qualifiers=provisional_qualifiers, qualifier_columns=qualifier_columns if show_provisional else None, country_to_flag_iso=country_to_flag_iso, winner_points=winner_points, cut_line=cut_line, show_provisional=show_provisional)

if __name__ == '__main__':
    app.run(debug=True) 