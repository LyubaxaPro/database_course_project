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
    price_one_year integer check (price_one_year > 0),
    is_time_restricted boolean,
    min_time time,
    max_time time,
    days_of_week text[] 
);

copy prices(tariff_id, tariff_name, tariff_description, price_one_month, price_three_month,
            price_six_month, price_one_year, is_time_restricted, min_time, max_time, days_of_week) 
from '/home/lyubaxapro/database_course_project/database_data/prices.csv' with delimiter ';' header csv;

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
    instructor_id serial primary key,
    user_id integer references users_customuser(id) ON DELETE CASCADE ON UPDATE CASCADE,
    sex text,
    name text, 
    surname text, 
    patronymic text, 
    education text[],
    experience integer,
    achievements text[],
    specialization text[]
);

copy instructors(instructor_id, user_id, sex, name, surname, patronymic, education, experience, achievements, specialization) 
from '/home/lyubaxapro/database_course_project/database_data/instructors.csv' with delimiter ';' header csv;

create table customers
(
    customer_id serial primary key,
    user_id integer references users_customuser(id) ON DELETE CASCADE ON UPDATE CASCADE,
    sex text,
    name text,
    surname text,
    patronymic text,
    day_of_birth date,
    height integer,
    measured_weights integer[],
    measure_dates date[],
    tariff_id integer references prices(tariff_id) ON DELETE CASCADE ON UPDATE CASCADE, 
    tariff_end_date date,
    instructor_id integer  references instructors(instructor_id) ON DELETE CASCADE ON UPDATE CASCADE
);
copy customers(customer_id, user_id, sex, name, surname, patronymic, day_of_birth, height, measured_weights, measure_dates,
               tariff_id, tariff_end_date,instructor_id) from '/home/lyubaxapro/database_course_project/database_data/customers.csv' with delimiter ';' header csv;


create table group_classes_shedule
(
    shedule_id serial primary key,
    class_id integer references group_classes(class_id) ON DELETE CASCADE ON UPDATE CASCADE,
    club_id integer references fitness_clubs(club_id) ON DELETE CASCADE ON UPDATE CASCADE,
    instructor_id integer references instructors(instructor_id) ON DELETE CASCADE ON UPDATE CASCADE,
    class_time time,
    day_of_week text,
    maximum_quantity integer
);

copy group_classes_shedule(shedule_id,class_id, club_id, instructor_id, class_time,
day_of_week, maximum_quantity) from '/home/lyubaxapro/database_course_project/database_data/group_classes_shedule.csv' with delimiter ',' header csv;

create table group_classes_customers_records
(
    record_id serial primary key,
    shedule_id integer references group_classes_shedule(shedule_id) ON DELETE CASCADE ON UPDATE CASCADE, 
    customer_id integer references customers(customer_id) ON DELETE CASCADE ON UPDATE CASCADE,
    class_date date
);

copy group_classes_customers_records(shedule_id, customer_id, class_date) 
from '/home/lyubaxapro/database_course_project/database_data/group_classes_customers_records.csv' with delimiter ',' header csv;

create table special_offers
(
    offer_id integer primary key,
    offer_name text,
    offer_description text
);

copy special_offers(offer_id, offer_name, offer_description)
from '/home/lyubaxapro/database_course_project/database_data/special_offers.csv' with delimiter ',' header csv;

create table instructor_shedule
(
    i_shedule_id serial primary key,
    instructor_id integer references instructors(instructor_id) ON DELETE CASCADE ON UPDATE CASCADE,
    training_time time,
    day_of_week text
);

copy instructor_shedule(i_shedule_id ,instructor_id ,training_time ,day_of_week)
from '/home/lyubaxapro/database_course_project/database_data/instructor_shedule.csv' with delimiter ',' header csv;


create table instructor_shedule_customers
(
    record_id serial primary key,
    customer_id integer references customers(customer_id) ON DELETE CASCADE ON UPDATE CASCADE,
    i_shedule_id integer references instructor_shedule(i_shedule_id) ON DELETE CASCADE ON UPDATE CASCADE,
    training_date date    
);

copy instructor_shedule_customers(customer_id, i_shedule_id, training_date)
from '/home/lyubaxapro/database_course_project/database_data/instructor_shedule_customers.csv' with delimiter ',' header csv;


create table administrators
(
    user_id integer primary key references users_customuser(id) ON DELETE CASCADE ON UPDATE CASCADE,
    name varchar(30),
    surname varchar(30),
    patronym varchar(30)

);

create table admin_records
(
    id serial primary key,
    creation_datetime timestamp with time zone,
    status integer,
    instructor_id integer references instructors(instructor_id) ON DELETE CASCADE ON UPDATE CASCADE,
    admin_id integer references admins(id) ON DELETE CASCADE ON UPDATE CASCADE,
    change jsonb
);