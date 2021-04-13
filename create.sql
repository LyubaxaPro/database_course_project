-- CREATE TABLE customers
-- (
--     NAME TEXT CHECK(NAME != ''),
-- 	SURNAME TEXT,
--     ID INTEGER CHECK(ID > 0)
-- );

-- INSERT INTO customers (name, surname, id) VALUES
--     ('Любовь', 'Прохорова', 1),
--     ('Дмитрий', 'Енин', 2),
-- 	('Дарья', 'Русинова', 3);


-- CREATE TABLE users
-- (
--     user_class_id
-- club_id
-- time
-- day_of_weekid INTEGER CHECK(user_id > 0) primary key
-- );

-- insert into users(user_id) values
-- (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12),(13),(14),(15);


-- CREATE TABLE customers
-- (
--     NAME TEXT CHECK(NAME != ''),
-- 	SURNAME TEXT,
--     ID INTEGER CHECK(ID > 0),
-- 	user_id integer,
-- 	FOREIGN KEY (user_id) REFERENCES users(user_id)
-- );

-- INSERT INTO customers (name, surname, id, user_id) VALUES
--     ('Любовь', 'Прохорова', 1, 1),
--     ('Дмитрий', 'Енин', 2, 2),
-- 	('Дарья', 'Русинова', 4, 3);

CREATE TABLE fitness_clubs
(
    club_id integer primary key,
    address text unique,
    city text,
    phone text unique
);

copy fitness_clubs(club_id, address, city, phone) from '/home/lyubaxapro/database_course_project/database_data/fitness_clubs.csv' with delimiter ',' header csv;

CREATE TABLE users
(
    user_id integer primary key,
    login text unique,
    password text,
    email text unique,
    phone text unique,
    role text,
    club_id integer references fitness_clubs (club_id)
);

copy users(user_id, login, password, email, phone, role, club_id) from '/home/lyubaxapro/database_course_project/database_data/users.csv' with delimiter ',' header csv;

CREATE TABLE prices
(
    tariff_id integer primary key,
    tariff_name text unique,
    tariff_description text unique,
    price_one_month integer check (price_one_month > 0),
    price_three_month integer check (price_three_month > 0),
    price_six_month integer check (price_six_month > 0),
    price_one_year integer check (price_one_year > 0)
);

copy prices(tariff_id, tariff_name, tariff_description, price_one_month, price_three_month, price_six_month, price_one_year) 
from '/home/lyubaxapro/database_course_project/database_data/prices.csv' with delimiter ',' header csv;

CREATE TABLE admin_records (
    update_instructor json,
    add_instructor json
);

create table services(
    service_id integer primary key,
    service_name text unique,
    service_description text unique
);

copy services(service_id, service_name, service_description) from '/home/lyubaxapro/database_course_project/database_data/services.csv' with delimiter ',' header csv;


create table group_classes(
    class_id integer primary key,
    class_name text,
    duration integer,
    description text
);

copy group_classes(class_id, class_name, duration, description) from '/home/lyubaxapro/database_course_project/database_data/group_classes.csv' with delimiter ',' header csv;
