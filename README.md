# Best Bet!
#### Video Demo:  <https://youtu.be/uX-53aBmiII>
#### Description:
This project is a betting trivia game webapp that allows users to bet on their answers to trivia questions in order to rack up a high score.

The game is a single-player version of a multiplayer game I helped refine with a friend, with whom I used to play with other friends.
The goal of Best Bet! is to get as many chips as possible by answering 8 questions, and betting as much as possible on each answer
in which you're confident without losing chips on answers you get wrong.

Players start with 100 chips in the game, and for each question, the player must bet at least 10 chips and up to all of their chips. If they
get the question correct, they double their bet. For instance, if a player has a stack of 100 chips, and they bet 50 of their chips and get it right,
they win 100 chips to add to their stack of 100, for 200 total chips. Any wrong answers, and the player will lose all of their bet.

However, in order to keep the player in the game, any time a player loses all of their chips, they automatically receive 10 chips immediately to keep playing.
Their chip total will never fall below 10, and as a result they can still win a lot of chips even if they go big and lose early on.

The game is made up of the following non-display files:

requirements.txt - An overview of the Flask and CS50 libraries that were used to build up the game.
helpers.py - A helper Python file that creates a few useful functions, such as comma, which adds commas in the thousands place to present table data with more polish.
best_bet.db - A database consisting of three tables--users, which tracks each user and their chip total, transactions, which tracks all chip purchases made, and
high_scores, which as the name suggests tracks all of the chip winnings from each user's games in order from highest to lowest.
application.py - The home file which contains all of the Python and Flask functionality used to produce the web game.

The game includes the following html files:

scores.html - A file that displays a page showing the single-game high scores and total chip high scores among all players.
rules.html - A file that displays a page showing the rules of Best Bet!
register.html - A file that displays a page that allows users to register an account on the site (which is required in order to play).
play.html - A file that displays all of the components of the Best Bet! game itself, including questions, answers, descriptions, and clickable buttons, as well as chip scores.
password.html - A file that displays a page allowing users to change their passwords.
login.html - A file that displays a page allowing users to log into their accounts.
layout.html - A file that holds all of the boilerplate display content common to each page of the web game.
index.html - A file that displays the home page of the web game, including a brief description of the game and a table of the user's chip total.
history.html - A file that displays a page showing a history of all chip purchases a user has made from their account.
chips.html - A file that displays a page allowing the user to purchase additional chips for their stack.
apology.html - A file that displays a page of boilerplate language in the event of an error in the game.

The game also includes these design and scripting files:

styles.css - A style sheet for some of my design features, such as purple buttons, which I love.
script.js - A file that holds all of the Javascript used to make Best Bet! playable, as well as track chip totals within the game.
questions.js - A file that holds all of the questions and answers that show up randomly in Best Bet!