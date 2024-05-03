import psycopg2
from psycopg2 import sql
import datetime


def save_student_in_db(tg_id, name, student_group, group_uid, login, password):
    conn = psycopg2.connect(dbname='univer_helper', user='usr', host='localhost', port=5555)
    cur = conn.cursor()
    try:
        insert_query = """
        INSERT INTO students (tg_id, name, group_name, group_uid, login, password) VALUES (%s, %s, %s, %s, %s, %s);
        """
        data_tuple = (tg_id, name, student_group, group_uid, login, password)
        cur.execute(insert_query, data_tuple)
        conn.commit()
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        cur.close()
        conn.close()


def save_subject_of_student_in_db(subject_name, teacher, student_tg_id):
    conn = psycopg2.connect(dbname='univer_helper', user='usr', host='localhost', port=5555)
    cur = conn.cursor()

    insert_query = "INSERT INTO subjects (name, teacher, student_tg_id) VALUES (%s, %s, %s)"
    data_tuple = subject_name, teacher, student_tg_id
    cur.execute(insert_query, data_tuple)
    conn.commit()

    cur.close()
    conn.close()


def save_homework_in_db(content, deadline, subject_name):
    try:
        conn = psycopg2.connect(dbname='univer_helper', user='usr', host='localhost', port=5555)
        cur = conn.cursor()

        cur.execute("SELECT id FROM subjects WHERE name = %s", (subject_name,))
        subject_id = cur.fetchone()[0]
        print(subject_id)

        insert_query = "INSERT INTO homeworks (content, deadline, subject_id) VALUES (%s, %s, %s);"
        data_tuple = content, deadline, subject_id
        cur.execute(insert_query, data_tuple)
        conn.commit()
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        cur.close()
        conn.close()  


def save_homework_deadline(deadline, subject_name):
    try:
        conn = psycopg2.connect(dbname='univer_helper', user='usr', host='localhost', port=5555)
        cur = conn.cursor()
        cur.execute("SELECT id FROM subjects WHERE name = %s", (subject_name,))
        subject_id = cur.fetchone()
        if not subject_id:
            print("Предмет с таким названием не найден.")
            return

        update_query = "INSERT INTO homeworks (deadline, subject_id) VALUES (%s, %s)"
        data_tuple = deadline, subject_id
        cur.execute(update_query, data_tuple)
        conn.commit()
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        cur.close()
        conn.close()   


def get_homeworks_from_db(cur_tg_id):
    try:
        conn = psycopg2.connect(dbname='univer_helper', user='usr', host='localhost', port=5555)
        cur = conn.cursor()
        
        cur.execute(f"""
            SELECT h.content, h.deadline, s.name AS subject_name
            FROM homeworks h
            JOIN subjects s ON h.subject_id = s.id
            WHERE s.student_tg_id = %s;
            """, (cur_tg_id,))
        homeworks = cur.fetchall()

        return homeworks
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        cur.close()
        conn.close()  

def get_subject_id_by_name(subject_name):
    try:
        conn = psycopg2.connect(dbname='univer_helper', user='usr', host='localhost', port=5555)
        cur = conn.cursor()

        cur.execute("SELECT id FROM subjects WHERE name = %s", (subject_name,))
        subject_id = cur.fetchone()[0]

        return subject_id
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        cur.close()
        conn.close()   


def get_subjects_of_student_by_tg_id(cur_tg_id):
    try:
        conn = psycopg2.connect(dbname='univer_helper', user='usr', host='localhost', port=5555)
        cur = conn.cursor()
        query = "SELECT name FROM subjects WHERE student_tg_id = %s;"
        cur.execute(query, (cur_tg_id, ))
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        cur.close()
        conn.close()  


def get_group_uid_by_tg_id(cur_tg_id):
    try:
        conn = psycopg2.connect(dbname='univer_helper', user='usr', host='localhost', port=5555)
        cur = conn.cursor()
        query = "SELECT group_uid FROM students WHERE tg_id = %s;"
        cur.execute(query, (cur_tg_id, ))
        result = cur.fetchone()
        uid = result[0]
        return uid
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        cur.close()
        conn.close()  


def show_table():
    conn = psycopg2.connect(dbname='univer_helper', user='usr', host='localhost', port=5555)
    cur = conn.cursor()

    insert_query = "select * from subjects"
    cur.execute(insert_query)

    rows = cur.fetchall()
    for row in rows:
        print(f"id: {row[0]}, name: {row[1]}, teacher: {row[2]}")

    cur.close()
    conn.close()

def is_user_exists_by_id(cur_tg_id):
    conn = psycopg2.connect(dbname='univer_helper', user='usr', host='localhost', port=5555)
    cur = conn.cursor()
    try:
        query = "SELECT * FROM students WHERE tg_id = %s;"
        cur.execute(query, (cur_tg_id, ))
        is_user_exists = cur.fetchone() is not None
        return is_user_exists
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        cur.close()
        conn.close()



