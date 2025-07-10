## The Prehistory

The qualifying process for the events on the Tour is largely based on historical performance by players. However, because this Tour is being started from scratch, there is no historical performance to consider. As such, it is necessary that we create a "prehistory" of the Tour, which will be used to determine the initial ranking of players and priority lists for events. This will take the form of the following:

1. Create a database of 600 players using the player generation script that gives them specific stats and characteristics.
2. Generate a season of ten, 600-player field tournaments, with no cut lines, for all 600 players to play in. 
    - First place gets 600 points, second place gets 599 points, etc.
    - At the end of the season, remove the bottom 450 players, leaving the the highest ranked 150 players.
3. Generate a full season of 35 events encompassing a Continental Championship, Sovereign Tournament, AGA Championship, American Open, Royal Open, 8 signature events, 7 standard invitationals, and 15 standard events. For pursposes of this script, each of these events will consist of only a single round, and the 150 players will be awarded points based on their place in the final standings; for example, first place gets 150 points, second gets 149, and so on.
4. The season will be simualted event by event, with players' stats and skill levels being utilized to determine their performance in each event (along with some randomization modifiers).
5. At the conclusion of the season, the bottom 50 players in terms of points earned will be removed from the database, and will be replaced with 50 new players generated using the player generation script. Each player will be aged up by 1 year, though their stats will not be affected. 
6. The script will generate a report with the final season standings, the winners of each event, the players that were removed for being in the bottom 50, and the players that were added to the database.
7. Steps 3-6 will repeat 9 times, resulting in a ten-year pseudo historical record of tournament results, which will be used to determine the initial ranking of players and be used to build out priority lists for events moving forward. All intermediate reports as well as the final report will be saved to a markdown file that is saved in a new /records directory. 

