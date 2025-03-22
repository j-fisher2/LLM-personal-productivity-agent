import requests
import webbrowser
import time
from .schedule_event import schedule_event

#schedule_event(event_name, location, 2025, 3, 25, 10, 0, duration_minutes, calendar_name="Work")

def get_google_search_url(query):
    return f"https://www.google.com/search?q={query.replace(' ', '+')}"

while True:
    print("Message: ",end="")
    command = input("")

    url = "http://localhost:11434/api/generate"
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

    🚫 **No Action Format:**  
    - If the request **does not** require opening something or retrieving a query response, respond with:  
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

    ---

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
