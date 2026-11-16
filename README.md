# Lab 4 - Search Queries in SQL (Problem 2: Library)

Introduction to Database Systems, Fall 2026, Alexandria National University
Dr. Yasser Fouad

## Team

| Name | ID | Group | Did what |
|------|----|-------|----------|
| Joudy Mohamed Aly | 2304050 | 2 | Worked on everything together with Raneem: DDL, seed data, queries, Flask back end, login and register, templates and CSS, testing, README |
| Raneem Ahmed Ragab | 2304016 | 2 | Worked on everything together with Joudy: DDL, seed data, queries, Flask back end, login and register templates and CSS, testing, README |

## Technology

- Back end: Python 3 + Flask (sessions for login, `bcrypt` for password hashes)
- Database: MySQL, accessed with `mysql-connector-python` (plain SQL, no ORM): database `library` for the pages and database `registration` (table `users`) for sign-up and login
- Front end: HTML (Jinja templates) + CSS + a little JavaScript

## Files

```
lab4-2304050-2304016/
  problem2_DDL.sql       six tables, primary keys, foreign keys, ON DELETE CASCADE
  problem2_DML.sql       seed data
  problem2_Queries.sql   the SQL of the pages F2.1 - F2.6
  auth_schema.sql        database registration + table users (login and register)
  website/               the Flask site
  README.md
```

## How to run it (from an empty machine)

1. Install Python 3, MySQL Server and Git.
2. Build the databases and insert the data (type the MySQL root password when asked):
   ```
   mysql -u root -p < problem2_DDL.sql
   mysql -u root -p < problem2_DML.sql
   mysql -u root -p < auth_schema.sql
   ```
3. Go to the website folder and install the packages:
   ```
   cd website
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
   (on Linux/macOS: `source venv/bin/activate`)
4. Copy `.env.example` to `.env`, write your MySQL password in `DB_PASSWORD` and any long random text in `SECRET_KEY`.
5. Start the server:
   ```
   python app.py
   ```
6. Open http://127.0.0.1:5000 (you are sent to the login page; click Register to create an account).

To run the page queries by hand: `mysql -u root -p library < problem2_Queries.sql`

## Features

| Page | Address | What it shows |
|------|---------|---------------|
| F2.1 Search books | /search | title keyword (LIKE), min and max price (BETWEEN), category list, cheapest first |
| F2.2 Catalogue | /catalogue | books with author, publisher and category names (JOIN) |
| F2.3 Reports | /reports | books and average price per category, authors with 2+ books, total/min/max price |
| F2.4 Loans | /loans | loans not returned yet, members who never borrowed, books never borrowed |
| F2.5 Most borrowed | /most-borrowed | top 3 books and the member with most loans |
| F2.6 Authors and books | /authors-books | books per author (including 0), books whose author and publisher share a country |

Login and register: every page needs a logged-in user, otherwise the visitor is sent to the login page.

| Page | Address | What it does |
|------|---------|--------------|
| Register | /register | name, email, password, confirm password; a duplicate email shows `Email Already Exists`; after success the user is logged in |
| Login | /login | email and password; a wrong email or a wrong password both show `Invalid email or password` |
| Logout | button in the header | ends the session |

Checks run in the browser (JavaScript) and again on the server with the same messages. Passwords are stored as bcrypt hashes, all SQL uses parameters, and the `user_id` is kept in the server session. The password fields have an eye button to show or hide the typed password.

Bonus: the search form in F2.1 uses prepared statements (`%s` placeholders); the typed values are never glued into the SQL text.

## Seed data

4 authors with books and 1 author without books (Paulo Coelho), 3 publishers, 3 categories, 10 books, 5 members, 12 loans. It contains two authors from the same country (Egypt and UK), an author who wrote 2 or more books, an author and a publisher from the same country, books priced between 15 and 20, books never borrowed, a member with no loans and loans that are not returned yet.

The `price` column of `book` has `CHECK (price >= 0)`, so a book can never get a negative price.

Reviewed and tested by Raneem Ahmed.