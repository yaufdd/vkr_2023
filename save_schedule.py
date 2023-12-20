import psycopg2
from datetime import datetime

def get_todaySchedule(isweekType_even, current_weekday):
    conn = psycopg2.connect(
    dbname='telegrambot_vkr',
    user='usr',
    host='localhost',
    port='5432'
)
    cursor = conn.cursor()
    if isweekType_even:
        if current_weekday == 1: 
            query = """
                    SELECT discipline_name, lesson_type, teacher_name, classroom, campus, calls FROM schedules
                    WHERE week_day = 1 AND even = TRUE;
                    """
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        if current_weekday == 2: 
            return 'Tuesday'
        if current_weekday == 3: 
            return 'Wednesday'
        if current_weekday == 4: 
            return 'Thursday'
        if current_weekday == 5: 
            return 'Friday'
        if current_weekday == 6:
            return 'Saturday'
        return 'Unknown'
    else:
        pass


    cursor.close()
    conn.close()


def week_evenOrNot(target_date):
    year = target_date.year
    september_1 = datetime(year, 9, 1)
    weekday = september_1.weekday()
    count = (target_date - september_1).days
    number = (count + weekday) // 7 + 1

    even = True
    if number % 2 != 0:
        even = False

    return even, target_date.weekday()


# even, weekday = week_evenOrNot(datetime.today())
# print(even, weekday)
#print(datetime.today().year)

td_sche = get_todaySchedule(True, 1)
