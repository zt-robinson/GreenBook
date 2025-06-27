# GreenBook

**GreenBook** is a Flask-based web application that simulates an entire professional golf tour – complete with tournaments, players, stats, and leaderboards – and lets you experience the thrill of betting on the outcomes **using fake money on fake events**. In other words, it’s like fantasy sports betting meets a golf simulator. All events and currency are simulated, so *no real money is involved* – it’s just for fun and practice in a data-rich golf universe.

This project draws inspiration from the prestige and classic style of Augusta National, featuring a classy green-and-gold theme and a focus on detailed stats presented in a country club aesthetic. Our goal is to mirror the drama, structure, and excitement of a real PGA Tour season (from weekly tournaments to player career progression), while providing a **safe sandbox for sports betting** enthusiasts to test their instincts with play money.

## Current Features

Even at this early stage, **GreenBook** already boasts an impressive range of features and content:

* **Fictional Pro Players:** Over 200 unique virtual golfers are generated, each with realistic skill ratings, nationalities, ages, and career stats. This diverse player database forms the backbone of the simulation, ensuring every tournament has a competitive field with varied talent.

* **Career & Tour Card System:** Each player carries a PGA Tour–like status (`TourCardStatus`) that gets updated based on their performance. For example, the top players retain full tour cards, lower-ranked players might have conditional status, and those who lose their status are sent to a *developmental tour* to play their way back onto the main tour. This means the league is dynamic – at season’s end, the bottom-ranked pros drop to the dev league, while the dev league’s top performers get promoted, mimicking real-life promotion and relegation.

* **Extensive Course Library:** The app includes 30+ championship golf courses, each modeled with detailed attributes like yardage, par, typical weather, green speed, elevation, etc.. These varied course profiles add realism and ensure that tournaments feel different week to week (a links course by the coast will play differently than a tight tree-lined course, for example).

* **Season Schedule & Tournaments:** GreenBook comes with a full season schedule of tournaments, including majors, invitationals, and open events. Each tournament has an appropriate field size and entry criteria to mirror the real tour (e.g. invitationals have smaller fields, majors allow certain qualifiers, etc.). Events are structured as authentic 72-hole competitions (four rounds of stroke play) with a **cut** after round 2 (only the top 65 or so make the cut, similar to real golf). Each event also has a set purse (prize money) and a points distribution, so players are competing for both winnings and ranking points throughout the season.

* **Modern Augusta-Inspired UI:** The user interface sports a classy dark-green, gold, and off-white color scheme with classic serif typography – a nod to Augusta National’s timeless look. The layout uses flat, stately design elements (think of a digital scorecard at an exclusive country club) to present information in a visually pleasing way. The result is a modern web app that feels both premium and welcoming.

* **Responsive Design:** GreenBook is built to be accessible on various devices and screen sizes. The design includes flexible multi-column layouts and compact, balanced tables so that pages remain readable and attractive whether you’re on a large desktop monitor or a mobile phone. Key information (like leaderboards or player stats) is displayed in a clear, concise format without overwhelming the user.

* **Full Web App Experience:** The application includes multiple pages to explore all aspects of the simulated tour:

  * **Home Page:** A friendly landing page with a welcome message and some quick stats/summary of the current season.
  * **Players Page:** A searchable table listing all the players. You can expand a player’s entry to see detailed stats and career info (wins, rankings, etc.), giving you a deep look at each golfer in the universe.
  * **Courses Page:** A list of all courses in the game, each expandable to show a professional scorecard and the course’s real-world characteristics. It’s great for scouting the week’s venue and understanding its challenges (length, difficulty, typical conditions, etc.).
  * **Schedule Page:** A chronological list of all upcoming (and past) tournaments with key details like the start date, event type, location, field size, purse, and round timing (all events are scheduled in Eastern Time). This lets you see what’s coming up on the tour and results of completed events.
  * All these pages are tied together with a clean navigation bar at the top of the app, making it easy to jump between the home, players, courses, and schedule sections. Overall, the web interface is designed to be intuitive so users can browse the rich data without feeling lost.

*(Under the hood, GreenBook uses a Flask backend with SQLite databases to store all this data – players, courses, tournaments, etc. – and Jinja2 templates to render the pages. Utility scripts in the `scripts/` folder help generate or reset data as needed. This technical foundation ensures the app runs smoothly and can be expanded over time.)*

## Planned Features

GreenBook is an ambitious project, and there’s a lot more in store. Here’s a look at what’s on the roadmap – both in the near term and farther down the line:

### Short-Term Plans (Next Steps)

* **Live Tournament Simulation:** Implementing the real-time simulation engine is a top priority. This will allow tournaments to play out shot-by-shot (or hole-by-hole) in a group-by-group fashion, rather than deciding results instantly. Along with this, we plan to add automated tournament field generation logic so that each event’s player field is selected according to the qualification rules (tour status, recent performance, etc.). In short, you’ll be able to watch a virtual tournament unfold in real time, with pairings and tee times just like on TV.

* **Dynamic Odds & Betting Interface:** Since betting is the cornerstone of GreenBook, we’re working on a comprehensive betting system. This will include a full **betting UI** where users can place a variety of wager types – outright winners, top-5/10/20 finishes, make/miss the cut, head-to-head matchups, round leaders, even fun props like “bogey-free round” or over/under on birdies. Odds for these bets will update live as the tournament progresses (after each hole, and between rounds) based on the unfolding results. We’ll implement realistic odds calculation factors (player skill, current form, course difficulty, etc.) so that the odds react in a believable way to on-course action. All betting will use **play money** (an in-app virtual currency), and the system will track your bets, show potential payouts, and settle wagers once results are in. The end result: you can sweat the tournament as both a fan and a **(virtual) bettor**, without risking a dime of real money.

* **Enhanced Player Profiles & Stats:** We plan to introduce a dedicated player profile page or dialog that goes deeper into each golfer’s career. This could include a full season log, career earnings, win count, performance in majors, and other advanced stats or charts. Essentially, you’ll be able to drill down into how a player’s season is going or see their all-time accomplishments, adding more depth for those who love stats. (This feature will complement the current Players page by providing more historical context and interesting trivia for each golfer.)

* **Development Tour Simulation:** The “dev tour” (developmental tour) will be more fully simulated. Right now, we have the concept of a secondary tour where relegated players go; upcoming improvements will simulate an entire season for that dev tour as well. We’ll track which players are dominating the lower circuit and ensure that at season’s end, the top X players from the dev league earn (or *re*-earn) their Tour cards for the next year. This will keep the world of GreenBook dynamic, with fresh talent coming in and underperforming players having to fight their way back – just like the real Korn Ferry Tour feeding into the PGA Tour.

### Long-Term Plans (Future Ideas)

* **Season-Ending Championship & Playoffs:** Introduce a FedExCup-style playoff system or a Tour Championship event at the end of the season. This could mean a special points race throughout the year leading to a final event with only the top qualifiers, maybe even with staggered starting scores or other twists to mirror how the real Tour does its Championship. The goal is to have a dramatic season finale to crown the year’s champion.

* **Player Form, Injuries, and Morale:** To increase realism, we want to add factors like player injuries, fatigue, and hot/cold streaks. For example, a golfer might have a form rating that affects their performance (someone “in form” plays above their usual skill level, while a slump or a minor injury might hurt a player’s stats temporarily). This would add another layer of depth – you might think twice about betting on a star player who’s dealing with a virtual wrist injury or who has missed three cuts in a row.

* **Sponsorships & Pressure Mechanics:** This is a bit experimental, but we’d love to simulate the off-course aspects of pro golf too. This could include sponsorship deals (imaginary endorsements that players earn with success) and pressure scenarios (e.g. a player going for a milestone or trying to keep their card might “feel the pressure” in the sim). These factors could subtly influence performance and make the narrative more engaging – for instance, a rookie with a big sponsor contract might choke in a high-stakes moment, or a veteran might find an extra gear knowing a record is on the line.

* **User Accounts & Persistent Profiles:** Currently, GreenBook is a single-player experience. In the future, we plan to add user accounts/logins so that multiple people can use the app and keep their own *virtual bankrolls* and betting history. This way, you can track how your fake-money betting performance changes over time, and perhaps even have friendly competitions with other users (e.g. leaderboards for best bettors, longest streak of winning bets, etc.). Persistent accounts also open the door to things like achievements or saved preferences.

* **Admin Tools & Editing:** As the simulation grows, we’ll need internal tools to manage it. We plan to build an admin interface for the maintainers (and power users) to easily add or edit content – for example, creating a new tournament, editing a course’s data, or tweaking a player’s profile. This would make it easier to update the app without diving directly into the database or code, and could even allow community contributions like custom tournaments or user-created courses down the road.

* **Public API & Integrations:** Down the line, we envision providing an API so that external applications or services can tap into GreenBook’s data. Imagine a Discord bot that posts updates on tournament leaders, or a mobile companion app that lets you place bets from your phone – with a robust API, these kinds of integrations become possible. This could make the GreenBook ecosystem more open and interactive.

* **More Betting Markets & Analytics:** We’ll continuously expand the betting aspect with new markets and better stats. This might include advanced prop bets, detailed analytics pages (for the real data nerds), live probability graphs during tournaments, etc.. The aim is to keep the experience fresh and engaging, offering both casual fun bets and deep analytical content for those who want to dive in. We want GreenBook to scratch the itch for both sports bettors and golf fans who love stats.

As development progresses, this roadmap may evolve. We’re prioritizing core simulation and betting features first, then moving into these enhancements to enrich the experience even further.

## Getting Started

Ready to try out GreenBook? Here’s how you can get it up and running on your local machine:

1. **Clone the repository.** In a terminal, run:

   ```bash
   git clone https://github.com/zt-robinson/GreenBook.git  
   cd GreenBook
   ```

   This will download the project to a folder named `GreenBook` and navigate into it.

2. **Create a virtual environment (recommended).**
   Make sure you have Python 3 installed, then set up a venv and activate it:

   ```bash
   python3 -m venv venv  
   source venv/bin/activate
   ```

   This will isolate the project’s Python dependencies from your system.

3. **Install dependencies.**
   With your virtual environment active, install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

   This will download and install Flask and any other libraries the app needs.

4. **Set up the database.**
   The repo comes with some pre-generated data in the `data/` directory (SQLite databases for players, courses, etc.). If you want to reset or regenerate data, you can use the scripts in the `scripts/` folder. For example:

   ```bash
   python scripts/create_player.py    # regenerate the players database  
   python scripts/create_course.py   # regenerate the courses database
   ```

   Running these will refresh the data with new random players or courses. (This step is optional since the repository likely includes an initial dataset. You can skip it if you just want to use the default data.)

5. **Run the application.**
   Start the Flask development server by running:

   ```bash
   flask run
   ```

   *(Make sure your virtual env is activated, and you’re in the project directory. Alternatively, you can do `python app.py` to run the app.)*

6. **Open the app in your browser.**
   Once the server is running, go to [http://localhost:5000](http://localhost:5000) in your web browser. You should see the GreenBook web app’s home page. From there, you can navigate to the Players, Courses, and Schedule pages using the top menu, and get started exploring the GreenBook world!

*(Note: GreenBook is currently in development, so some features described above may be in-progress. The interface is live, but the actual tournament simulation might be stubbed or running in a simplified way until the full logic is implemented. Feel free to play around with the data and interface.)*

## Contributing

This project is a work in progress and **open to ideas**! If you have suggestions for improvement, encounter a bug, or want to contribute in any way, please don’t hesitate to reach out. The best way to contribute is to open an issue on GitHub to discuss your idea, or directly create a pull request with your changes. Whether it’s adding new features, tweaking the simulation, or improving the UI, any help is welcome. We just ask that you maintain the spirit of the project – making it fun, accessible, and realistic for users.

*Stay tuned for updates by watching the repo. As GreenBook evolves, we’d love to have a community of golf and coding enthusiasts involved!* 👥⛳

## License

GreenBook is an open-source project, released under the **MIT License**. This means you’re free to use, modify, and distribute the code, as long as you include the original license notice. (See the `LICENSE` file for the full text of the license.) Enjoy!
