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
                is_done INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    # --- SEKCOJA NAWYKÓW ---

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
            if last_completed == today_str:
                return False

            if last_completed == yesterday_str:
                new_streak = streak + 1
            else:
                new_streak = 1

            self.cursor.execute("""
                UPDATE habits 
                SET streak = ?, last_completed = ? 
                WHERE id = ?
            """, (new_streak, today_str, habit_id))
            self.conn.commit()
            return True

    # --- SEKCOJA ZADAŃ (Teraz poprawnie wysunięta) ---

    def add_task(self, title):
        self.cursor.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        self.conn.commit()

    def get_all_tasks(self):
        self.cursor.execute("SELECT * FROM tasks")
        return self.cursor.fetchall()

    def toggle_task(self, task_id, current_state):
        # Zamiana 0 na 1 lub 1 na 0
        new_state = 1 if current_state == 0 else 0
        self.cursor.execute("UPDATE tasks SET is_done = ? WHERE id = ?", (new_state, task_id))
        self.conn.commit()

    def delete_task(self, task_id):
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()