USE library;

INSERT INTO author (author_id, name, country) VALUES
(1, 'Naguib Mahfouz', 'Egypt'),
(2, 'Taha Hussein', 'Egypt'),
(3, 'George Orwell', 'UK'),
(4, 'Jane Austen', 'UK'),
(5, 'Paulo Coelho', 'Brazil');

INSERT INTO publisher (publisher_id, name, country) VALUES
(1, 'Dar El Shorouk', 'Egypt'),
(2, 'Penguin Books', 'UK'),
(3, 'HarperCollins', 'USA');

INSERT INTO category (category_id, name) VALUES
(1, 'Fiction'),
(2, 'Non-Fiction'),
(3, 'Classics');

INSERT INTO book (book_id, title, price, publish_year, author_id, publisher_id, category_id) VALUES
(1, 'Palace Walk', 18.50, 1956, 1, 1, 3),
(2, 'Sugar Street', 16.00, 1957, 1, 1, 3),
(3, 'Children of the Alley', 22.00, 1959, 1, 1, 1),
(4, 'The Days', 14.00, 1929, 2, 1, 2),
(5, 'Animal Farm', 12.50, 1945, 3, 2, 3),
(6, '1984', 19.99, 1949, 3, 2, 1),
(7, 'Pride and Prejudice', 9.99, 1813, 4, 2, 3),
(8, 'Emma', 11.50, 1815, 4, 2, 3),
(9, 'Homage to Catalonia', 15.00, 1938, 3, 3, 2),
(10, 'On Pre-Islamic Poetry', 13.75, 1926, 2, 1, 2);

INSERT INTO member (member_id, name, email, join_date) VALUES
(1, 'Ahmed Hassan', 'ahmed.hassan@mail.com', '2026-01-10'),
(2, 'Sara Ali', 'sara.ali@mail.com', '2026-02-15'),
(3, 'Omar Khaled', 'omar.khaled@mail.com', '2026-03-05'),
(4, 'Mona Samir', 'mona.samir@mail.com', '2026-04-20'),
(5, 'Youssef Adel', 'youssef.adel@mail.com', '2026-05-12');

INSERT INTO loan (loan_id, book_id, member_id, loan_date, return_date) VALUES
(1, 1, 1, '2026-09-01', '2026-09-10'),
(2, 1, 2, '2026-09-12', '2026-09-20'),
(3, 1, 3, '2026-10-01', '2026-10-08'),
(4, 6, 1, '2026-09-05', '2026-09-15'),
(5, 6, 2, '2026-10-02', '2026-10-12'),
(6, 5, 3, '2026-09-20', '2026-09-30'),
(7, 5, 4, '2026-10-10', NULL),
(8, 2, 2, '2026-10-15', NULL),
(9, 3, 1, '2026-10-20', '2026-10-28'),
(10, 7, 4, '2026-10-22', NULL),
(11, 8, 2, '2026-11-01', '2026-11-08'),
(12, 4, 2, '2026-11-05', NULL);
