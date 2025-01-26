import discord
import asyncio
import re
import os
from datetime import datetime

# Config
CHANNEL_ID = 1324498333758390353  # Ganti dengan ID channel target

def load_tokens():
    """Membaca token dari file token.txt"""
    tokens = []
    try:
        with open('token.txt', 'r') as f:
            for line in f:
                token = line.strip()
                if token and not token.startswith('#'):
                    tokens.append(token)
        return tokens
    except FileNotFoundError:
        print("[!] File token.txt tidak ditemukan!")
        exit(1)

class QuestClaimer(discord.Client):
    def __init__(self, token, *args, **kwargs):
        # Set intents dan bot=False
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            intents=intents, 
            *args, 
            **kwargs,
            bot=False  # Parameter bot=False disini
        )
        self.token = token

    async def on_ready(self):
        print(f"[+] {self.user} siap!")
        await self.claim_quests()

    async def claim_quests(self):
        channel = self.get_channel(CHANNEL_ID)
        
        while True:
            try:
                async for message in channel.history(limit=50):
                    if "Quest claimed!" in message.content and message.author.id != self.user.id:
                        await self.process_quest(message)
                
                await asyncio.sleep(2)

            except Exception as e:
                print(f"[-] Error: {str(e)}")
                await asyncio.sleep(10)

    async def process_quest(self, message):
        user_id = message.author.id
        
        if user_id in self.claimed_users:
            return

        if re.search(r"You have been awarded \d+ 🟢", message.content):
            await message.add_reaction("✅")
            await asyncio.sleep(2)
            
            self.claimed_users.add(user_id)
            
            await message.reply(
                f"Verified! {message.author.mention}",
                delete_after=5
            )
            print(f"[+] Berhasil verifikasi {message.author}")

async def main():
    tokens = load_tokens()
    
    if not tokens:
        print("[!] Tidak ada token yang valid di token.txt!")
        return

    for token in tokens:
        client = QuestClaimer(token)
        asyncio.create_task(client.start(client.token))  # Parameter benar

    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
