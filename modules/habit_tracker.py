import time
from datetime import datetime
import customtkinter as ctk


class HabitTrackerFrame(ctk.CTkFrame):

    def __init__(self, master, db, **kwargs):
        super().__init__(master, **kwargs)
        self.db = db
        self.active_counters = (
            []
        )
        self.setup_ui()

    def setup_ui(self):
        ctk.CTkLabel(
            self, text="🔥 TWOJE NAWYKI", font=("Arial", 24, "bold")
        ).pack(pady=10)

        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(pady=10, fill="x", padx=20)

        self.habit_entry = ctk.CTkEntry(
            input_frame, placeholder_text="Nowy nawyk..."
        )
        self.habit_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        add_btn = ctk.CTkButton(
            input_frame, text="Dodaj", width=80, command=self.add_habit
        )
        add_btn.pack(side="right")

        self.scroll_frame = ctk.CTkScrollableFrame(
            self, label_text="Lista nawyków"
        )
        self.scroll_frame.pack(pady=10, fill="both", expand=True, padx=20)

        self.refresh_list()

    def refresh_list(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.active_counters.clear()

        habits = self.db.get_all_habits()
        for h_id, h_name, h_streak, h_last in habits:
            row = ctk.CTkFrame(self.scroll_frame)
            row.pack(pady=5, fill="x", padx=5)

            name_label = ctk.CTkLabel(
                row, text=f"{h_name}", font=("Arial", 14, "bold")
            )
            name_label.pack(side="left", padx=10)

            time_label = ctk.CTkLabel(row, text="00:00:00", text_color="gray")
            time_label.pack(side="left", padx=10)

            try:
                if h_last:
                    dt = datetime.strptime(h_last, "%Y-%m-%d %H:%M:%S")
                    start_time = dt.timestamp()
                else:
                    start_time = time.time()
            except ValueError:
                start_time = (
                    time.time()
                )

            self.active_counters.append(
                {"label": time_label, "start_time": start_time}
            )


            btn_del = ctk.CTkButton(
                row,
                text="X",
                width=30,
                fg_color="red",
                hover_color="#880000",
                command=lambda i=h_id: self.delete_habit(i),
            )
            btn_del.pack(side="right", padx=5, pady=5)


            btn_reset = ctk.CTkButton(
                row,
                text="Reset",
                width=70,
                fg_color="#f39c12",
                hover_color="#d35400",
                command=lambda i=h_id: self.reset_habit(i),
            )
            btn_reset.pack(side="right", padx=5)

    def update_all_counters(self):
        now = time.time()

        for counter in self.active_counters:
            elapsed = int(now - counter["start_time"])

            if elapsed < 0:
                elapsed = 0


            seconds = elapsed % 60
            minutes = (elapsed // 60) % 60
            hours = elapsed // 3600


            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            counter["label"].configure(text=f"Od startu: {time_str}")


    def add_habit(self):
        name = self.habit_entry.get()
        if name:
            self.db.add_habit(name)
            self.habit_entry.delete(0, "end")
            self.refresh_list()

    def reset_habit(self, habit_id):
        self.db.complete_habit(habit_id)
        self.refresh_list()

    def delete_habit(self, habit_id):
        self.db.delete_habit(habit_id)
        self.refresh_list()