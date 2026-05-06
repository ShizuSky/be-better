import customtkinter as ctk


class HabitTrackerFrame(ctk.CTkFrame):
    def __init__(self, master, db, **kwargs):
        super().__init__(master, **kwargs)
        self.db = db  # Przekazujemy dostęp do bazy danych
        self.setup_ui()

    def setup_ui(self):
        # Nagłówek
        ctk.CTkLabel(self, text="🔥 TWOJE NAWYKI", font=("Arial", 24, "bold")).pack(pady=10)

        # Panel dodawania
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(pady=10, fill="x", padx=20)

        self.habit_entry = ctk.CTkEntry(input_frame, placeholder_text="Nowy nawyk...")
        self.habit_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        add_btn = ctk.CTkButton(input_frame, text="Dodaj", width=80, command=self.add_habit)
        add_btn.pack(side="right")

        # Przewijalna lista
        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="Lista nawyków")
        self.scroll_frame.pack(pady=10, fill="both", expand=True, padx=20)

        self.refresh_list()

    def refresh_list(self):
        # Czyścimy starą listę przed przeładowaniem
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        habits = self.db.get_all_habits()
        for h_id, h_name, h_streak, h_last in habits:
            row = ctk.CTkFrame(self.scroll_frame)
            row.pack(pady=5, fill="x", padx=5)

            # Wyświetlamy nawyk i streak
            label = ctk.CTkLabel(row, text=f"{h_name} (Seria: {h_streak} 🔥)")
            label.pack(side="left", padx=10)

            # Przycisk do odhaczania
            btn_done = ctk.CTkButton(row, text="Zrobione!", width=70,
                                     command=lambda i=h_id: self.mark_done(i))
            btn_done.pack(side="right", padx=5, pady=5)

            # Przycisk usuwania
            btn_del = ctk.CTkButton(row, text="X", width=30, fg_color="red", hover_color="#880000",
                                    command=lambda i=h_id: self.delete_habit(i))
            btn_del.pack(side="right", padx=5)

    def add_habit(self):
        name = self.habit_entry.get()
        if name:
            self.db.add_habit(name)
            self.habit_entry.delete(0, 'end')
            self.refresh_list()

    def mark_done(self, habit_id):
        self.db.complete_habit(habit_id)
        self.refresh_list()

    def delete_habit(self, habit_id):
        self.db.delete_habit(habit_id)
        self.refresh_list()