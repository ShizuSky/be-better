# modules/training.py
import customtkinter as ctk
import time
from datetime import date


class TrainingFrame(ctk.CTkFrame):
    def __init__(self, master, db, **kwargs):
        super().__init__(master, **kwargs)
        self.db = db
        self.current_session_id = None
        self.selected_date = date.today()
        self.setup_ui()

    def setup_ui(self):
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        self.tab_today = self.tabview.add("TRENING")
        self.tab_history = self.tabview.add("HISTORIA")
        self.setup_today_tab()
        self.setup_history_tab()

    # --- ZAKŁADKA TRENING ---
    def setup_today_tab(self):
        for widget in self.tab_today.winfo_children(): widget.destroy()

        self.container_today = ctk.CTkFrame(self.tab_today, fg_color="transparent")
        self.container_today.pack(fill="both", expand=True)

        self.start_screen = ctk.CTkFrame(self.container_today, fg_color="transparent")
        self.start_screen.pack(fill="both", expand=True)

        ctk.CTkLabel(self.start_screen, text="NOWA SESJA", font=("Arial", 24, "bold")).pack(pady=60)

        start_btn = ctk.CTkButton(self.start_screen, text="ROZPOCZNIJ TRENING",
                                  fg_color="#D4AF37", text_color="black",
                                  font=("Arial", 18, "bold"), height=60,
                                  command=self.start_new_session)
        start_btn.pack(side="bottom", fill="x", padx=40, pady=40)

    def start_new_session(self):
        self.current_session_id = int(time.time())  # Unikalne ID sesji
        self.start_screen.destroy()
        self.show_active_training_panel()

    def show_active_training_panel(self):
        self.active_frame = ctk.CTkFrame(self.container_today, fg_color="transparent")
        self.active_frame.pack(fill="both", expand=True)

        # GÓRNY PASEK
        top = ctk.CTkFrame(self.active_frame, fg_color="transparent")
        top.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(top, text=f"AKTYWNA SESJA: {self.selected_date}", font=("Arial", 14, "bold")).pack(side="left")
        ctk.CTkButton(top, text="ZAKOŃCZ TRENING", fg_color="#aa3333", command=self.finish_workout).pack(side="right")

        # DODAWANIE NOWEGO ĆWICZENIA DO BAZY (To czego brakowało!)
        manage_frame = ctk.CTkFrame(self.active_frame)
        manage_frame.pack(pady=5, padx=20, fill="x")

        self.new_ex_entry = ctk.CTkEntry(manage_frame, placeholder_text="Wpisz nazwę nowego ćwiczenia...", height=30)
        self.new_ex_entry.pack(side="left", fill="x", expand=True, padx=10, pady=5)

        ctk.CTkButton(manage_frame, text="DODAJ DO BAZY", width=100, height=30,
                      command=self.add_new_exercise_to_db).pack(side="right", padx=10)

        # FORMULARZ SERII
        input_f = ctk.CTkFrame(self.active_frame)
        input_f.pack(pady=10, padx=20, fill="x")

        exs = self.db.get_exercise_list()
        self.ex_choice = ctk.CTkOptionMenu(input_f, values=exs if exs else ["Najpierw dodaj ćwiczenie!"])
        self.ex_choice.grid(row=0, column=0, padx=5, pady=10)

        self.s_ent = ctk.CTkEntry(input_f, placeholder_text="S", width=40)
        self.s_ent.grid(row=0, column=1, padx=2)
        self.r_ent = ctk.CTkEntry(input_f, placeholder_text="R", width=40)
        self.r_ent.grid(row=0, column=2, padx=2)
        self.w_ent = ctk.CTkEntry(input_f, placeholder_text="kg", width=50)
        self.w_ent.grid(row=0, column=3, padx=2)

        ctk.CTkButton(input_f, text="DODAJ", width=60, command=self.add_record).grid(row=0, column=4, padx=5)

        self.scroll_active = ctk.CTkScrollableFrame(self.active_frame, label_text="Aktualna sesja")
        self.scroll_active.pack(fill="both", expand=True, padx=20, pady=10)

    def add_new_exercise_to_db(self):
        """Dodaje nowe ćwiczenie do bazy i odświeża listę wyboru."""
        name = self.new_ex_entry.get()
        if name:
            self.db.cursor.execute("INSERT OR IGNORE INTO exercises (name, category) VALUES (?, ?)", (name, "Własne"))
            self.db.conn.commit()
            self.new_ex_entry.delete(0, 'end')

            # Odświeżamy OptionMenu
            new_list = self.db.get_exercise_list()
            self.ex_choice.configure(values=new_list)
            self.ex_choice.set(name)

    def add_record(self):
        ex = self.ex_choice.get()
        if self.s_ent.get() and self.r_ent.get() and ex != "Najpierw dodaj ćwiczenie!":
            self.db.add_workout_entry(self.current_session_id, ex, int(self.s_ent.get()),
                                      int(self.r_ent.get()), float(self.w_ent.get() or 0), str(self.selected_date))
            self.refresh_active_list()

    def refresh_active_list(self):
        for w in self.scroll_active.winfo_children(): w.destroy()
        details = self.db.get_workout_details(self.current_session_id)
        for name, s, r, w in details:
            ctk.CTkLabel(self.scroll_active, text=f"• {name}: {s}x{r} @ {w}kg", anchor="w").pack(fill="x", padx=10)

    def finish_workout(self):
        self.current_session_id = None
        self.setup_today_tab()
        self.refresh_history()
        self.tabview.set("HISTORIA")

    # --- ZAKŁADKA HISTORIA ---
    def setup_history_tab(self):
        for w in self.tab_history.winfo_children(): w.destroy()
        self.scroll_hist = ctk.CTkScrollableFrame(self.tab_history, fg_color="transparent")
        self.scroll_hist.pack(fill="both", expand=True, padx=10, pady=10)
        self.refresh_history()

    def refresh_history(self):
        for w in self.scroll_hist.winfo_children(): w.destroy()

        history = self.db.get_history_summary()

        for sid, w_date, vol in history:
            card = ctk.CTkFrame(self.scroll_hist, fg_color="#2b2b3d")
            card.pack(fill="x", pady=5)

            header = ctk.CTkFrame(card, fg_color="transparent")
            header.pack(fill="x", padx=10, pady=5)

            ctk.CTkLabel(header, text=f"📅 {w_date}", font=("Arial", 14, "bold")).pack(side="left")
            ctk.CTkLabel(header, text=f"Objętość: {vol or 0}kg", font=("Arial", 11)).pack(side="right")

            # Kontener na szczegóły (domyślnie schowany)
            details_f = ctk.CTkFrame(card, fg_color="#1a1a2e")

            def toggle(f=details_f, s=sid):
                if f.winfo_viewable():
                    f.pack_forget()
                else:
                    f.pack(fill="x", padx=10, pady=5)
                    for widget in f.winfo_children(): widget.destroy()
                    details = self.db.get_workout_details(s)
                    for name, s, r, w in details:
                        ctk.CTkLabel(f, text=f"  └ {name}: {s}x{r} @ {w}kg", anchor="w", font=("Arial", 11)).pack(
                            fill="x")

            ctk.CTkButton(header, text="SZCZEGÓŁY", width=80, height=20, command=toggle).pack(side="right", padx=10)