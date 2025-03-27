import subprocess
from datetime import datetime

def schedule_reminder(title: str, body: str, reminder_year, reminder_month, reminder_day, reminder_hour, reminder_minute):
    try:
        reminder_time = datetime(reminder_year, reminder_month, reminder_day, reminder_hour, reminder_minute)
        apple_script = f'''
        tell application "Reminders"
            set newReminder to make new reminder with properties {{name:"{title}", body:"{body}", due date:date "{reminder_time.strftime('%A, %B %d, %Y %I:%M %p')}" }}
        end tell
        '''
        subprocess.run(["osascript", "-e", apple_script], check=True)
        print(f"Reminder '{title}' scheduled successfully for {reminder_time}.")
    except Exception as e:
        print(f"Failed to schedule reminder: {e}")

schedule_reminder("Meeting with John", "Discuss project updates.", 2025, 3, 28, 9,30)