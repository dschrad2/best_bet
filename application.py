import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from cs50 import SQL
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd, comma

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd
app.jinja_env.filters["comma"] = comma

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure Library to use SQLite database
db = SQL("sqlite:///best_bet.db")


@app.route("/")
@login_required
def index():
    """Show welcome screen and chips balance"""

    # Query database for user's chips total
    user_id = session["user_id"]
    rows = db.execute("SELECT username, chips FROM users WHERE id = ?", user_id)
    chips = rows[0]["chips"]
    username = rows[0]["username"]

    return render_template("index.html", chips=chips, username=username)


@app.route("/play", methods=["GET", "POST"])
@login_required
def play():
    """Play the Best Bet game"""

    # Query database for user's transaction history
    user_id = session["user_id"]
    rows = db.execute("SELECT username, chips FROM users WHERE id = ?", user_id)
    chips = rows[0]["chips"]
    username = rows[0]["username"]


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        bankroll = request.form.get("bankroll", type=int)

        if type(bankroll) == int and bankroll >= 10:

            # Update chip total in the users table
            chips += bankroll
            db.execute("UPDATE users SET chips = ? WHERE id = ?", chips, user_id)

            # Add a row to the high scores table signifying the score
            db.execute("INSERT INTO high_scores (user_id, username, chips_gained, time) VALUES (?, ?, ?, datetime('now'))",
                      user_id, username, bankroll)

            return redirect("/")

        else:
            return apology("Still in progress")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("play.html", chips=chips, username=username)


@app.route("/chips", methods=["GET", "POST"])
@login_required
def chips():
    """Buy extra chips for your stack"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        price = request.form.get("price", type=float)
        requested_chips = request.form.get("chips", type=int)

        # Ensure chip request was entered correctly
        if type(requested_chips) == int and requested_chips > 0:

            # Query database for user's chips total
            user_id = session["user_id"]
            rows = db.execute("SELECT chips FROM users WHERE id = ?", user_id)
            current_chips = rows[0]["chips"]


            # Add a row to the transactions table signifying the transaction
            db.execute("INSERT INTO transactions (user_id, amount, price, transacted) VALUES (?, ?, ?, datetime('now'))",
                      user_id, requested_chips, price)

            # Update users table to show new chip stack
            current_chips += requested_chips
            db.execute("UPDATE users SET chips = ? WHERE id = ?", current_chips, user_id)

            return redirect("/")

        else:
            return apology("Must enter a whole number greater than zero")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("chips.html")


@app.route("/history")
@login_required
def history():
    """Show chip purchases"""

    # Query database for user's transaction history
    user_id = session["user_id"]
    transactions = db.execute(
        "SELECT amount, price, transacted FROM transactions WHERE user_id = ? ORDER BY transacted", user_id)

    return render_template("history.html", transactions=transactions)


@app.route("/rules")
@login_required
def rules():
    """Show rules"""

    return render_template("rules.html")


@app.route("/scores")
@login_required
def scores():
    """Show single-game and all-time high scores"""

    # Query database for single-game high scores
    scores = db.execute("SELECT username, chips_gained, time FROM high_scores ORDER BY chips_gained DESC LIMIT 10")

    # Query database for chips totals
    chips = db.execute("SELECT username, chips FROM users ORDER BY chips DESC LIMIT 10")

    return render_template("scores.html", scores=scores, chips=chips)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

    return apology("Still in progress")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("Username required")

        # Ensure password was submitted
        elif not password:
            return apology("Password required")

        # Ensure password was re-entered
        elif not confirmation:
            return apology("Must re-enter password")

        # Ensure password matches confirmation
        elif password != confirmation:
            return apology("Passwords must match")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username does not exist
        if len(rows) != 0:
            return apology("Username already exists")

        # Generate password hash
        password_hash = generate_password_hash(password)

        # Insert username and password into the users table
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, password_hash)

        # Automatically log user into the site
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("Something went wrong logging you in.")

        # Automatically log in the user
        session["user_id"] = rows[0]["id"]

        # Send the user back to the main page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/password", methods=["GET", "POST"])
def password():
    """Change user password"""

    if request.method == "POST":

        current = request.form.get("current")
        new = request.form.get("new")
        confirmation = request.form.get("confirmation")

        # Ensure current password was submitted
        if not current:
            return apology("Current password required")

        # Ensure new password was submitted
        elif not new:
            return apology("New password required")

        # Ensure new password was re-entered
        elif not confirmation:
            return apology("Must re-enter new password")

        # Ensure new password matches confirmation
        elif new != confirmation:
            return apology("New and re-entered password must match")

        # Check current user
        user_id = session["user_id"]
        rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)

        # Ensure user is unique
        if len(rows) != 1:
            return apology("Something went wrong identifying record")

        # Ensure current password is correct
        if not check_password_hash(rows[0]["hash"], current):
            return apology("Current password does not match password on record")

        # Generate password hash
        password_hash = generate_password_hash(new)

        # Update record with new password
        db.execute("UPDATE users SET hash = ? WHERE id = ?", password_hash, user_id)

        # Double-check that new password has been added to record
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)

        # Ensure username is only record and new password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], new):
            return apology("Something went wrong verifying new password")

        # Send the user back to the main page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("password.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)