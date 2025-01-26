import requests
import time

# Baca token dari tokens.txt
def load_tokens(file_path):
    try:
        with open(file_path, "r") as file:
            tokens = [line.strip() for line in file.readlines() if line.strip()]
        return tokens
    except FileNotFoundError:
        print("[ERROR] File tokens.txt tidak ditemukan!")
        return []

# Kirim permintaan POST untuk klik tombol 'Verify'
def click_verify_button(token, channel_id, message_id, custom_id):
    url = f"https://discord.com/api/v9/interactions"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    payload = {
        "type": 3,
        "message_id": message_id,
        "channel_id": channel_id,
        "application_id": "your_application_id",  # Ganti sesuai kebutuhan
        "data": {
            "component_type": 2,
            "custom_id": custom_id
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"[INFO] Verification success for message ID: {message_id}")
    else:
        print(f"[ERROR] Verification failed: {response.status_code} - {response.text}")

# Ambil pesan dari channel
def fetch_messages(token, channel_id):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    headers = {"Authorization": token}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"[ERROR] Failed to fetch messages: {response.status_code} - {response.text}")
        return []

# Proses klaim otomatis
def main():
    tokens = load_tokens("tokens.txt")
    channel_id = "1324498333758390353"  # Channel ID

    if not tokens:
        print("[ERROR] Tidak ada token yang ditemukan!")
        return

    for token in tokens:
        print(f"[INFO] Menggunakan token: {token[:10]}...")
        messages = fetch_messages(token, channel_id)

        if not messages:
            print("[INFO] Tidak ada pesan ditemukan.")
            continue

        for message in messages:
            message_id = message["id"]
            components = message.get("components", [])
            
            for component in components:
                for action in component.get("components", []):
                    if action["type"] == 2 and action["custom_id"].startswith("claimDrop_"):
                        print(f"[INFO] Found Verify button in message ID: {message_id}")
                        click_verify_button(token, channel_id, message_id, action["custom_id"])
                        time.sleep(2)  # Delay untuk menghindari rate limit

if __name__ == "__main__":
    main()
