import os
import bcrypt
import mysql.connector
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-change-me")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


def connect(db):
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=db,
    )


def library_db():
    return os.getenv("DB_NAME", "library")


def auth_db():
    return os.getenv("AUTH_DB_NAME", "registration")


def run(sql, params=(), db=None):
    conn = connect(db or library_db())
    cur = conn.cursor()
    cur.execute(sql, params)
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return cols, rows


def insert(sql, params, db):
    conn = connect(db)
    cur = conn.cursor()
    try:
        cur.execute(sql, params)
        conn.commit()
        return cur.lastrowid
    finally:
        cur.close()
        conn.close()


def section(heading, sql, params=()):
    cols, rows = run(sql, params)
    return {"heading": heading, "cols": cols, "rows": rows}


def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8")[:72], bcrypt.gensalt()).decode("utf-8")


def check_password(password, stored):
    try:
        return bcrypt.checkpw(password.encode("utf-8")[:72], stored.encode("utf-8"))
    except ValueError:
        return False


@app.before_request
def require_login():
    if request.endpoint in (None, "login", "register", "static"):
        return None
    if "user_id" not in session:
        return redirect(url_for("login"))
    return None


@app.errorhandler(mysql.connector.Error)
def db_error(e):
    return render_template(
        "page.html",
        title="Database error",
        sections=[],
        error="Could not talk to MySQL. Check your .env file and that the server is running.",
    ), 500


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("index"))
    errors = []
    name = ""
    email = ""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        if not name:
            errors.append("Name is required")
        if not email:
            errors.append("Email is required")
        if not password:
            errors.append("Password is required")
        if not confirm:
            errors.append("Confirm password is required")
        if password and confirm and password != confirm:
            errors.append("Passwords do not match")
        if not errors:
            try:
                user_id = insert(
                    "INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s)",
                    (email, name, hash_password(password)),
                    auth_db(),
                )
            except mysql.connector.IntegrityError as e:
                if e.errno == 1062:
                    errors.append("Email Already Exists")
                else:
                    raise
            else:
                session.clear()
                session["user_id"] = user_id
                session["name"] = name
                return redirect(url_for("index"))
    return render_template("register.html", title="Register", errors=errors, name=name, email=email)


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("index"))
    errors = []
    email = ""
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        if not email:
            errors.append("Email is required")
        if not password:
            errors.append("Password is required")
        if not errors:
            rows = run(
                "SELECT user_id, name, password_hash FROM users WHERE email = %s",
                (email,),
                auth_db(),
            )[1]
            if rows and check_password(password, rows[0][2]):
                session.clear()
                session["user_id"] = rows[0][0]
                session["name"] = rows[0][1]
                return redirect(url_for("index"))
            errors.append("Invalid email or password")
    return render_template("login.html", title="Login", errors=errors, email=email)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
def index():
    return render_template("index.html", title="Library")


@app.route("/search")
def search():
    keyword = request.args.get("keyword", "").strip()
    min_price = request.args.get("min_price", "").strip()
    max_price = request.args.get("max_price", "").strip()
    category = request.args.get("category", "").strip()
    categories = run("SELECT category_id, name FROM category ORDER BY name")[1]
    sections = []
    error = None

    if request.args:
        conditions = []
        params = []
        try:
            lo = float(min_price) if min_price else None
            hi = float(max_price) if max_price else None
        except ValueError:
            lo = hi = None
            error = "Prices must be numbers."
        if error is None:
            if keyword:
                conditions.append("b.title LIKE %s")
                params.append("%" + keyword + "%")
            if lo is not None and hi is not None:
                conditions.append("b.price BETWEEN %s AND %s")
                params.extend([lo, hi])
            elif lo is not None:
                conditions.append("b.price >= %s")
                params.append(lo)
            elif hi is not None:
                conditions.append("b.price <= %s")
                params.append(hi)
            if category:
                conditions.append("b.category_id = %s")
                params.append(category)
            where = (" WHERE " + " AND ".join(conditions)) if conditions else ""
            sql = (
                "SELECT b.book_id, b.title, b.price, c.name AS category "
                "FROM book b JOIN category c ON b.category_id = c.category_id"
                + where
                + " ORDER BY b.price ASC"
            )
            sections.append(section("Matching books", sql, params))

    return render_template(
        "search.html",
        title="Search books",
        sections=sections,
        error=error,
        categories=categories,
        keyword=keyword,
        min_price=min_price,
        max_price=max_price,
        category=category,
    )


@app.route("/catalogue")
def catalogue():
    sql = (
        "SELECT b.book_id, b.title, b.price, b.publish_year, a.name AS author, "
        "p.name AS publisher, c.name AS category "
        "FROM book b "
        "JOIN author a ON b.author_id = a.author_id "
        "JOIN publisher p ON b.publisher_id = p.publisher_id "
        "JOIN category c ON b.category_id = c.category_id "
        "ORDER BY b.book_id"
    )
    return render_template("page.html", title="Catalogue", sections=[section("All books", sql)])


@app.route("/reports")
def reports():
    sections = [
        section(
            "Books and average price of each category",
            "SELECT c.name AS category, COUNT(b.book_id) AS books, ROUND(AVG(b.price), 2) AS average_price "
            "FROM category c LEFT JOIN book b ON b.category_id = c.category_id "
            "GROUP BY c.category_id, c.name",
        ),
        section(
            "Authors who wrote at least 2 books",
            "SELECT a.name AS author, COUNT(*) AS books "
            "FROM author a JOIN book b ON b.author_id = a.author_id "
            "GROUP BY a.author_id, a.name HAVING COUNT(*) >= 2",
        ),
        section(
            "Total, smallest and largest price of the library",
            "SELECT SUM(price) AS total_price, MIN(price) AS smallest_price, MAX(price) AS largest_price FROM book",
        ),
    ]
    return render_template("page.html", title="Reports", sections=sections)


@app.route("/loans")
def loans():
    sections = [
        section(
            "Loans not returned yet",
            "SELECT l.loan_id, b.title AS book, m.name AS member, l.loan_date "
            "FROM loan l JOIN book b ON l.book_id = b.book_id "
            "JOIN member m ON l.member_id = m.member_id "
            "WHERE l.return_date IS NULL ORDER BY l.loan_date",
        ),
        section(
            "Members who never borrowed a book",
            "SELECT m.member_id, m.name, m.email "
            "FROM member m LEFT JOIN loan l ON l.member_id = m.member_id "
            "WHERE l.loan_id IS NULL",
        ),
        section(
            "Books that were never borrowed",
            "SELECT b.book_id, b.title "
            "FROM book b LEFT JOIN loan l ON l.book_id = b.book_id "
            "WHERE l.loan_id IS NULL",
        ),
    ]
    return render_template("page.html", title="Loans", sections=sections)


@app.route("/most-borrowed")
def most_borrowed():
    sections = [
        section(
            "The 3 most borrowed books",
            "SELECT b.book_id, b.title, COUNT(*) AS loans "
            "FROM loan l JOIN book b ON l.book_id = b.book_id "
            "GROUP BY b.book_id, b.title ORDER BY loans DESC, b.title LIMIT 3",
        ),
        section(
            "The member with the most loans",
            "SELECT m.member_id, m.name, COUNT(*) AS loans "
            "FROM loan l JOIN member m ON l.member_id = m.member_id "
            "GROUP BY m.member_id, m.name ORDER BY loans DESC, m.name LIMIT 1",
        ),
    ]
    return render_template("page.html", title="Most borrowed", sections=sections)


@app.route("/authors-books")
def authors_books():
    sections = [
        section(
            "Number of books of every author",
            "SELECT a.author_id, a.name, COUNT(b.book_id) AS books "
            "FROM author a LEFT JOIN book b ON b.author_id = a.author_id "
            "GROUP BY a.author_id, a.name ORDER BY books DESC, a.name",
        ),
        section(
            "Books whose author and publisher are from the same country",
            "SELECT b.book_id, b.title, a.name AS author, p.name AS publisher, a.country "
            "FROM book b JOIN author a ON b.author_id = a.author_id "
            "JOIN publisher p ON b.publisher_id = p.publisher_id "
            "WHERE a.country = p.country",
        ),
    ]
    return render_template("page.html", title="Authors and books", sections=sections)


if __name__ == "__main__":
    app.run(debug=True)
