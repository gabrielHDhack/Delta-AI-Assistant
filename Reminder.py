import tkinter as tk
from tkinter import Label, Entry, Button
from datetime import datetime
import winsound  


class ReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reminder App")
        self.reminders = {}

        self.task_label = Label(root, text="Task:")
        self.task_label.grid(row=0, column=0, padx=10, pady=10)

        self.task_entry = Entry(root)
        self.task_entry.grid(row=0, column=1, padx=10, pady=10)

        self.date_time_label = Label(root, text="Date/Time (Format: day/month/year hour:minute AM/PM):")
        self.date_time_label.grid(row=1, column=0, padx=10, pady=10)

        self.date_time_entry = Entry(root)
        self.date_time_entry.grid(row=1, column=1, padx=10, pady=10)

        self.add_button = Button(root, text="Add Reminder", command=self.add_reminder)
        self.add_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.reset_button = Button(root, text="Reset Reminder", command=self.reset_reminder)
        self.reset_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        self.reset_button.grid_remove()

        self.time_label = Label(root, text="", font=("Arial", 20))
        self.time_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.update_time_label()

    def add_reminder(self):
        task = self.task_entry.get()
        date_time = self.date_time_entry.get()
        try:
            date_time = self.parse_datetime(date_time)
            if date_time:
                self.reminders[task] = date_time
                self.task_entry.delete(0, 'end')
                self.date_time_entry.delete(0, 'end')
                self.task_label.grid_remove()
                self.task_entry.grid_remove()
                self.date_time_label.grid_remove()
                self.date_time_entry.grid_remove()
                self.add_button.grid_remove()
                self.reset_button.grid()
        except ValueError:
            print("Invalid date/time format. Use the format: day/month/year hour:minute AM/PM")

    def reset_reminder(self):
        self.task_label.grid()
        self.task_entry.grid()
        self.date_time_label.grid()
        self.date_time_entry.grid()
        self.add_button.grid()
        self.reset_button.grid_remove()
        self.time_label.config(text="")

    def update_time_label(self):
        now = datetime.now()
        current_time = now.strftime("")

        reminders_to_remove = []

        for task, date_time in self.reminders.items():
            remaining_time = date_time - now

            if remaining_time.total_seconds() <= 0:
                self.play_sound()
                reminders_to_remove.append(task)
            else:
                days = remaining_time.days
                seconds = remaining_time.seconds
                hours, seconds = divmod(seconds, 3600)
                minutes, seconds = divmod(seconds, 60)
                time_str = f"{days}D, {hours}H:{minutes}M:{seconds}S until your task"
                self.time_label.config(text=current_time + "\n" + time_str)

        for task in reminders_to_remove:
            del self.reminders[task]

        self.root.after(1000, self.update_time_label)

    def parse_datetime(self, datetime_str):
        datetime_formats = ["%d/%m/%Y %I:%M %p", "%d/%m/%Y %H:%M"]
        for format_str in datetime_formats:
            try:
                return datetime.strptime(datetime_str, format_str)
            except ValueError:
                pass
        return None

    def play_sound(self):
        sound_file = r"C:\DeltaAI1\mixkit-alert-alarm-1005.wav"
        winsound.PlaySound(sound_file, winsound.SND_FILENAME)

def main():
    root = tk.Tk()
    app = ReminderApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
