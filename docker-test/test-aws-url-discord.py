import json
import os
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

DISCORD_PUBLIC_KEY = os.environ["DISCORD_PUBLIC_KEY"]

DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def lambda_handler(event, context):
    signature = event['headers'].get('x-signature-ed25519')
    timestamp = event['headers'].get('x-signature-timestamp')
    body = event['body']

    if not verify_signature(signature, timestamp, body):
        print("invalid request signature")
        return {
            "statusCode": 401,
            "body": "invalid request signature"
        }

    data = json.loads(body)

    if data["type"] == 1:
        # PING from Discord
        print("ping")
        return {
            "statusCode": 200,
            "body": json.dumps({"type": 1})
        }

    if data["type"] == 2:
        # Slash command
        print("slash command")
        if data["data"]["name"] == "timetable":
            print("timetable")
            embed = [{
                        "title": "📅 Weekly Timetable",
                        "description": f"```\n{DAYS_OF_WEEK}```",
                        "color": 0x008000
                    }]
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "type": 4,  # Channel message with source
                    # "data": {
                    #     "content": "🗓️ Here’s the timetable:\n" + "\n".join(DAYS_OF_WEEK)
                    # }
                    "data": {
                        "embeds": embed
                    }
                })
            }

    print("unhandled")
    return {    
        "statusCode": 400,
        "body": "unhandled"
    }

def verify_signature(signature, timestamp, body):
    try:
        verify_key = VerifyKey(bytes.fromhex(DISCORD_PUBLIC_KEY))
        verify_key.verify(f"{timestamp}{body}".encode(), bytes.fromhex(signature))
        return True
    except BadSignatureError:
        return False
