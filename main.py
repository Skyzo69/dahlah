import requests

# Konfigurasi
channel_id = "1324498333758390353"  # ID channel yang ingin diverifikasi
tokens_file = "tokens.txt"  # File yang berisi token-token Discord (1 token per baris)

def verify_quests(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
    }
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    
    try:
        # Mengambil semua pesan di channel
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching messages: {response.status_code} - {response.text}")
            return False

        messages = response.json()
        for message in messages:
            if "Verify" in message.get("content", ""):  # Memeriksa tombol Verify
                message_id = message["id"]
                components = message.get("components", [])
                
                for component in components:
                    for button in component.get("components", []):
                        if button.get("label") == "Verify":
                            custom_id = button["custom_id"]
                            
                            # Mengirim permintaan untuk memverifikasi
                            verify_url = f"https://discord.com/api/v9/interactions"
                            payload = {
                                "type": 3,
                                "channel_id": channel_id,
                                "message_id": message_id,
                                "custom_id": custom_id,
                            }
                            verify_response = requests.post(verify_url, headers=headers, json=payload)
                            if verify_response.status_code == 200:
                                print(f"Verified successfully for token: {token[:10]}...")
                            else:
                                print(f"Failed to verify: {verify_response.status_code} - {verify_response.text}")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


if __name__ == "__main__":
    try:
        with open(tokens_file, "r") as file:
            tokens = [line.strip() for line in file.readlines()]
        
        for token in tokens:
            print(f"Processing token: {token[:10]}...")
            verify_quests(token)
    except FileNotFoundError:
        print(f"Tokens file '{tokens_file}' not found. Please create the file and list your tokens.")
