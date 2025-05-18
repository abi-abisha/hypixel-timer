import requests
from datetime import datetime, timedelta
import time
import csv
# r = requests.get('https://api.mojang.com/users/profiles/minecraft/Slimyslimy')

# print(r.text)
# d = r.json()
# print(d)
# https://developer.hypixel.net/dashboard
api_key = "" # hypixel key
Fl0of = "ccf434d6004444f0a275adf229269fc1"
slimyslimy = "6ae06bc2a45a4c12afcd4fba49a4b404"
# r = requests.get(f'https://api.hypixel.net/v2/player?key={api_key}&uuid={Fl0of}')

# d = r.json()
# "lastLogin": 1745238978307,
# "lastLogout": 1745239404641,
# player = d["player"]
# lastLogin = int(player["lastLogin"]) / 1000
# lastLogout = int(player["lastLogout"]) / 1000

# me
lastLogin = 1745272331158 / 1000
# lastLogin = 1745364420
lastLogout =1745271406060 / 1000
# chris
# lastLogin = 1745238978307 / 1000
# lastLogout =1745239404641 / 1000
print(f"lastLogin: {lastLogin}")
print(f"lastLogout: {lastLogout}")

# if you encounter a "year is out of range" error the timestamp
# may be in milliseconds, try `ts /= 1000` in that case
loginDT = datetime.fromtimestamp(lastLogin)
logoutDT = datetime.fromtimestamp(lastLogout)
print(loginDT.strftime('%Y-%m-%d %H:%M:%S'))
print(logoutDT.strftime('%Y-%m-%d %H:%M:%S'))

now = datetime.now()
print(now.strftime('%Y-%m-%d %H:%M:%S'))

# if lastLogin < lastLogout:
#     print("currently offline")
# else:
#     print("currently online")
print("⬛️🟩🟥🟨⬇️⭐🟪")
# ⬛️🟩🟥🟨⬇️⭐🟪
# list of lists with inner lists having login and logout time in unix
# activity = [[1745238978307, 1745239404641], [1745272331158]]
activity = [[1745228078307, 1745239404641], [1745315331158]] # madeup/testing numbers  
# [1745272331158] [1745315331158]
grid = [["⬛️" for _ in range(7)] for _ in range(24)]
def display_grid():
    star = "⭐"
    # current_day =[" ", " ", " ", " ", " ", " ", " "]
    current_day =["S", "M", "T", "W", "T", "F", "S"]
    day_labels = ["S", "M", "T", "W", "T", "F", "S"]
    nowCol = datetime.now().weekday()
    day = {0: 1, 1: 2, 2: 3, 3:4, 4: 5, 5: 6, 6: 0}
    for i in range(0,7):
        if i < day[nowCol]:
            current_day[i] = " "
        elif i > day[nowCol]:
            day_labels[i] = " "
    current_day[day[nowCol]] = star
    print("        " + "     ".join(current_day))
    print("         " + "     ".join(day_labels))
    for hour in range(24):
        print(f"{str(hour).zfill(2)}:00 {grid[hour]}")
# display_grid()
def populate_online_times(activity):
    day = {0: 1, 1: 2, 2: 3, 3:4, 4: 5, 5: 6, 6: 0}
    print("populate")
    print(activity)
    for times in activity:
        lastLogin = times[0] / 1000
        loginDT = datetime.fromtimestamp(lastLogin)
        colLogin = day[loginDT.weekday()]
        # is 2 if login<logout; is 1 if login>logout
        if len(times) == 2:
            print("==============2===========")
            lastLogout = times[1] / 1000
            logoutDT = datetime.fromtimestamp(lastLogout)
            print(loginDT)
            print(logoutDT)
            print(loginDT.hour)
            print(logoutDT.hour)
            print(colLogin)
            colLogout = day[logoutDT.weekday()]
            print(colLogout)
            if colLogin != colLogout:
                for hour in range(loginDT.hour, 24):
                    grid[hour][colLogin] = "🟪"
                # assumed not logged on for more than 1 day
                for hour in range(0, logoutDT.hour+1):
                    grid[hour][colLogout] = "🟪"
            else:
                for hour in range(loginDT.hour, logoutDT.hour+1):
                    grid[hour][colLogin] = "🟩"
        elif len(times) == 1:
            print("=============1==============")
            nowDT = datetime.now() 
            print(loginDT)
            print(nowDT)
            print(loginDT.hour)
            print(nowDT.hour)
            print(colLogin)
            colNow = day[nowDT.weekday()]
            print(colNow)
            if colLogin != colNow:
                for hour in range(loginDT.hour, 24):
                    grid[hour][colLogin] = "🟥"
                # assumed not logged on for more than 1 day
                for hour in range(0, nowDT.hour+1):
                    grid[hour][colNow] = "🟥"
            else:
                for i in range(loginDT.hour, nowDT.hour+1):
                    grid[i][colLogin] = "🟨"

def load_times_csv():
    '''
    1745228078307,1745239404641
    1745315331158
    1745238978307,1745239404641
    1745272331158
    '''
    l = []
    with open("activity.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            row = list(map(int, row))
            l.append(row)
    return l

def create_times_csv():
    lastLogin, lastLogout = get_skyblock_info()
    if lastLogin == -1:
        return -1
    curr = load_times_csv()
    with open("activity.csv", "w", newline="") as f:
        writer = csv.writer(f)
        if lastLogin < lastLogout:
            print("currently offline")
            newRow = [(lastLogin), (lastLogout)]
        else:
            print("currently online")
            newRow = [(lastLogin)]
        # check if info new or old
        print(curr[len(curr)-1], newRow)
        if len(curr) > 0 and curr[len(curr)-1] != newRow:
            print("newinfo")
            # remove last row if previously online and currently offline
            if len(curr[len(curr)-1]) == 1 and len(newRow) == 2:
                curr.pop()
            curr.append(newRow)
        else:
            print("notnew")
            
        writer.writerows(curr)
    return 0

def get_skyblock_info():
    r = requests.get(f'https://api.hypixel.net/v2/player?key={api_key}&uuid={Fl0of}')
    d = r.json()
    if d["success"] == False:
        print(f"failure bc: {d["cause"]}")
        return -1, -1
    player = d["player"]
    lastLogin = int(player["lastLogin"])
    lastLogout = int(player["lastLogout"])
    # lastLogin = 1745353620007
    # lastLogout =1745364420008
    print(lastLogin)
    print(lastLogout)
    return lastLogin, lastLogout

def activity_last_week(activity):
    last_week = []
    # day1 = datetime.fromtimestamp(1745380800).date()  # 20250423 00:00:00
    # day2 = datetime.fromtimestamp(1744776000).date()  # 20250416 00:00:00
    # day2 = datetime.fromtimestamp(1744779600).date()  # 20250416 01:00:00
    # day2 = datetime.fromtimestamp(1744862399).date() # 20250416 23:59:59
    # day2 = datetime.fromtimestamp(1744862400).date() # 20250417 00:00:00
    # day2 = datetime.fromtimestamp(1744862401).date() # 20250417 00:00:01
    now = datetime.now().date()
    # print((day1-day2).days)
    # print((now-day2).days)
    for times in activity:
        lastLogin = times[0] / 1000
        # print(lastLogin)
        loginDT = datetime.fromtimestamp(lastLogin).date()
        print(loginDT)
        if (now-loginDT).days < 7:
            print("within last week")
            last_week.append(times)
        else:
            print("not within last week")
    return last_week

# create_times_csv()
# l = load_times_csv()
# print(l)
# last_week = activity_last_week(l)
# populate_online_times(last_week)
# display_grid()
# t=[[1744776000006,1744862399002],[1744862400003,1744866000005]]
# print(activity_last_week(t))
'''
actual chris times
1745238978307,1745239404641
1745373628663,1745381576115
'''

try:
    while True:
        fail = create_times_csv()
        if fail == -1:
            break
        l = load_times_csv()
        print(l)
        last_week = activity_last_week(l)
        populate_online_times(last_week)
        display_grid()
        seconds = 1200 # 300 wait 5 mins, 1200 wait 20 mins
        print("//////////////////")
        print(f"now {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"waiting {seconds} sec")
        print("//////////////////")
        time.sleep(seconds) 
finally:
    print("stopped program")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))