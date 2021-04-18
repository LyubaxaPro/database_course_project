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

create table instructors
(   
    instructor_id integer primary key,
    user_id integer references users(user_id),
    sex text,
    name text, 
    surname text, 
    patronymic text, 
    education text[],
    experience integer,
    achievements text[],
    specialization text[]
);

copy group_classes(class_id, class_name, duration, description) from '/home/lyubaxapro/database_course_project/database_data/instructors.csv' with delimiter ',' header csv;

create table customers
(
    customer_id integer primary key,
    user_id integer references users(user_id),
    sex text,
    name text,
    surname text,
    patronymic text,
    day_of_birth date,
    measure jsonb,
    tariff_id integer references prices(tariff_id), 
    tariff_end_date date,
    instructor_id integer  references instructors(instructor_id)
);
copy customers(customer_id, user_id, sex, name, surname, patronymic, day_of_birth, measure, tariff_id, tariff_end_date,
instructor_id) from '/home/lyubaxapro/database_course_project/database_data/customers.csv' with delimiter ';' header csv;

create table group_classes_shedule
(
    shedule_id integer primary key,
    class_id integer references group_classes(class_id),
    club_id integer references fitness_clubs(club_id),
    instructor_id integer references instructors(instructor_id),
    class_time time,
    day_of_week text,
    maximum_quantity integer
);

copy group_classes_shedule(shedule_id,class_id, club_id, instructor_id, class_time,
day_of_week, maximum_quantity) from '/home/lyubaxapro/database_course_project/database_data/group_classes_shedule.csv' with delimiter ',' header csv;

create table group_classes_customers_records
(
    record_id serial primary key,
    shedule_id integer references group_classes_shedule(shedule_id), 
    customer_id integer references customers(customer_id),
    class_date date
);

copy group_classes_customers_records(shedule_id, customer_id, class_date) from '/home/lyubaxapro/database_course_project/database_data/group_classes_customers_records.csv' with delimiter ',' header csv;
