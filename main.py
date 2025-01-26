import httpx
import asyncio
import logging

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Membaca token dari file token.txt
def load_tokens():
    with open("token.txt", "r") as file:
        return [line.strip() for line in file]

# Fungsi untuk mendapatkan pesan dari channel
async def fetch_messages(token, channel_id, limit=100):
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages?limit={limit}"
    headers = {"Authorization": token}  # User token tidak perlu prefix "Bot"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"Gagal mengambil pesan: {response.status_code} - {response.text}")
            return []

# Fungsi untuk mengklik tombol "Verify"
async def click_button(token, message, button):
    url = f"https://discord.com/api/v10/interactions"
    headers = {"Authorization": token, "Content-Type": "application/json"}
    
    # Payload untuk interaksi tombol
    payload = {
        "type": 3,
        "message_id": message["id"],
        "channel_id": message["channel_id"],
        "application_id": message["author"]["id"],
        "data": {
            "custom_id": button["custom_id"],
            "component_type": button["type"]
        }
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            logging.info(f"Berhasil klik tombol untuk pesan {message['id']}")
        else:
            logging.error(f"Gagal klik tombol: {response.status_code} - {response.text}")

# Fungsi utama untuk memverifikasi semua quest
async def verify_quests(token, channel_id):
    messages = await fetch_messages(token, channel_id)
    for message in messages:
        if "components" in message:  # Pastikan pesan memiliki tombol
            for row in message["components"]:
                for button in row["components"]:
                    if button["label"] == "Verify":  # Cari tombol dengan label "Verify"
                        await click_button(token, message, button)
                        await asyncio.sleep(2)  # Jeda 2 detik untuk menghindari rate-limiting

# Fungsi untuk menjalankan banyak token secara paralel
async def main(channel_id):
    tokens = load_tokens()
    tasks = [verify_quests(token, channel_id) for token in tokens]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    # Ganti YOUR_CHANNEL_ID_HERE dengan ID channel Discord tempat quest berada
    CHANNEL_ID = "YOUR_CHANNEL_ID_HERE"

    asyncio.run(main(CHANNEL_ID))
