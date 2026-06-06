import customtkinter as ctk
from database import Database
from modules.habit_tracker import HabitTrackerFrame
from modules.planning import PlanningFrame
from modules.training import TrainingFrame

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.db = Database()

        self.title("Be-Better")
        self.geometry("900x600")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.habit_module = None


        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="SAMOROZWÓJ",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        self.btn_planowanie = ctk.CTkButton(
            self.sidebar_frame,
            text="Planowanie Dnia",
            command=self.show_planowanie,
        )
        self.btn_planowanie.grid(row=1, column=0, padx=20, pady=10)

        self.btn_trening = ctk.CTkButton(
            self.sidebar_frame, text="Moduł Treningu", command=self.show_trening
        )
        self.btn_trening.grid(row=2, column=0, padx=20, pady=10)

        self.btn_habits = ctk.CTkButton(
            self.sidebar_frame, text="Habit Tracker", command=self.show_habits
        )
        self.btn_habits.grid(row=3, column=0, padx=20, pady=10)

        self.main_content = ctk.CTkFrame(self, corner_radius=15)
        self.main_content.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.content_label = ctk.CTkLabel(
            self.main_content,
            text="Witaj! Wybierz moduł z lewej strony.",
            font=ctk.CTkFont(size=16),
        )
        self.content_label.pack(pady=50)


        self.global_update_counters()

    def clear_frame(self):

        self.habit_module = None
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def show_planowanie(self):
        self.clear_frame()
        self.planning_module = PlanningFrame(
            self.main_content, self.db, fg_color="transparent"
        )
        self.planning_module.pack(fill="both", expand=True)

    def show_trening(self):
        self.clear_frame()
        self.training_module = TrainingFrame(
            self.main_content, self.db, fg_color="transparent"
        )
        self.training_module.pack(fill="both", expand=True)

    def show_habits(self):
        self.clear_frame()
        self.habit_module = HabitTrackerFrame(
            master=self.main_content, db=self.db, fg_color="transparent"
        )
        self.habit_module.pack(fill="both", expand=True)

    def global_update_counters(self):

        if self.habit_module and hasattr(
            self.habit_module, "update_all_counters"
        ):
            self.habit_module.update_all_counters()

        self.after(1000, self.global_update_counters)


if __name__ == "__main__":
    app = App()
    app.mainloop()