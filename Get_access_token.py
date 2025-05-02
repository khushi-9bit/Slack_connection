import requests

client_id = "6141813715298.8819754192566"
client_secret = "d182a0f44c0c962ca3bef4f037cf0ba1"
code = "8861252289408.8831185880582.5cb0eea79e77924e0abab1e6688a615f89078c2abc9c3e9930b3c875860faf66"  # paste from the URL
redirect_uri = "https://localhost:5000/callback"  # must match exactly

response = requests.post("https://slack.com/api/oauth.v2.access", data={
    'client_id': client_id,
    'client_secret': client_secret,
    'code': code,
    'redirect_uri': redirect_uri
})

data = response.json()

if data.get("ok"):
    print("✅ Access Token:", data["access_token"])
    print("🔑 Bot Token:", data.get("access_token"))
    print("👥 Team Info:", data.get("team"))
else:
    print("❌ Error:", data.get("error"))
