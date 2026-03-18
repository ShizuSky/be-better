import sqlite3
from datetime import date, datetime, timedelta

class Database:
    def __init__(self, db_name="better_me.db"):
        # Połączenie z bazą (plik powstanie automatycznie w folderze projektu)
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Tabela dla nawyków
        # id: unikalny numer
        # name: nazwa nawyku
        # streak: aktualna seria dni
        # last_completed: data ostatniego odhaczenia (format RRRR-MM-DD)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                streak INTEGER DEFAULT 0,
                last_completed TEXT
            )
        ''')
        self.conn.commit()

    def add_habit(self, name):
        """Dodaje nowy nawyk do bazy."""
        self.cursor.execute("INSERT INTO habits (name, streak) VALUES (?, 0)", (name,))
        self.conn.commit()

    def get_all_habits(self):
        """Zwraca listę wszystkich nawyków."""
        self.cursor.execute("SELECT * FROM habits")
        return self.cursor.fetchall()

    def delete_habit(self, habit_id):
        """Usuwa nawyk o podanym ID."""
        self.cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        self.conn.commit()

    def complete_habit(self, habit_id):
        """Logika odhaczania nawyku i zarządzania serią (streak)."""
        today = date.today()
        today_str = str(today)
        yesterday_str = str(today - timedelta(days=1))

        # Pobieramy dane o nawyku
        self.cursor.execute("SELECT streak, last_completed FROM habits WHERE id = ?", (habit_id,))
        habit = self.cursor.fetchone()

        if habit:
            streak, last_completed = habit

            # 1. Jeśli już dzisiaj odhaczone - nic nie rób
            if last_completed == today_str:
                return False

            # 2. Jeśli ostatnio odhaczone wczoraj - zwiększ streak
            if last_completed == yesterday_str:
                new_streak = streak + 1
            # 3. Jeśli przerwa była dłuższa niż 1 dzień - zresetuj do 1
            else:
                new_streak = 1

            self.cursor.execute("""
                UPDATE habits 
                SET streak = ?, last_completed = ? 
                WHERE id = ?
            """, (new_streak, today_str, habit_id))
            self.conn.commit()
            return True