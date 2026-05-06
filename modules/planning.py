# modules/planning.py
import customtkinter as ctk
from datetime import date, timedelta


class PlanningFrame(ctk.CTkFrame):
    def __init__(self, master, db, **kwargs):
        super().__init__(master, **kwargs)
        self.db = db
        self.selected_date = date.today()  # Domyślnie ustawiamy na dzisiaj
        self.setup_ui()

    def setup_ui(self):
        # Nagłówek z aktualnie wybraną datą
        self.date_label = ctk.CTkLabel(self, text=f"📅 PLAN NA: {self.selected_date}",
                                       font=("Arial", 20, "bold"))
        self.date_label.pack(pady=10)

        # Nawigacja datami
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(pady=5)

        ctk.CTkButton(nav_frame, text="<", width=40, command=lambda: self.change_date(-1)).pack(side="left", padx=5)
        ctk.CTkButton(nav_frame, text="Dziś", width=60, command=self.set_today).pack(side="left", padx=5)
        ctk.CTkButton(nav_frame, text=">", width=40, command=lambda: self.change_date(1)).pack(side="left", padx=5)

        # Dodawanie zadania
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=10, fill="x", padx=20)

        self.task_entry = ctk.CTkEntry(input_frame, placeholder_text="Co planujesz na ten dzień?")
        self.task_entry.pack(side="left", fill="x", expand=True, padx=10, pady=10)

        add_btn = ctk.CTkButton(input_frame, text="Dodaj", command=self.add_task)
        add_btn.pack(side="right", padx=10)

        # Lista zadań
        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="Zadania")
        self.scroll_frame.pack(pady=10, fill="both", expand=True, padx=20)

        self.refresh_list()

    def change_date(self, days):
        self.selected_date += timedelta(days=days)
        self.update_view()

    def set_today(self):
        self.selected_date = date.today()
        self.update_view()

    def update_view(self):
        self.date_label.configure(text=f"📅 PLAN NA: {self.selected_date}")
        self.refresh_list()

    def refresh_list(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # Pobieramy zadania tylko dla wybranego dnia
        tasks = self.db.get_tasks_by_date(str(self.selected_date))
        for t_id, t_title, t_date, t_is_done in tasks:
            row = ctk.CTkFrame(self.scroll_frame)
            row.pack(pady=2, fill="x", padx=5)

            check = ctk.CTkCheckBox(row, text=t_title,
                                    command=lambda i=t_id, s=t_is_done: self.toggle_task(i, s))
            if t_is_done: check.select()
            check.pack(side="left", padx=10, pady=5)

            btn_del = ctk.CTkButton(row, text="Usuń", width=60, fg_color="#aa3333",
                                    command=lambda i=t_id: self.delete_task(i))
            btn_del.pack(side="right", padx=10)

    def add_task(self):
        title = self.task_entry.get()
        if title:
            self.db.add_task(title, str(self.selected_date))
            self.task_entry.delete(0, 'end')
            self.refresh_list()

    def toggle_task(self, task_id, current_state):
        self.db.toggle_task(task_id, current_state)
        self.refresh_list()

    def delete_task(self, task_id):
        self.db.delete_task(task_id)
        self.refresh_list()