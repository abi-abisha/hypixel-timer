import boto3
from boto3.dynamodb.conditions import Key
import os, json
from datetime import datetime, timedelta
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import pytz 
from decimal import Decimal

def lambda_handler(event, context):
    embed = build_timetable()
    print(embed)
    print(embed[0]["description"])
    # signature = event['headers'].get('x-signature-ed25519')
    # timestamp = event['headers'].get('x-signature-timestamp')
    # body = event['body']

    # if not verify_signature(signature, timestamp, body):
    #     print("invalid request signature")
    #     return {
    #         "statusCode": 401,
    #         "body": "invalid request signature"
    #     }

    # data = json.loads(body)

    # if data["type"] == 1:
    #     # PING from Discord
    #     print("ping")
    #     return {
    #         "statusCode": 200,
    #         "body": json.dumps({"type": 1})
    #     }
    # print("-------")
    # if data["type"] == 2:
    #     # Slash command
    #     print("slash command")
    #     if data["data"]["name"] == "timetable":
    #         print("timetable")
    #         embed = build_timetable()
    #         # print(embed)
    #         print(embed[0]["description"])

    #         return {
    #             "statusCode": 200,
    #             "body": json.dumps({
    #                 "type": 4,  # Channel message with source
    #                 "data": {
    #                     "embeds": embed
    #                 }
    #             })
    #         }
        
    print("unhandled")
    return {
        "statusCode": 400,
        "body": "unhandled"
    }
    
# @discord.command()
def timetable(ctx):
    embed = build_timetable()
    return {
        "type": 4,
        "data": {
            "embeds": embed
        }
    }

def build_timetable():
    # ⬛️🟩🟥🟨⬇️⭐🟪
    intervals = generate_intervals()
    grid = build_schedule_matrix()

    star = "⭐"
    current_day =[" ", " ", " ", " ", " ", " ", " "]
    previous_week =["S", "M", "T", "W", "T", "F", "S"]
    current_week = ["S", "M", "T", "W", "T", "F", "S"]
    now = datetime.now(pytz.timezone("US/Eastern"))
    nowCol = now.weekday()
    day = {0: 1, 1: 2, 2: 3, 3:4, 4: 5, 5: 6, 6: 0}
    for i in range(0,7):
        if i < day[nowCol]:
            previous_week[i] = " "
        elif i > day[nowCol]:
            current_week[i] = " "
    previous_week[day[nowCol]] = star
    current_day[day[nowCol]] = now.strftime('%m-%d')

    # Build timetable text block
    timetable_text = ""
    timetable_text += "       " + "   ".join(current_day) + "\n"
    # previous week labels, includes star for current day
    timetable_text += "       " + "   ".join(previous_week) + "\n"
    # timetable_text += now.strftime('%m-%d') + "  " + "   ".join(previous_week) + "\n"
    # current week labels
    timetable_text += "       " + "   ".join(current_week) + "\n"
    
    # last_week_activity = get_last_week_items()
    print("fuck")
    last_week_activity = [{'end_time': Decimal('1745413406169'), 'id': Decimal('0'), 'start_time': Decimal('1745404807233')}, {'end_time': Decimal('1745438248248'), 'id': Decimal('0'), 'start_time': Decimal('1745436907936')}, {'end_time': Decimal('1745458669159'), 'id': Decimal('0'), 'start_time': Decimal('1745446690450')}, {'end_time': Decimal('1745464481608'), 'id': Decimal('0'), 'start_time': Decimal('1745459822923')}, 
                        {'end_time': Decimal('1745553177696'), 'id': Decimal('0'), 'start_time': Decimal('1745551412683')}, {'id': Decimal('0'), 'end_time': Decimal('1745652442842'), 'start_time': Decimal('1745643854656')}, {'id': Decimal('0'), 'end_time': Decimal('1745683112381'), 'start_time': Decimal('1745678417996')}, {'id': Decimal('0'), 'end_time': Decimal('1745696148171'), 'start_time': Decimal('1745683112382')}, {'id': Decimal('0'), 'end_time': Decimal('1745725367958'), 'start_time': Decimal('1745705773082')}, 
                        {'end_time': Decimal('1745725369216'), 'id': Decimal('0'), 'start_time': Decimal('1745725367959')}, {'id': Decimal('0'), 'end_time': Decimal('1745791495051'), 'start_time': Decimal('1745768708957')}, {'id': Decimal('0'), 'end_time': Decimal('1745817780281'), 'start_time': Decimal('1745792625324')}, {'id': Decimal('0'), 'end_time': Decimal('1745844561774'), 'start_time': Decimal('1745842656892')}, {'id': Decimal('0'), 'end_time': Decimal('1745886992620'), 'start_time': Decimal('1745876147439')}, 
                        {'id': Decimal('0'), 'end_time': Decimal('1745904717254'), 'start_time': Decimal('1745891755686')}, {'id': Decimal('0'), 'end_time': Decimal('1745934417929'), 'start_time': Decimal('1745931047010')}]
    print(last_week_activity)
    populated_grid = populate_online_times(last_week_activity, grid)
    # Each hour row
    for time_label, row in zip(intervals, populated_grid):
        timetable_text += f"{time_label} " + "  ".join(row) + "\n"

    # Create embed with the timetable
    embed = [{
        "title": "📅 Chris's Weekly Hypixel Timetable",
        "description": f"```\n{timetable_text}```",
        "color": 0x008000
    }]
    return embed

def populate_online_times(activity, grid):
    day = {0: 1, 1: 2, 2: 3, 3:4, 4: 5, 5: 6, 6: 0}
    print("populate")
    # print(activity)
    for row in activity:
        print(row)
        lastLogin = int(row['start_time'] / 1000)
        loginDT = datetime.fromtimestamp(lastLogin, pytz.timezone("US/Eastern"))
        colLogin = day[loginDT.weekday()]
        # end_time exists if login<logout; does not exist if login>logout
        if 'end_time' in row:
            print("==============2===========")
            lastLogout = int(row['end_time'] / 1000)
            logoutDT = datetime.fromtimestamp(lastLogout, pytz.timezone("US/Eastern"))
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
        else:
            print("=============1==============")
            nowDT = datetime.now(pytz.timezone("US/Eastern")) 
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
    return grid


def get_last_week_items():
    # 1. Get today's date at midnight (UTC)
    now = datetime.now(pytz.timezone("US/Eastern"))
    eastern = pytz.timezone("US/Eastern")
    today_midnight = eastern.localize(datetime(now.year, now.month, now.day))
    # today_midnight = datetime(year=now.year, month=now.month, day=now.day)

    # 2. Subtract 6 full days
    cutoff_date = today_midnight - timedelta(days=6)
    # print(cutoff_date)
    cutoff_timestamp = int(cutoff_date.timestamp() * 1000)
    # print(cutoff_timestamp)
    # d1 = 1745031600007
    # if d1 >= cutoff_timestamp:
    #     print("yes")
    # else:
    #     print("no")

    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ['TABLE_NAME']
    table = dynamodb.Table(table_name)
    # items in last week
    response = table.query(
        KeyConditionExpression=Key('id').eq(0) & Key('start_time').gte(cutoff_timestamp),
        ScanIndexForward=True  # or False for newest first
    )
    items = response.get('Items', [])

    # print("last week---------")
    # for item in items:
    #     print(f"{item.get('id')}, start_time: {item.get('start_time')}, end_time: {item.get('end_time')}")
    #     start_time = int(item.get('start_time') / 1000) 
    #     if item.get('end_time') == None:
    #         end_time = None
    #         print(f"start_time: {datetime.fromtimestamp(start_time)}; end_time: {None}")
    #     else:
    #         end_time = int(item.get('end_time') / 1000) 
    #         print(f"start_time: {datetime.fromtimestamp(start_time)}; end_time: {datetime.fromtimestamp(end_time)}")
    return items

# Create 1hr intervals 
def generate_intervals():
    intervals = []
    for hour in range(24):
        intervals.append(f"{str(hour).zfill(2)}:00")
    return intervals

# Dummy schedule matrix: 24 rows × 7 columns (all ⬛️ for now)
def build_schedule_matrix():
    rows = []
    for _ in range(24):
        row = ["⬛️"] * 7
        rows.append(row)
    return rows

def verify_signature(signature, timestamp, body):
    try:
        verify_key = VerifyKey(bytes.fromhex(os.environ["DISCORD_PUBLIC_KEY"]))
        verify_key.verify(f"{timestamp}{body}".encode(), bytes.fromhex(signature))
        return True
    except BadSignatureError:
        return False


if __name__ == "__main__":
    print(__name__)
    os.environ['TABLE_NAME'] = "hypixel-activity-table"
    os.environ['DISCORD_PUBLIC_KEY'] = ""
    event = {}
    r = lambda_handler(event, None)
    print(r)