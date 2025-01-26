import requests

# Konfigurasi
channel_id = "1324498333758390353"  # ID channel tempat quest berada
tokens_file = "tokens.txt"  # File berisi token-token Discord (satu token per baris)

def verify_quests(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
    }
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    
    try:
        print(f"[INFO] Fetching messages from channel {channel_id}...")
        response = requests.get(url, headers=headers)
        print(f"[INFO] Response status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"[ERROR] Failed to fetch messages: {response.text}")
            return False

        messages = response.json()
        print(f"[INFO] Fetched {len(messages)} messages.")
        
        for message in messages:
            print(f"[INFO] Processing message ID: {message.get('id')}")
            
            components = message.get("components", [])
            for component in components:
                for button in component.get("components", []):
                    if button.get("label") == "Verify":  # Memastikan tombol 'Verify' ada
                        custom_id = button["custom_id"]
                        message_id = message["id"]
                        
                        # Membuat permintaan untuk memverifikasi
                        print(f"[INFO] Found Verify button with custom_id: {custom_id}")
                        verify_url = "https://discord.com/api/v9/interactions"
                        payload = {
                            "type": 3,
                            "channel_id": channel_id,
                            "message_id": message_id,
                            "custom_id": custom_id,
                        }
                        verify_response = requests.post(verify_url, headers=headers, json=payload)
                        if verify_response.status_code == 200:
                            print(f"[SUCCESS] Verified successfully for token: {token[:10]}...")
                        else:
                            print(f"[ERROR] Verification failed: {verify_response.status_code} - {verify_response.text}")
        return True

    except Exception as e:
        print(f"[EXCEPTION] An error occurred: {e}")
        return False


if __name__ == "__main__":
    try:
        with open(tokens_file, "r") as file:
            tokens = [line.strip() for line in file.readlines()]
        
        for token in tokens:
            print(f"[INFO] Processing token: {token[:10]}...")
            success = verify_quests(token)
            if not success:
                print(f"[WARNING] Verification failed for token: {token[:10]}...")
    
    except FileNotFoundError:
        print(f"[ERROR] Tokens file '{tokens_file}' not found. Please create the file and list your tokens.")
