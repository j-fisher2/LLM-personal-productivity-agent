import subprocess
from datetime import datetime

def schedule_reminder(title: str, body: str, remind_time: str):
    try:
        remind_datetime = datetime.strptime(remind_time, "%Y-%m-%d %H:%M")
        apple_script = f'''
        tell application "Reminders"
            set newReminder to make new reminder with properties {{name:"{title}", body:"{body}", due date:date "{remind_datetime.strftime('%A, %B %d, %Y %I:%M %p')}" }}
        end tell
        '''
        subprocess.run(["osascript", "-e", apple_script], check=True)
        print(f"Reminder '{title}' scheduled successfully for {remind_datetime}.")
    except Exception as e:
        print(f"Failed to schedule reminder: {e}")

schedule_reminder("Meeting with John", "Discuss project updates.", "2025-03-28 09:30")