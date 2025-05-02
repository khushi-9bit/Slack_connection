from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import time
from datetime import datetime

client = WebClient(token=slack_token)

# ---------------------- SEND MESSAGE TO A CHANNEL ----------------------
def send_message_to_channel(channel_name, message):
    try:
        # Get the channel ID
        channels = client.conversations_list(types="public_channel")["channels"]
        channel_id = next((c["id"] for c in channels if c["name"] == channel_name), None)
        
        if not channel_id:
            print(f"❌ Channel '{channel_name}' not found.")
            return

        # Send the message
        client.chat_postMessage(channel=channel_id, text=message)
        print(f"✅ Message sent to #{channel_name}")

    except SlackApiError as e:
        print("❌ Channel Error:", e.response['error'])

# ---------------------- READ MESSAGES FROM A CHANNEL ----------------------
def read_messages_from_channel(channel_name):
    try:
        channels = client.conversations_list(types="public_channel")["channels"]
        channel_id = next((c["id"] for c in channels if c["name"] == channel_name), None)
        
        if not channel_id:
            print(f"❌ Channel '{channel_name}' not found.")
            return

        # Read messages
        history = client.conversations_history(channel=channel_id)
        for msg in history["messages"]:
            print("📝", msg.get("text"))

    except SlackApiError as e:
        print("❌ Read Channel Error:", e.response['error'])

def get_user_id_by_name(username):
    try:
        response = client.users_list()
        for user in response["members"]:
            if user.get("name") == username or user.get("real_name") == username:
                return user["id"]
        print(f"❌ User '{username}' not found.")
        return None
    except SlackApiError as e:
        print("❌ Error fetching users:", e.response["error"])
        return None
    
def send_dm_by_username(username, message):
    user_id = get_user_id_by_name(username)
    if user_id:
        send_dm_to_user(user_id, message)

def read_dm_by_username(username):
    user_id = get_user_id_by_name(username)
    if user_id:
        read_dm_from_user(user_id)

# ---------------------- SEND DM TO USER ----------------------
def send_dm_to_user(user_id, message):
    try:
        dm_channel = client.conversations_open(users=[user_id])["channel"]["id"]
        client.chat_postMessage(channel=dm_channel, text=message)
        print(f"✅ DM sent to {user_id}")
    except SlackApiError as e:
        print("❌ DM Error:", e.response['error'])

def read_dm_from_user(user_id):
    try:
        dm_channel = client.conversations_open(users=[user_id])["channel"]["id"]
        history = client.conversations_history(channel=dm_channel)

        print(f"📬 Messages from DM with user ID {user_id}:")
        for msg in history["messages"]:
            print("💬", msg.get("text"))
    except SlackApiError as e:
        print("❌ DM Read Error:", e.response['error'])

def get_channel_id_by_name(channel_name):
    try:
        response = client.conversations_list()
        for channel in response["channels"]:
            if channel["name"] == channel_name:
                return channel["id"]
        return None
    except SlackApiError as e:
        print("❌ Error fetching channel list:", e.response["error"])
        return None

def fetch_logs_between_dates(channel_id, start_time_str, end_time_str):
    #channel_id = get_channel_id_by_name(channel_name)
    if not channel_id:
        print("❌ Channel not found")
        return

    # Convert datetime strings to Unix timestamps
    start_ts = time.mktime(datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S").timetuple())
    end_ts = time.mktime(datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S").timetuple())

    try:
        response = client.conversations_history(
            channel=channel_id,
            oldest=start_ts,
            latest=end_ts,
            inclusive=True,
            limit=1000
        )

        for msg in response["messages"]:
            print(f"{msg.get('user', 'bot')} @ {datetime.fromtimestamp(float(msg['ts']))}: {msg['text']}")

    except SlackApiError as e:
        print("❌ Error fetching logs:", e.response["error"])

#idid = "C08LMQXU6KV"
# ---------------------- MAIN ----------------------
if __name__ == "__main__":
    #send_message_to_channel("general", "🚀 Hello from bot in #general!")
    #read_messages_from_channel("general")
    #send_dm_to_user("U0645M37UM9", "👋 Hello Rajeev from your bot!")
    #read_dm_from_user("U0645M37UM9")
    #send_dm_by_username("Rajeev Jamaiyar", "Hey! ")
    #read_dm_by_username("Rajeev Jamaiyar")
      # Replace this with the correct ID from `list_channels()`
    fetch_logs_between_dates(
    channel_id= "C08LMQXU6KV",
    start_time_str="2025-04-22 00:00:00",
    end_time_str="2025-04-30 23:59:59"
)
