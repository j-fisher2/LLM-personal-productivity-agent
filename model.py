import requests
import webbrowser
import time
from schedule_event import schedule_event, verify_scheduling_output
from dotenv import load_dotenv
import os

load_dotenv()

def get_google_search_url(query):
    return f"https://www.google.com/search?q={query.replace(' ', '+')}"

while True:
    print("Message: ",end="")
    command = input("")

    url = os.getenv("LLM_ENDPOINT")
    data = {
        "model": "mistral",
        "prompt": f"""

    You are a virtual assistant capable of performing **system actions**. 
    Your task is to **clearly indicate when an action is required** by following these rules:

    ✅ **Action Format:**  
    - If the user asks to open, launch, or visit a website, **always respond with:**  
        ACTION: Opening [component_name] where the component_name is a website in proper format.
    - If the component is unknown, simulate it by saying:  
        ACTION: Attempting to open [component_name]
    - If the user asks you to search for something or to find something **always respond with:**
        ACTION: Searching [component_name] where the component_name is their query and it is properly formatted for google searches without `for` as a prefix.
    - If the user asks you to schedule an event or meeting, make sure that the user provides an event name, an event location, a start year, a start month, a start day, a start hour and a start minute and **always respond with:**:
        ACTION: Scheduling your event with the following fields - [component_name] where the component_name is a JSON object of all the fields you have extracted from the query. If minutes are not provided they are set to 0. If a year is not provided you may assume the year is 2025 and just place 2025 in the response with no other details. If an event name is not provided, assume it is the same as the location and just place it in the response with no other details. **always** use commas to seperate the fields. **do not** add any additional output or comments to your response and always format it exactly as in the examples below.

    🚫 **No Action Format:**  
    - If the request **does not** require opening something or retrieving a query response, or to schedule a meeting or event, respond with:  
        NO_ACTION: [your helpful response]

    ---

    🔧 **Examples:**  
    - "Open Google Chrome" → ACTION: Opening google.com  
    - "Launch Spotify.com" → ACTION: Opening spotify.com  
    - "Go to GitHub" → ACTION: Opening github.com 
    - "open youtube for me" → ACTION: Opening youtube.com
    - "What's the capital of France?" → NO_ACTION: The capital of France is Paris.  
    - "What's the weather like?" → NO_ACTION: It's 25°C and sunny.
    - "Tell me a joke" → NO_ACTION: Why don't scientists trust atoms? Because they make up everything!
    - "Find good restaurants near me" → ACTION: Searching `good restaurants near you`
    - "Search for things to do in Toronto" → ACTION: Searching `things to do in Toronto`
    - "What can i do at Canada's wonderland?" → ACTION: Searching `things to do at Canada's wonderland`
    - "what can I do when going to India next year?" → ACTION: Searching `things to do in india`
    - "find me a good movie to watch" → ACTION: Searching `good movies to watch`
    - "Schedule a meeting for me called starbucks_meeting on March 25, 2025 at 10:15AM at Starbucks lasting 20 minutes" 
    → ACTION: Scheduling your meeting meeting with the following fields - location: Starbucks, start_year: 2025, start_month: 3, start_day: 25, start_hour: 10, start_minute: 15, duration_minutes: 20 

    - "Schedule a meeting on April 5, 2025 at 2:20PM at Microsoft lasting 35 minutes" 
    → ACTION: Scheduling your meeting with the following fields - 
        event_name: MeetingAtMicrosoft
        location: Harry HQ,
        start_year: 2025,
        start_month: 4,
        start_day: 5,
        start_hour: 14,
        start_minute: 20,
        duration_minutes: 35
    - "Schedule a meeting on April 5 at 2:20PM at Harry HQ lasting 35 minutes" 
    → ACTION: Scheduling your event with the following fields - 
        event_name: MeetingAtHarryHQ,
        location: Harry HQ,
        start_year: 2025,
        start_month: 4,
        start_day: 5,
        start_hour: 14,
        start_minute: 20,
        duration_minutes: 35


    Now, respond to this command:  
    **{command}**
    """,
        "stream": False
    }
    response = requests.post(url, json=data)

    if response.status_code != 200:
        print(f"Error: {response.status_code}", response.text)
        exit()

    result = response.json().get("response", "")
    print(result)
    time.sleep(2)
    if "ACTION: Opening" in result or "ACTION: Attempting to open" in result:
        component = result.split("Opening")[-1].strip()

        if "." in component: 
            webbrowser.open(f"https://{component}")
    
    elif "ACTION: Searching" in result:
        query = result.split("Searching")[-1].replace("`","").strip()
        webbrowser.open(get_google_search_url(query))

    elif "ACTION: Scheduling" in result:
        keywords = result.split("-")[1].strip()
        if "," in keywords:
            result = result.replace("\n","")
            keywords = [word.strip() for word in keywords.split(",")]
        else:
            keywords = [word.strip() for word in keywords.split("\n")]
        values = []
        for idx, metric in enumerate(keywords):
            values.append(metric.split(" ")[1])

        confirmation = input("Is this correct? y/n: ")
        if confirmation in ("Yes", "yes", "y") and verify_scheduling_output(result):
            schedule_event(values[0],values[1],int(values[2]), int(values[3]), int(values[4]),int(values[5]),int(values[6]),int(values[7]))
        else:
            print("There was an error in the scheduling format, please try again.")