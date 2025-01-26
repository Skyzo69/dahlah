import asyncio
import logging
import discord
from discord.ext import commands

# Konfigurasi Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Membaca token dari file token.txt
def load_tokens():
    with open("token.txt", "r") as file:
        return [line.strip() for line in file]

# Fungsi untuk memverifikasi quest di satu channel
async def verify_quests(bot, channel_id):
    channel = bot.get_channel(channel_id)
    if not channel:
        logging.error(f"Channel dengan ID {channel_id} tidak ditemukan.")
        return

    try:
        # Iterasi semua pesan di channel
        async for message in channel.history(limit=100):
            # Cek apakah pesan memiliki komponen tombol
            if message.author.bot and message.components:
                for row in message.components:
                    for component in row.children:
                        if component.label == "Verify":  # Cari tombol "Verify"
                            try:
                                await message.interaction_response.send_message()  # Klik tombol
                                logging.info(f"{bot.user} berhasil memverifikasi quest: {message.id}")
                                await asyncio.sleep(2)  # Jeda 2 detik
                            except Exception as e:
                                logging.warning(f"Gagal memverifikasi quest {message.id}: {e}")
    except Exception as e:
        logging.error(f"Kesalahan saat membaca history channel: {e}")

# Main function untuk menjalankan beberapa bot/token
async def run_bots(channel_id):
    tokens = load_tokens()
    bots = []

    for token in tokens:
        bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        bots.append(bot)

        @bot.event
        async def on_ready():
            logging.info(f"{bot.user} berhasil login.")
            await verify_quests(bot, channel_id)
            await bot.close()  # Tutup bot setelah tugas selesai

    # Jalankan semua bot secara paralel
    await asyncio.gather(*[bot.start(token) for token in tokens])

if __name__ == "__main__":
    # Ganti YOUR_CHANNEL_ID_HERE dengan ID channel Discord Anda
    CHANNEL_ID = 1324498333758390353

    asyncio.run(run_bots(CHANNEL_ID))
