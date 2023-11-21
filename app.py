import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///final-project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def income():
    """Get income"""
    if request.method == "POST":

        # Add the user's entry into the database
        # Access form data
        date = request.form.get("date")
        category = request.form.get("category")
        amount = int(request.form.get("amount"))

        # Insert data into database
        user_id = session["user_id"]
        db.execute("INSERT INTO incomes (user_id, date, category, amount) VALUES(?, ?, ?, ?)", user_id, date, category, amount)

        # Go back to homepage
        return redirect("/")

    else:
        # Query database for user's all incomes
        user_id = session["user_id"]
        incomes_db = db.execute("SELECT * FROM incomes WHERE user_id = :id", id=user_id)

        #Render incomes page
        return render_template("income.html", incomes=incomes_db)


@app.route("/expense", methods=["GET", "POST"])
@login_required
def expense():
    """Get expense"""
    if request.method == "POST":

        # Add the user's entry into the database
        # Access form data
        date = request.form.get("date")
        category = request.form.get("category")
        amount = int(request.form.get("amount"))

        # Insert data into database
        user_id = session["user_id"]
        db.execute("INSERT INTO expenses (user_id, date, category, amount) VALUES(?, ?, ?, ?)", user_id, date, category, amount)

        expenses_db = db.execute("SELECT * FROM expenses WHERE user_id = :id", id=user_id)

         #Render expenses page
        return render_template("expense.html", expenses=expenses_db)

    else:
        # Query database for user's all expenses, orderd by most recent first
        user_id = session["user_id"]
        expenses_db = db.execute("SELECT * FROM expenses WHERE user_id = :id", id=user_id)

        return render_template("expense.html", expenses=expenses_db)


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
    if request.method == "GET":
        return render_template("register.html")

    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        if not password:
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        if not confirmation:
            return apology("must confirm password", 400)

        # Ensure password and confirmation match
        if password != confirmation:
            return apology("password do not match", 400)

        hash = generate_password_hash(password)

        try:
            # Insert new user into database
            new_user = db.execute(
                "INSERT INTO users (username, hash) VALUES(?, ?)", username, hash
            )
        except:
            # Ensure username does not already exist
            return apology("username already exists", 400)

        # Remember which user has logged in
        session["user_id"] = new_user

        # Redirect user to home page
        return redirect("/")




