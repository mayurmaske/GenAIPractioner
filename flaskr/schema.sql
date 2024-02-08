-- You need to create two tables in a SQLite database: "user" and "product". Write SQL commands to achieve this.

-- Start by ensuring that if tables with the same names already exist, they are dropped to avoid conflicts.

-- Then, create the "user" table with the following columns:

-- id: An INTEGER primary key that auto-increments.
-- username: A TEXT field that must be unique and cannot be null.
-- password: A TEXT field that cannot be null.
-- Next, create the "product" table with the following columns:

-- id: An INTEGER primary key that auto-increments.
-- name: A TEXT field for the name of the product, which cannot be null.
-- url: A TEXT field for the URL of the product image, which cannot be null.
-- price: An INTEGER field representing the price of the product, which cannot be null.
-- description: A TEXT field for the description of the product, which cannot be null.
-- add mobile_number column to user table

drop table if exists user;
drop table if exists product;
create table user (
    id integer primary key autoincrement,
    username text not null,
    password text not null,
    mobile_number integer not null
);
create table product (
    id integer primary key autoincrement,
    name text not null,
    url text not null,
    price integer not null,
    description text not null
);

-- write code to create table 'cart' with following columns
-- id: an integer primary key that auto-increments
-- name: a text field for the name of the product, which cannot be null
-- price: an integer field representing the price of the product, which cannot be null

drop table if exists cart;
create table cart (
    id integer primary key autoincrement,
    name text not null,
    price integer not null
);

