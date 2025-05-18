import boto3
from boto3.dynamodb.conditions import Key
import os, json
import urllib3
# from datetime import datetime, timedeltas

# will get triggered every 5(or 20) mins
# obtain info from hypixel
# read db and see if info new
# if new update db, else nothing
def lambda_handler(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        table_name = os.environ['TABLE_NAME']
        table = dynamodb.Table(table_name)

        # get latest entry
        response = table.query(
            KeyConditionExpression=Key('id').eq(0),  # or whatever shared id you're using
            ScanIndexForward=False,  # descending order
            Limit=1
        )

        if response['Items']:
            latest_item = response['Items'][0]
        else:
            latest_item = None
            raise Exception("cant find latest item in table")

        # update latest_item
        if latest_item:
            lastLogin, lastLogout = get_skyblock_info()
            # lastLogin, lastLogout = -1, -1
            if lastLogin == -1:
                raise Exception("get_skyblock_info failed: api?")
            print("latest--")
            print(lastLogin)
            print(lastLogout)
            print(latest_item)

            # check if info new or old
            if latest_item["start_time"] != lastLogin:
                print("newinfo")
                if "end_time" not in latest_item:
                    print("new info, but previous logout was not recorded so must update previous entry")
                    print("logged out and logged back in within triggers")
                    r = table.put_item(
                    Item={
                        'id': 0,  # Same partition key for all items
                        'start_time': latest_item["start_time"],
                        'end_time': lastLogin - 1
                    })

                if lastLogin < lastLogout:
                    print("currently offline")
                    r = table.put_item(
                    Item={
                        'id': 0,  # Same partition key for all items
                        'start_time': lastLogin,
                        'end_time': lastLogout
                    })
                else:
                    print("currently online")
                    # previously online and currently offline
                    r = table.put_item(
                    Item={
                        'id': 0,  # Same partition key for all items
                        'start_time': lastLogin
                    })
            else:
                # not new login
                print("not new login")
                if lastLogin < lastLogout and "end_time" not in latest_item:
                    # old login, new logout
                    print("old login, new logout")
                    print("previously online and currently offlin")
                    # previously online and currently offline
                    # allegedly put_item replaces if id and start_time the same
                    r = table.put_item(
                    Item={
                        'id': 0,  # Same partition key for all items
                        'start_time': lastLogin,
                        'end_time': lastLogout
                    })

        return {
            'statusCode': 200,
            'body': json.dumps(f"Updated {os.environ['TABLE_NAME']} with lastLogin {lastLogin} lastLogout {lastLogout} from latest_item {latest_item}")
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps("Internal server error")
        }

def get_skyblock_info():
    Fl0of = "ccf434d6004444f0a275adf229269fc1"
    slimyslimy = "6ae06bc2a45a4c12afcd4fba49a4b404"

    # r = requests.get(f'https://api.hypixel.net/v2/player?key={os.environ["HYPIXEL_API_KEY"]}&uuid={Fl0of}')
    # d = r.json()
    # http = urllib3.PoolManager()
    # url = f'https://api.hypixel.net/v2/player?key={os.environ["HYPIXEL_API_KEY"]}&uuid={Fl0of}'

    # response = http.request('GET', url)
    # d = json.loads(response.data.decode('utf-8'))
    # if d["success"] == False:
    #     print(f"failure bc: {d['cause']}")
    #     return -1, -1
    # player = d["player"]
    # lastLogin = int(player["lastLogin"])
    # lastLogout = int(player["lastLogout"])
    '''
0
1745678417996
0
1745683112382
1745696148171
0
1745705773082
1745711082568
0
1745725367959
1745725369216
    '''
    lastLogin =  1745725367959
    lastLogout = 1745725369216
    # lastLogout = 1745681665000

    print(lastLogin)
    print(lastLogout)
    return lastLogin, lastLogout


if __name__ == "__main__":
    print(__name__)
    os.environ['TABLE_NAME'] = "hypixel-activity-table"
    os.environ['HYPIXEL_API_KEY'] = ""
    event = {}
    r = lambda_handler(event, None)
    print(r)