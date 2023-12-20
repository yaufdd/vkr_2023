import psycopg2

def save_student_todb(name, group_name, login, password, telegram_id):
        conn = psycopg2.connect(
            dbname='telegrambot_vkr',
            user='usr',
            host='localhost',
            port='5432'
    )
        cursor = conn.cursor()

        insert_query = "INSERT INTO Students (name, group_name, login, password, telegram_id) VALUES (%s, %s, %s, %s, %s);"
        data_to_insert = (name, group_name, login, password, telegram_id)
        cursor.execute(insert_query, data_to_insert)

        conn.commit()

        # закрыть курсор и соединение после использования
        cursor.close()
        conn.close()

        

def save_schedule_todb(student_tgID, json_schedule):
    conn = psycopg2.connect(
        dbname='telegrambot_vkr',
        user='usr',
        host='localhost',
        port='5432'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Students WHERE telegram_id = %s;", (student_tgID,))
    student_id = cursor.fetchone()[0]

    for lesson in json_schedule['lessons']:
        discipline = lesson['discipline']['name']
        lesson_type = lesson['lesson_type']['name']
        try : 
            teacher = lesson['teachers'][0]['name']
        except IndexError:
            teacher = "Неизвестно"
        classroom = lesson['room']['name']
        campus = lesson['room']['campus']['name']
        calls = lesson['calls']['num']
        week_day = lesson['weekday']
        week_number = lesson['weeks'][0]
        is_weekEven = False
        if week_number % 2 == 0:
            is_weekEven = True
        else:
            is_weekEven = False
        insert_query = "INSERT INTO schedules (student_id, discipline_name, lesson_type, teacher_name, classroom, campus, calls, week_day, even) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        data_to_insert = (student_id, discipline, lesson_type, teacher, classroom, campus, calls, week_day, is_weekEven)

        cursor.execute(insert_query, data_to_insert)
        conn.commit()


    # закрыть курсор и соединение после использования
    cursor.close()
    conn.close()


    

def get_todaySchedule(isweekType_even, current_weekday, current_tgId):
    conn = psycopg2.connect(
    dbname='telegrambot_vkr',
    user='usr',
    host='localhost',
    port='5432'
)
    cursor = conn.cursor()
    if isweekType_even:
        if current_weekday == 1: 
            query = find_subjects(1, "TRUE", current_tgId)
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows: 
                return rows
            else:
                return "Сегодня нет пар"
        if current_weekday == 2:  
            query = find_subjects(2, "TRUE", current_tgId)
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows: 
                return rows
            else:
                return "Сегодня нет пар"

        if current_weekday == 3: 
            query = find_subjects(3, "TRUE", current_tgId)
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows: 
                return rows
            else:
                return "Сегодня нет пар"

        if current_weekday == 4: 
            query = find_subjects(4, "TRUE", current_tgId)
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows: 
                return rows
            else:
                return "Сегодня нет пар"

        if current_weekday == 5: 
            query = find_subjects(5, "TRUE", current_tgId)
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows: 
                return rows
            else:
                return "Сегодня нет пар"

        if current_weekday == 6:
            query = find_subjects(6, "TRUE", current_tgId)
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows: 
                return rows
            else:
                return "Сегодня нет пар"

        return 'Unknown'
    else:
        if current_weekday == 1: 
            query = find_subjects(1, "FALSE", current_tgId)
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows: 
                return rows
            else:
                return "Сегодня нет пар"

        if current_weekday == 2: 
            query = find_subjects(2, "FALSE", current_tgId)
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows: 
                return rows
            else:
                return "Сегодня нет пар"
        if current_weekday == 3:
            query = find_subjects(3, "FALSE", current_tgId)
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows: 
                return rows
            else:
                return "Сегодня нет пар"
        if current_weekday == 4:
            query = find_subjects(4, "FALSE", current_tgId)
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows: 
                return rows
            else:
                return "Сегодня нет пар"

        if current_weekday == 5:
            query = find_subjects(5, "FALSE", current_tgId)
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows: 
                return rows
            else:
                return "Сегодня нет пар"


        if current_weekday == 6:
            query = find_subjects(6, "FALSE", current_tgId)
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows: 
                return rows
            else:
                return "Сегодня нет пар"

            
    cursor.close()
    conn.close()


def find_subjects(week_number, isEven, tg_id):
    query = f"""
            SELECT 
            Schedules.discipline_name,
            Schedules.lesson_type,
            Schedules.teacher_name,
            Schedules.classroom,
            Schedules.campus
        FROM Schedules
        JOIN Students ON Schedules.student_id = Students.id
        WHERE Students.telegram_id = {str(tg_id)}
        AND Schedules.week_day = {str(week_number)}
        AND Schedules.even = {isEven};
            """
    return query

        
        

    
