import subprocess
from datetime import datetime, timedelta

def schedule_event(event_name, location, start_time_year, start_time_month, start_time_day, start_time_hour, start_time_minute, duration_minutes, start_time_second = 0, calendar_name="Work"):

    start_time = datetime(start_time_year, start_time_month, start_time_day, start_time_hour, start_time_minute, start_time_second)
    
    end_time = start_time + timedelta(minutes=duration_minutes)

    start_str = start_time.strftime("%A, %B %d, %Y at %I:%M:%S %p")
    end_str = end_time.strftime("%A, %B %d, %Y at %I:%M:%S %p")

    script = (
        'tell application "Calendar"\n'
        '    tell calendar "' + calendar_name + '"\n'
        '        make new event with properties {summary:"' + event_name + '", location:"' + location + '", start date:(date "' + start_str + '"), end date:(date "' + end_str + '")}\n'
        '    end tell\n'
        'end tell'
    )

    process = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)

    if process.returncode == 0:
        print(f"✅ Event '{event_name}' scheduled successfully!")
    else:
        print(f"❌ Failed to schedule event.")


def verify_scheduling_output(text):
    required_keys = ["location: ", "start_year: ", "start_month: ", "start_day: ", "start_hour: ", "start_minute: ", "duration_minutes: ", "event_name: "]
    return all(key in text for key in required_keys) 