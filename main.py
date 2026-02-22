import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from datetime import datetime
import csv
import os

from database import DatabaseManager
import bmi_logic
import analytics

class VitalityApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.users = self.db.get_users()
        self.current_user_id = self.users[0][0]

        self.title("BMI-Analytics")
        self.geometry("1000x750")
        ctk.set_appearance_mode("Dark")
        
        self.setup_top_bar()
        
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=10)
        self.tab_dash = self.tabs.add("Dashboard")
        self.tab_data = self.tabs.add("Manage Data & Export")

        self.setup_dashboard_tab()
        self.setup_manage_data_tab()
        self.refresh_all()

    # --- TOP BAR & THEMING ---
    def setup_top_bar(self):
        self.top_frame = ctk.CTkFrame(self, height=50, corner_radius=0)
        self.top_frame.pack(fill="x", side="top", pady=(0, 10))

        ctk.CTkLabel(self.top_frame, text="Active Profile:", font=("Roboto", 14, "bold")).pack(side="left", padx=(20, 10), pady=10)
        
        self.user_var = ctk.StringVar(value=self.users[0][1])
        self.user_menu = ctk.CTkOptionMenu(self.top_frame, values=[u[1] for u in self.users], variable=self.user_var, command=self.switch_user)
        self.user_menu.pack(side="left", padx=10)

        self.add_user_btn = ctk.CTkButton(self.top_frame, text="+ Add Profile", width=100, command=self.create_user)
        self.add_user_btn.pack(side="left", padx=10)

        self.theme_var = ctk.StringVar(value="Dark")
        self.theme_switch = ctk.CTkSwitch(self.top_frame, text="Dark Mode", command=self.toggle_theme, variable=self.theme_var, onvalue="Dark", offvalue="Light")
        self.theme_switch.pack(side="right", padx=20)

    def create_user(self):
        dialog = ctk.CTkInputDialog(text="Enter new profile name:", title="Add Profile")
        new_name = dialog.get_input()
        if new_name and new_name.strip():
            new_name = new_name.strip()
            if self.db.add_user(new_name):
                self.users = self.db.get_users()
                self.user_menu.configure(values=[u[1] for u in self.users])
                self.user_var.set(new_name)
                self.switch_user(new_name)
                messagebox.showinfo("Success", f"Profile '{new_name}' created!")
            else:
                messagebox.showerror("Error", "Profile name already exists.")

    def toggle_theme(self):
        ctk.set_appearance_mode(self.theme_var.get())
        self.refresh_all()

    def switch_user(self, username):
        try:
            self.current_user_id = next(u[0] for u in self.users if u[1] == username)
            self.refresh_all()
        except StopIteration:
            messagebox.showerror("Error", "User profile not found.")

    # --- DASHBOARD TAB ---
    def setup_dashboard_tab(self):
        self.tab_dash.grid_columnconfigure(0, weight=1)
        self.tab_dash.grid_columnconfigure(1, weight=3)
        self.tab_dash.grid_rowconfigure(0, weight=1)

        # Input Panel
        self.input_frame = ctk.CTkFrame(self.tab_dash, corner_radius=15)
        self.input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.input_frame, text="Log Metrics", font=("Roboto", 24, "bold")).pack(pady=(20, 10))

        self.w_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        self.w_frame.pack(pady=10)
        self.weight_entry = ctk.CTkEntry(self.w_frame, placeholder_text="Weight", width=120)
        self.weight_entry.pack(side="left", padx=(0, 5))
        self.weight_unit = ctk.CTkOptionMenu(self.w_frame, values=["kg", "lbs"], width=70)
        self.weight_unit.pack(side="left")

        self.h_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        self.h_frame.pack(pady=10)
        self.height_entry = ctk.CTkEntry(self.h_frame, placeholder_text="Height", width=120)
        self.height_entry.pack(side="left", padx=(0, 5))
        self.height_unit = ctk.CTkOptionMenu(self.h_frame, values=["m", "cm", "ft'in"], width=70)
        self.height_unit.set("ft'in")
        self.height_unit.pack(side="left")

        self.calc_btn = ctk.CTkButton(self.input_frame, text="Save Data", command=self.process_entry)
        self.calc_btn.pack(pady=20)

        self.result_label = ctk.CTkLabel(self.input_frame, text="BMI: -- \nCategory: --", font=("Roboto", 18))
        self.result_label.pack(pady=20)

        # Chart Panel
        self.chart_frame = ctk.CTkFrame(self.tab_dash, corner_radius=15)
        self.chart_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.figure = plt.Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        self.stat_label = ctk.CTkLabel(self.tab_dash, text="Stats loading...", font=("Roboto", 14))
        self.stat_label.grid(row=1, column=0, columnspan=2, pady=10)

    # --- MANAGE DATA TAB ---
    def setup_manage_data_tab(self):
        self.tab_data.grid_columnconfigure(0, weight=1)

        self.history_scroll = ctk.CTkScrollableFrame(self.tab_data, label_text="Your History (Saved in Metric)")
        self.history_scroll.pack(fill="both", expand=True, padx=20, pady=20)

        self.export_btn = ctk.CTkButton(self.tab_data, text="Export to CSV", command=self.export_to_csv, fg_color="green")
        self.export_btn.pack(pady=10)

    # --- LOGIC & REFRESH ---
    def process_entry(self):
        w_str, w_unit = self.weight_entry.get(), self.weight_unit.get()
        h_str, h_unit = self.height_entry.get(), self.height_unit.get()
        
        is_valid, err, w_kg, h_m = bmi_logic.validate_inputs(w_str, w_unit, h_str, h_unit)
        if not is_valid:
            messagebox.showerror("Validation Error", err)
            return

        bmi = bmi_logic.calculate_bmi(w_kg, h_m)
        cat = bmi_logic.categorize_bmi(bmi)
        self.result_label.configure(text=f"BMI: {bmi}\nCategory: {cat}")

        if self.db.add_entry(self.current_user_id, w_kg, h_m, bmi, cat):
            self.refresh_all()
            self.weight_entry.delete(0, 'end')
            self.height_entry.delete(0, 'end')

    def delete_record(self, record_id):
        if messagebox.askyesno("Confirm", "Delete this record forever?"):
            self.db.delete_entry(record_id)
            self.refresh_all()

    def export_to_csv(self):
        data = self.db.get_history(self.current_user_id)
        if not data:
            messagebox.showinfo("Export", "No data to export.")
            return
            
        filename = f"bmi_export_{self.user_var.get()}_{datetime.now().strftime('%Y%m%d')}.csv"
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Date", "Weight(kg)", "Height(m)", "BMI", "Category"])
            writer.writerows(data)
        
        messagebox.showinfo("Success", f"Data exported to {os.path.abspath(filename)}")

    def refresh_all(self):
        data = self.db.get_history(self.current_user_id)
        
        # 1. Chart Update
        self.ax.clear()
        
        text_color = "white" if self.theme_var.get() == "Dark" else "black"
        bg_color = "#2b2b2b" if self.theme_var.get() == "Dark" else "#ebebeb"
        self.figure.patch.set_facecolor(bg_color)
        self.ax.set_facecolor(bg_color)
        self.ax.tick_params(colors=text_color)
        self.ax.xaxis.label.set_color(text_color)
        self.ax.yaxis.label.set_color(text_color)

        if data:
            dates = [datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S") for row in data]
            bmis = [row[4] for row in data]
            
            self.ax.plot(dates, bmis, marker='o', color='#1f538d', linewidth=2, label="BMI", zorder=3)
            
            ma = bmi_logic.calculate_moving_average(bmis, window=3)
            if len(dates) >= 3:
                self.ax.plot(dates, ma, color='orange', linestyle='--', linewidth=2, label="3-Pt Avg", zorder=4)

            self.ax.scatter([dates[-1]], [bmis[-1]], color='red', s=100, label="Latest", zorder=5)
            self.ax.axhspan(18.5, 24.9, alpha=0.2, color='green', zorder=1)
            
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
            self.figure.autofmt_xdate()
            self.ax.set_ylabel('BMI')
            self.ax.grid(True, linestyle='--', alpha=0.3)
            self.ax.legend(loc='upper right')
        else:
            self.ax.text(0.5, 0.5, "No Data", ha='center', va='center', color=text_color)
        
        self.figure.tight_layout()
        self.canvas.draw()

        # 2. Stats Update
        stats = analytics.generate_stats(data)
        self.stat_label.configure(text=f"Total Entries: {stats['total']} | Avg BMI: {stats['avg_bmi']} | Trend: {stats['trend']}")

        # 3. History Tab Update
        for widget in self.history_scroll.winfo_children():
            widget.destroy()

        for row in reversed(data):
            rec_id, date, w, h, bmi, cat = row
            frame = ctk.CTkFrame(self.history_scroll)
            frame.pack(fill="x", pady=5, padx=5)
            
            lbl = ctk.CTkLabel(frame, text=f"{date[:10]} | W: {w}kg | BMI: {bmi} ({cat})")
            lbl.pack(side="left", padx=10, pady=5)
            
            del_btn = ctk.CTkButton(frame, text="Delete", width=60, fg_color="red", command=lambda r=rec_id: self.delete_record(r))
            del_btn.pack(side="right", padx=10, pady=5)

if __name__ == "__main__":
    app = VitalityApp()
    app.mainloop()