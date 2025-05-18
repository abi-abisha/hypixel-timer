from decimal import Decimal
from datetime import datetime, timedelta
# from zoneinfo import ZoneInfo, available_timezones  # Available in Python 3.9+
import pytz


x = "hey"

print("wassup")
print(x)


# # Unix timestamp in milliseconds
# timestamp_ms = 1745904717254

# # Convert milliseconds to seconds
# timestamp_s = timestamp_ms / 1000

# # Convert to UTC datetime
# dt_utc = datetime.fromtimestamp(timestamp_s, tz=timezone.utc)

# # Convert to Eastern Time
# dt_est = dt_utc.astimezone(ZoneInfo("US/Eastern"))

# print("Eastern Time:", dt_est.strftime('%Y-%m-%d %H:%M:%S %Z%z'))

# Unix timestamp in milliseconds
timestamp_ms = 1745904717254

# Convert milliseconds to seconds
timestamp_s = timestamp_ms / 1000

# Create a datetime object in UTC
# dt_utc = datetime.fromtimestamp(timestamp_s).replace(tzinfo=pytz.utc)

# Convert to Eastern Time (EST/EDT)
# eastern = pytz.timezone('US/Eastern')
# dt_est = dt_utc.astimezone(eastern)
dt_est = datetime.fromtimestamp(timestamp_s, pytz.timezone("US/Eastern"))
# n = datetime.now(pytz.timezone("US/Eastern"))
now = datetime.fromtimestamp(1745946000, pytz.timezone("US/Eastern"))
eastern = pytz.timezone("US/Eastern")
today_midnight = eastern.localize(datetime(now.year, now.month, now.day))
# 2. Subtract 6 full days
cutoff_date = today_midnight - timedelta(days=6)
# print(cutoff_date)
cutoff_timestamp = int(cutoff_date.timestamp() * 1000)
e = {'end_time': Decimal('1745381576115'), 'id': Decimal('0'), 'start_time': Decimal('1745373628663')}
# problem with this time showing up in current week even thought it shouldnt
print("now")
print(now)
print(today_midnight)
print(cutoff_date)
print(cutoff_timestamp)
print("Eastern Time:", dt_est.strftime('%Y-%m-%d %H:%M:%S %Z%z'))
y = datetime.fromtimestamp(int(e['start_time'] / 1000), pytz.timezone("US/Eastern"))
print(y)
if __name__ == "__main__":
    print("hi")
    x = 3
    z = 1745353620000
    z = int(Decimal('1745725367959'))
    # print(available_timezones())
    # print(datetime.fromtimestamp(z / 1000))
    # print(dt_utc)
    print(dt_est)
    # print(n)
    now = datetime.now(pytz.timezone("US/Eastern"))
    today_midnight = datetime(year=now.year, month=now.month, day=now.day)

    # 2. Subtract 6 full days
    cutoff_date = today_midnight - timedelta(days=6)
    # print(cutoff_date)
    cutoff_timestamp = int(cutoff_date.timestamp() * 1000)
    print(today_midnight)
    print(cutoff_date)
    print(cutoff_timestamp)
    # print(n.strftime('%m-%d'))
    # if dt_est < n:
    #     print("yes")
    # else:
    #     print("no")
    print(x)