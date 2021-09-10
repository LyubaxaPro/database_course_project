create or replace function translate_day_of_week(day text) RETURNS text AS $$
        BEGIN
        IF day = 'Monday' THEN
                RETURN 'понедельник';
        ELSIF day = 'Tuesday' THEN
                RETURN 'вторник';
        ELSIF day = 'Wednesday' THEN
                RETURN 'среда';
        ELSIF day = 'Thursday' THEN
                RETURN 'четверг';
        ELSIF day = 'Friday' THEN
                RETURN 'пятница';
        ELSIF day = 'Saturday' THEN
                RETURN 'суббота';
        ELSIF day = 'Sunday' THEN
                RETURN 'воскресенье';
        END IF;     
        END;
$$ LANGUAGE plpgsql

--Тренер добавил персональную тренировку в расписание
CREATE OR REPLACE FUNCTION log_for_instructor_add_personal() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO instructor_personal_trainings_logs(act_date, instructor_id, description) 
    values (NOW(), NEW.instructor_id, 'Добавление персональной тренировки ' || translate_day_of_week(NEW.day_of_week)||' ' || NEW.training_time);
        RETURN NEW;
END;
$$ LANGUAGE plpgsql;

 drop TRIGGER IF EXISTS log_for_instructor_add_personal ON instructor_shedule;
 CREATE TRIGGER log_for_instructor_add_personal AFTER INSERT ON instructor_shedule
      FOR EACH ROW EXECUTE PROCEDURE log_for_instructor_add_personal();


--Тренер удалил персональную тренировку из расписания
CREATE OR REPLACE FUNCTION log_for_instructor_delete_personal() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO instructor_personal_trainings_logs(act_date, instructor_id, description) 
    values (NOW(), OLD.instructor_id, 'Отмена персональной тренировки ' || translate_day_of_week(OLD.day_of_week)||' ' || OLD.training_time);
        RETURN OLD;
END;
$$ LANGUAGE plpgsql;


 drop TRIGGER IF EXISTS log_for_instructor_delete_personal ON instructor_shedule;
 CREATE TRIGGER log_for_instructor_delete_personal BEFORE DELETE ON instructor_shedule
      FOR EACH ROW EXECUTE PROCEDURE log_for_instructor_delete_personal();


--Администратор добавил групповую тренировку в расписание
CREATE OR REPLACE FUNCTION log_for_admin_add_group_class() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO admin_group_classes_logs(act_date, club, group_class_id, description) 
    values (NOW(), NEW.club_id, NEW.class_id,'Добавление групповой тренировки: ' || translate_day_of_week(NEW.day_of_week)||' ' || NEW.class_time);
        RETURN NEW;
END;
$$ LANGUAGE plpgsql;

 drop TRIGGER IF EXISTS log_for_admin_add_group_class ON group_classes_shedule;
 CREATE TRIGGER log_for_admin_add_group_class AFTER INSERT ON group_classes_shedule
      FOR EACH ROW EXECUTE PROCEDURE log_for_admin_add_group_class();


--Администратор удалил групповую тренировку в расписание
CREATE OR REPLACE FUNCTION log_for_admin_delete_group_class() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO admin_group_classes_logs(act_date, club, group_class_id, description) 
    values (NOW(), OLD.club_id, OLD.class_id,'Отмена групповой тренировки: ' || translate_day_of_week(OLD.day_of_week)||' ' || OLD.class_time);
        RETURN OLD;
END;
$$ LANGUAGE plpgsql;

 drop TRIGGER IF EXISTS log_for_admin_delete_group_class ON group_classes_shedule;
 CREATE TRIGGER log_for_admin_delete_group_class BEFORE DELETE ON group_classes_shedule
      FOR EACH ROW EXECUTE PROCEDURE log_for_admin_delete_group_class();

      

