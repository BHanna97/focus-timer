import win32gui
import time
from datetime import date
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["focustimer"]

active_time_collection = db["activetime"]

def get_active_window():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())


active_time = 0
start_time = 0

try:
    while True:
        active_window = get_active_window()
        if 'Visual Studio Code' in active_window:
            if start_time == 0:
                start_time = time.time()
        else:
            if start_time != 0:    
                active_time += time.time() - start_time
                start_time = 0
                active_time_collection.update_one(
                    {"window_title": "Visual Studio Code","date": date.today().isoformat()},
                    {"$inc": {"total_active_time_seconds": active_time}},
                    upsert=True
                    )
                active_time = 0
        
        time.sleep(1)




except KeyboardInterrupt:
    if start_time:
        active_time += time.time() - start_time #account for an ongoing session
        active_time_collection.update_one(
                {"window_title": "Visual Studio Code", "date": date.today().isoformat()},
                {"$inc": {"total_active_time_seconds": active_time}},
                upsert=True
                )
    total_time_today = active_time_collection.find_one({"date": date.today().isoformat()})["total_active_time_seconds"]
    print(total_time_today)