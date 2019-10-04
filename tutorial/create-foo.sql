DROP DATABASE foo;
CREATE DATABASE foo;
\c foo;

CREATE TABLE bar (
id INTEGER PRIMARY KEY,
name VARCHAR NOT NULL,
phone_number VARCHAR,
salary MONEY
);

INSERT INTO bar (id, name) VALUES (234, 'Nandan');
