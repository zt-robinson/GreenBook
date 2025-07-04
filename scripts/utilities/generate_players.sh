#!/bin/bash

# A script to generate a specified number of players non-interactively.
# Usage: ./generate_players.sh [number_of_players]
# Example: ./generate_players.sh 150

# Default to 10 players if no number is provided
COUNT=${1:-10}

# Activate virtual environment if it exists
if [ -d "venv" ]; then
  source venv/bin/activate
  echo "Virtual environment activated."
fi

echo "Generating $COUNT players..."

for i in $(seq 1 $COUNT); do
  echo "----------------------------------------"
  echo "Creating player $i of $COUNT..."
  # Pipe 'y' to the python script to automatically confirm saving the player
  echo "y" | python3 create_player.py
done

echo "----------------------------------------"
echo "✅ Done. $COUNT players created." 