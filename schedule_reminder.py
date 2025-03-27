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
        print(f"✅ Reminder '{title}' scheduled successfully for {reminder_time}.")
    except Exception as e:
        print(f"❌ Failed to schedule reminder: {e}")


def verify_reminder_output(text):
    required_keys = ["title: ", "details: ", "start_year: ", "start_month: ", "start_day: ", "start_hour: ", "start_minute: "]
    return all(key in text for key in required_keys)