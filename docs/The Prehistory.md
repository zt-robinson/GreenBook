## The Prehistory

The qualifying process for the events on the Tour is largely based on historical performance by players. However, because this Tour is being started from scratch, there is no historical performance to consider. As such, it is necessary that we create a "prehistory" of the Tour, which will be used to determine the initial ranking of players and priority lists for events. This will take the form of the following:

1. Create a database of 600 players using the player generation script that gives them specific stats and characteristics. 
    - The logic here can be borrowed by the script that is inside greenbook/scripts/players/generate_complete_player.py. All players that are generated during this entire process will be generated with a random age between 19 and 22.
    - I want all players to be generated with the physical and mental attributes that the script assigns, with the exception of the "peaking" logic that is in the script. The goal is that we will have a pool of 600 players that all have traits that can be used (along with randomizations and vollatility modifiers) to determine their performance in a given tournament.
2. Generate a single season of ten 600-player field tournaments, all of which consisting of 72 holes, with no cut lines, for all 600 players to play in. We'll refer to this as the "Gauntlet Season".
3. Run each tournament in the Gauntlet, and record the results.    
    - For each player, I want you to find some way to combine their physical and mental attributes into a value that is compared to a randomly assigned difficulty rating for each hole; so for all 72 holes of every single tournament, each player will have a "performance" on the hole that determines their score for that hole. Do not worry about trying to mess with par values or anything; just use the performance value to determine the score for each hole.
    - Once a tournament is complete, the players will be ranked based on their total score for the tournament (the better the score, the higher the rank), and will be awarded points for that tournament; first place gets 600 points, second place gets 599 points, etc. There will be a persistent leaderboard that is updated after each tournament during the year of the Gauntlet, which will collect and aggregate each players points after each tournament, and after ten events, the final Gauntlet season scoreboard of all 600 players will show the ranked players based on their total points earned over the season.
4. At the end of the season, the player list will be culled.
    - The bottom 500-ranked players will be deleted from the database, leaving 100 players.
    - These 100 players will have their age increased by one year. Their stats and attributes will not be affected in any way.
    - The script will then generate 50 new players using the same logic as step 1, and add them to the database. As in the logic in that step 1, these players will all be aged 19 and 22. These new players will have their names edited to include "S1" at the end, to indicate the first season they were brought up to compete in (which is the first season after the Gauntlet Season).
    - Once the new players are added to the database and there are 150 players, the Guantlet is over.

At this point, using the 150 players who made it out of the Gauntlet, we will now prepare to have ten 35-event seasons generated, using the following logic:

5. Generate a full season of 35 events encompassing a Continental Championship, Sovereign Tournament, AGA Championship, American Open, Royal Open, 8 signature events, 7 standard invitationals, and 15 standard events. the events will be created in the following order, and labeled as such:

| Event # | Event Type | Event Name | Notes |
|---------|------------|------------|-------|
| 01 | Signature Event #1 | | |
| 02 | Standard Event #1 | | |
| 03 | Standard Event #2 | | |
| 04 | Standard Invitational #1 | | |
| 05 | Standard Event #3 | | |
| 06 | Standard Invitational #2 | | |
| 07 | Standard Event #4 | | |
| 08 | Standard Event #5 | | |
| 09 | Signature Event #2 | | |
| 10 | Continental Championship | | |
| 11 | Standard Event #6 | | |
| 12 | Standard Invitational #3 | | |
| 13 | Signature Event #3 | | |
| 14 | Standard Event #7 | | |
| 15 | Sovereign Tournament | First Major | |
| 16 | Standard Event #8 | | |
| 17 | Standard Event #9 | | |
| 18 | Standard Invitational #4 | | |
| 19 | Signature Event #4 | | |
| 20 | AGA Championship | Second Major | |
| 21 | Standard Event #10 | | |
| 22 | Signature Event #5 | | |
| 23 | Standard Invitational #5 | | |
| 24 | Standard Event #11 | | |
| 25 | Standard Event #12 | | |
| 26 | American Open | Third Major | |
| 27 | Signature Event #6 | | |
| 28 | Standard Event #13 | | |
| 29 | Standard Event #14 | | |
| 30 | Standard Invitational #6 | | |
| 31 | Royal Open | Fourth Major | |
| 32 | Standard Event #15 | | |
| 33 | Standard Invitational #7 | | |
| 34 | Standard Event #16 | | |
| 35 | Signature Event #7 | | |

Similar to the Gauntlet Season, each of these events will consist of a single round of 72 holes, and the 150 players will be scored using the same logic as the Gauntlet Season, and will be awarded points based on their place in the final standings; for example, first place gets 150 points, second gets 149, and so on. After every event in a given season, a database will be updated for that season that allows us to track that event, the season of that event, and the full leaderboard of that event.
6. The season will follow this simulation logic event by event. At the conclusion of the season, we will have a final season leaderboard that ranks all 150 players based on their total points earned over the season.
7. The players database will be culled, using the exact same logic as step 4 above.
- The bottom 50-ranked players will be deleted from the database, leaving 100 players.
- These 100 players will have their age increased by one year. Their stats and attributes will not be affected in any way.
- The script will then generate 50 new players using the same logic as step 1 above, and add them to the database. As in the logic in that step 1, these players will all be aged 19 and 22. These new players will have their names edited to include "S[X]" at the end, where "X" represents the number of the season following the current one, to indicate the first season they were brought up to compete in (which is the next season after the season that just finished simulating).
- Once the new players are added to the database and there are 150 players, the season is over.
8. Steps 5-7 will repeat 9 more times, resulting in a ten-year pseudo historical record of tournament results, which will be used to determine the initial ranking of players and be used to build out priority lists for events moving forward. 

After each season, I want you to generate a report that includes the following:
- The final season leaderboard
- A player-by-player breakdown of each player indicating their points earned in each event, their total points earned for the season, and their rank for the season.
- The final database of players, with their names and stats
