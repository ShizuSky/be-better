import customtkinter as ctk


class PlanningFrame(ctk.CTkFrame):
    def __init__(self, master, db, **kwargs):
        super().__init__(master, **kwargs)
        self.db = db
        self.setup_ui()

    def setup_ui(self):
        ctk.CTkLabel(self, text="📅 PLAN DNIA", font=("Arial", 24, "bold")).pack(pady=10)

        # Dodawanie zadania
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(pady=10, fill="x", padx=20)

        self.task_entry = ctk.CTkEntry(input_frame, placeholder_text="Co masz do zrobienia?")
        self.task_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        add_btn = ctk.CTkButton(input_frame, text="Dodaj", width=80, command=self.add_task)
        add_btn.pack(side="right")

        # Lista zadań
        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="Lista zadań")
        self.scroll_frame.pack(pady=10, fill="both", expand=True, padx=20)

        self.refresh_list()

    def refresh_list(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        tasks = self.db.get_all_tasks()
        for t_id, t_title, t_is_done in tasks:
            row = ctk.CTkFrame(self.scroll_frame)
            row.pack(pady=5, fill="x", padx=5)

            # Checkbox dla zadania
            check = ctk.CTkCheckBox(row, text=t_title,
                                    command=lambda i=t_id, s=t_is_done: self.toggle_task(i, s))
            if t_is_done:
                check.select()
            check.pack(side="left", padx=10, pady=5)

            # Przycisk usuwania
            btn_del = ctk.CTkButton(row, text="Usuń", width=60, fg_color="#cc3333",
                                    command=lambda i=t_id: self.delete_task(i))
            btn_del.pack(side="right", padx=10)

    def add_task(self):
        title = self.task_entry.get()
        if title:
            self.db.add_task(title)
            self.task_entry.delete(0, 'end')
            self.refresh_list()

    def toggle_task(self, task_id, current_state):
        self.db.toggle_task(task_id, current_state)
        self.refresh_list()

    def delete_task(self, task_id):
        self.db.delete_task(task_id)
        self.refresh_list()