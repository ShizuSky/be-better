import sqlite3
from datetime import date, datetime, timedelta

class Database:
    def __init__(self, db_name="better_me.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                streak INTEGER DEFAULT 0,
                last_completed TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                task_date TEXT NOT NULL,
                is_done INTEGER DEFAULT 0
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                category TEXT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                exercise_name TEXT NOT NULL,
                sets INTEGER,
                reps INTEGER,
                weight REAL,
                workout_date TEXT NOT NULL
            )
        ''')

        self.conn.commit()

    def add_habit(self, name):
        self.cursor.execute("INSERT INTO habits (name, streak) VALUES (?, 0)", (name,))
        self.conn.commit()

    def get_all_habits(self):
        self.cursor.execute("SELECT * FROM habits")
        return self.cursor.fetchall()

    def delete_habit(self, habit_id):
        self.cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        self.conn.commit()

    def complete_habit(self, habit_id):
        today = date.today()
        today_str = str(today)
        yesterday_str = str(today - timedelta(days=1))

        self.cursor.execute("SELECT streak, last_completed FROM habits WHERE id = ?", (habit_id,))
        habit = self.cursor.fetchone()

        if habit:
            streak, last_completed = habit
            if last_completed == today_str: return False
            new_streak = streak + 1 if last_completed == yesterday_str else 1

            self.cursor.execute("UPDATE habits SET streak = ?, last_completed = ? WHERE id = ?",
                                (new_streak, today_str, habit_id))
            self.conn.commit()
            return True

    def add_task(self, title, task_date):
        self.cursor.execute("INSERT INTO tasks (title, task_date) VALUES (?, ?)", (title, task_date))
        self.conn.commit()

    def get_tasks_by_date(self, task_date):
        self.cursor.execute("SELECT * FROM tasks WHERE task_date = ?", (task_date,))
        return self.cursor.fetchall()

    def toggle_task(self, task_id, current_state):
        new_state = 1 if current_state == 0 else 0
        self.cursor.execute("UPDATE tasks SET is_done = ? WHERE id = ?", (new_state, task_id))
        self.conn.commit()

    def delete_task(self, task_id):
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()


    def get_exercise_list(self):
        self.cursor.execute("SELECT name FROM exercises ORDER BY name")
        return [row[0] for row in self.cursor.fetchall()]

    def add_workout_entry(self, session_id, ex_name, sets, reps, weight, workout_date):

        self.cursor.execute(
            "INSERT INTO workouts (session_id, exercise_name, sets, reps, weight, workout_date) VALUES (?, ?, ?, ?, ?, ?)",
            (session_id, ex_name, sets, reps, weight, workout_date))
        self.conn.commit()

    def get_workout_details(self, session_id):

        self.cursor.execute("SELECT exercise_name, sets, reps, weight FROM workouts WHERE session_id = ?", (session_id,))
        return self.cursor.fetchall()

    def delete_workout_entry(self, entry_id):
        self.cursor.execute("DELETE FROM workouts WHERE id = ?", (entry_id,))
        self.conn.commit()

    def get_history_summary(self):
        self.cursor.execute("""
            SELECT session_id, workout_date, SUM(sets*reps*weight) 
            FROM workouts 
            GROUP BY session_id 
            ORDER BY session_id DESC
        """)
        return self.cursor.fetchall()