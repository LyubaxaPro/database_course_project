
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO guest;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO instructor;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO customer;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO administrator;
--------------------------------------------------------------

CREATE ROLE GUEST WITH LOGIN PASSWORD 'quest_password';
GRANT INSERT ON users_customuser to guest;
GRANT INSERT ON customers to guest;
GRANT INSERT ON instructors to guest;
GRANT SELECT ON users_customuser to guest;
GRANT SELECT ON fitness_clubs to guest;
GRANT SELECT ON group_classes to guest;
GRANT SELECT ON group_classes_shedule to guest;
GRANT SELECT ON instructor_shedule to guest;
GRANT SELECT ON instructors to guest;
GRANT SELECT ON prices to guest;
GRANT SELECT ON services to guest;
GRANT SELECT ON special_offers to guest;

--------------------------------------------------------

CREATE ROLE CUSTOMER WITH LOGIN PASSWORD 'customer_password';
GRANT SELECT ON users_customuser to customer;
GRANT INSERT ON users_customuser to customer;

GRANT SELECT ON customers to customer;
GRANT UPDATE ON customers to customer;
GRANT INSERT ON customers to customer;

GRANT SELECT ON fitness_clubs to customer;
GRANT SELECT ON group_classes to customer;

GRANT SELECT ON group_classes_customers_records to customer;
GRANT INSERT ON group_classes_customers_records to customer;
GRANT DELETE ON group_classes_customers_records to customer;

GRANT SELECT ON group_classes_shedule to customer;
GRANT SELECT ON admin_group_classes_logs to customer;
GRANT SELECT ON instructor_personal_trainings_logs to customer;
GRANT SELECT ON instructor_shedule to customer;
GRANT SELECT ON instructor_shedule_customers to customer;
GRANT INSERT ON instructor_shedule_customers to customer;
GRANT DELETE ON instructor_shedule_customers to customer;
GRANT SELECT ON instructors to customer;
GRANT SELECT ON prices to customer;
GRANT SELECT ON services to customer;
GRANT SELECT ON special_offers to customer;


------------------------------------------------------------------
CREATE ROLE INSTRUCTOR WITH LOGIN PASSWORD 'instructor_password';

GRANT SELECT ON users_customuser to instructor;
GRANT INSERT ON users_customuser to instructor;

GRANT SELECT ON admin_records to instructor;
GRANT INSERT ON admin_records to instructor;
GRANT DELETE ON admin_records to instructor;

GRANT SELECT ON instructors to instructor;
GRANT INSERT ON instructors to instructor;

GRANT SELECT ON customers to instructor;
GRANT SELECT ON fitness_clubs to instructor;
GRANT SELECT ON group_classes to instructor;
GRANT SELECT ON group_classes_shedule to instructor;
GRANT SELECT ON group_classes_shedule to instructor;

GRANT SELECT ON instructor_personal_trainings_logs to instructor;
GRANT INSERT ON instructor_personal_trainings_logs to instructor;

GRANT SELECT ON instructor_shedule to instructor;
GRANT INSERT ON instructor_shedule to instructor;
GRANT DELETE ON instructor_shedule to instructor;

GRANT SELECT ON instructor_shedule_customers to instructor;
GRANT SELECT ON prices to instructor;
GRANT SELECT ON special_offers to instructor;
GRANT SELECT ON administrators to instructor;
GRANT DELETE ON instructor_shedule_customers to instructor;
GRANT SELECT ON group_classes_customers_records to instructor;


------------------------------------------------------------------------
CREATE ROLE ADMINISTRATOR WITH LOGIN PASSWORD 'admin_password';

GRANT SELECT ON users_customuser to administrator;
GRANT DELETE ON users_customuser to administrator;

GRANT SELECT ON admin_group_classes_logs to administrator;
GRANT INSERT ON admin_group_classes_logs to administrator;

GRANT SELECT ON admin_records to administrator;
GRANT UPDATE ON admin_records to administrator;

GRANT SELECT ON administrators to administrator;
GRANT SELECT ON customers to administrator;
GRANT SELECT ON fitness_clubs to administrator;
GRANT SELECT ON group_classes to administrator;

GRANT SELECT ON group_classes_customers_records to administrator;
GRANT DELETE ON group_classes_customers_records to administrator;

GRANT SELECT ON group_classes_shedule to administrator;
GRANT INSERT ON group_classes_shedule to administrator;
GRANT DELETE ON group_classes_shedule to administrator;

GRANT SELECT ON instructor_shedule to administrator;
GRANT SELECT ON instructor_shedule_customers to administrator;

GRANT SELECT ON instructors to administrator;
GRANT UPDATE ON instructors to administrator;
GRANT DELETE ON instructors to administrator;

GRANT SELECT ON prices to administrator;
GRANT SELECT ON services to administrator;

GRANT SELECT ON special_offers to administrator;
GRANT INSERT ON special_offers to administrator;
GRANT DELETE ON special_offers to administrator;
----------------------------------------------------------


GRANT ALL ON auth_group to guest;
GRANT ALL ON auth_group_permissions to guest;
GRANT ALL ON auth_permission to guest;
GRANT ALL ON django_admin_log to guest;
GRANT ALL ON django_content_type to guest;
GRANT ALL ON django_migrations to guest;
GRANT ALL ON django_session to guest;
GRANT ALL ON users_customuser_groups to guest;
GRANT ALL ON users_customuser_user_permissions to guest;

GRANT ALL ON auth_group to customer;
GRANT ALL ON auth_group_permissions to customer;
GRANT ALL ON auth_permission to customer;
GRANT ALL ON django_admin_log to customer;
GRANT ALL ON django_content_type to customer;
GRANT ALL ON django_migrations to customer;
GRANT ALL ON django_session to customer;
GRANT ALL ON users_customuser_groups to customer;
GRANT ALL ON users_customuser_user_permissions to customer;

GRANT ALL ON auth_group to instructor;
GRANT ALL ON auth_group_permissions to instructor;
GRANT ALL ON auth_permission to instructor;
GRANT ALL ON django_admin_log to instructor;
GRANT ALL ON django_content_type to instructor;
GRANT ALL ON django_migrations to instructor;
GRANT ALL ON django_session to instructor;
GRANT ALL ON users_customuser_groups to instructor;
GRANT ALL ON users_customuser_user_permissions to instructor;

GRANT ALL ON auth_group to administrator;
GRANT ALL ON auth_group_permissions to administrator;
GRANT ALL ON auth_permission to administrator;
GRANT ALL ON django_admin_log to administrator;
GRANT ALL ON django_content_type to administrator;
GRANT ALL ON django_migrations to administrator;
GRANT ALL ON django_session to administrator;
GRANT ALL ON users_customuser_groups to administrator;
GRANT ALL ON users_customuser_user_permissions to administrator;
