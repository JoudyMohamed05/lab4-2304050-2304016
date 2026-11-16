USE library;

-- F2.1
SELECT b.book_id, b.title, b.price, c.name AS category
FROM book b
JOIN category c ON b.category_id = c.category_id
WHERE b.title LIKE '%a%' AND b.price BETWEEN 10 AND 20 AND b.category_id = 3
ORDER BY b.price ASC;

-- F2.2
SELECT b.book_id, b.title, b.price, b.publish_year, a.name AS author, p.name AS publisher, c.name AS category
FROM book b
JOIN author a ON b.author_id = a.author_id
JOIN publisher p ON b.publisher_id = p.publisher_id
JOIN category c ON b.category_id = c.category_id
ORDER BY b.book_id;

-- F2.3 (a)
SELECT c.name AS category, COUNT(b.book_id) AS books, ROUND(AVG(b.price), 2) AS average_price
FROM category c
LEFT JOIN book b ON b.category_id = c.category_id
GROUP BY c.category_id, c.name;

-- F2.3 (b)
SELECT a.name AS author, COUNT(*) AS books
FROM author a
JOIN book b ON b.author_id = a.author_id
GROUP BY a.author_id, a.name
HAVING COUNT(*) >= 2;

-- F2.3 (c)
SELECT SUM(price) AS total_price, MIN(price) AS smallest_price, MAX(price) AS largest_price
FROM book;

-- F2.4 (a)
SELECT l.loan_id, b.title AS book, m.name AS member, l.loan_date
FROM loan l
JOIN book b ON l.book_id = b.book_id
JOIN member m ON l.member_id = m.member_id
WHERE l.return_date IS NULL
ORDER BY l.loan_date;

-- F2.4 (b)
SELECT m.member_id, m.name, m.email
FROM member m
LEFT JOIN loan l ON l.member_id = m.member_id
WHERE l.loan_id IS NULL;

-- F2.4 (c)
SELECT b.book_id, b.title
FROM book b
LEFT JOIN loan l ON l.book_id = b.book_id
WHERE l.loan_id IS NULL;

-- F2.5 (a)
SELECT b.book_id, b.title, COUNT(*) AS loans
FROM loan l
JOIN book b ON l.book_id = b.book_id
GROUP BY b.book_id, b.title
ORDER BY loans DESC, b.title
LIMIT 3;

-- F2.5 (b)
SELECT m.member_id, m.name, COUNT(*) AS loans
FROM loan l
JOIN member m ON l.member_id = m.member_id
GROUP BY m.member_id, m.name
ORDER BY loans DESC, m.name
LIMIT 1;

-- F2.6 (a)
SELECT a.author_id, a.name, COUNT(b.book_id) AS books
FROM author a
LEFT JOIN book b ON b.author_id = a.author_id
GROUP BY a.author_id, a.name
ORDER BY books DESC, a.name;

-- F2.6 (b)
SELECT b.book_id, b.title, a.name AS author, p.name AS publisher, a.country
FROM book b
JOIN author a ON b.author_id = a.author_id
JOIN publisher p ON b.publisher_id = p.publisher_id
WHERE a.country = p.country;
