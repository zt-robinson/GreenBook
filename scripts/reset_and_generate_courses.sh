#!/bin/bash

set -e

DB="golf_players.db"

cd "$(dirname "$0")"

# Delete all courses and related data
echo "Deleting all courses, course_characteristics, and holes..."
sqlite3 "$DB" "DELETE FROM courses;"
sqlite3 "$DB" "DELETE FROM course_characteristics;"
sqlite3 "$DB" "DELETE FROM holes;"
echo "Database cleared."

echo "Generating 20 new courses with unique locations..."

# Use Python to shuffle and print 20 unique locations (repeat if needed)
LOCATIONS=$(python3 <<EOF
import random
locations = [
    ('Dallas', 'Texas', 'USA'),
    ('Los Angeles', 'California', 'USA'),
    ('Chicago', 'Illinois', 'USA'),
    ('Miami', 'Florida', 'USA'),
    ('Boston', 'Massachusetts', 'USA'),
    ('London', 'England', 'UK'),
    ('Edinburgh', 'Scotland', 'UK'),
    ('Dublin', 'Ireland', 'Ireland'),
    ('Toronto', 'Ontario', 'Canada'),
    ('Vancouver', 'British Columbia', 'Canada'),
    ('Sydney', 'New South Wales', 'Australia'),
    ('Melbourne', 'Victoria', 'Australia'),
    ('Tokyo', 'Tokyo', 'Japan'),
    ('Osaka', 'Osaka', 'Japan'),
    ('Paris', 'Île-de-France', 'France'),
    ('Madrid', 'Madrid', 'Spain'),
    ('Barcelona', 'Catalonia', 'Spain'),
    ('Valencia', 'Valencia', 'Spain'),
    ('Seville', 'Andalusia', 'Spain'),
    ('Zaragoza', 'Aragon', 'Spain'),
    ('Malaga', 'Andalusia', 'Spain'),
    ('Murcia', 'Murcia', 'Spain'),
    ('Palma de Mallorca', 'Balearic Islands', 'Spain'),
    ('Las Palmas de Gran Canaria', 'Canary Islands', 'Spain'),
    ('Bilbao', 'Basque Country', 'Spain'),
    ('Alicante', 'Valencia', 'Spain'),
    ('Cordoba', 'Andalusia', 'Spain'),
    ('Valladolid', 'Castile and Leon', 'Spain'),
    ('Vigo', 'Galicia', 'Spain'),
    ('Gijon', 'Asturias', 'Spain'),
    ('Marseille', "Provence-Alpes-Côte d'Azur", "France"),
    ('Belfast', 'Northern Ireland', 'UK'),
    ('Glasgow', 'Scotland', 'UK'),
    ('Liverpool', 'England', 'UK'),
    ('Manchester', 'England', 'UK'),
    ('Birmingham', 'England', 'UK'),
    ('Cork', 'Munster', 'Ireland'),
    ('Galway', 'Connacht', 'Ireland'),
    ('Perth', 'Western Australia', 'Australia'),
    ('Brisbane', 'Queensland', 'Australia'),
    ('Ottawa', 'Ontario', 'Canada'),
    ('Montreal', 'Quebec', 'Canada'),
    ('Calgary', 'Alberta', 'Canada'),
]
random.shuffle(locations)
while len(locations) < 20:
    locations += locations
for loc in locations[:20]:
    print('|'.join([str(x) for x in loc]))
EOF
)

COUNT=1
echo "$LOCATIONS" | while IFS='|' read -r CITY STATE COUNTRY; do
    echo "--- Generating course $COUNT: $CITY, $STATE, $COUNTRY ---"
    python3 create_course.py --city "$CITY" --state "$STATE" --country "$COUNTRY"
    echo "---------------------------"
    COUNT=$((COUNT+1))
done

echo "\nDone! 20 new courses generated."
echo "Current courses in the database:"
sqlite3 "$DB" "SELECT id, name, location FROM courses;" 