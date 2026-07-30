import os
import discord
from discord import app_commands
import google.generativeai as genai
from flask import Flask
from threading import Thread

# --- สร้างเว็บเซิร์ฟเวอร์จิ๋วไว้หลอก Render ว่ามีพอร์ตเปิดอยู่ ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ----------------------------------------------------

# กำหนดค่า API Key ของ Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# ตั้งค่าบอท Discord
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

ALLOWED_CHANNEL_NAME = "bot-chat"

@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user} (Slash Commands Synced)")

@tree.command(name="ask", description="ถาม AI หรือให้ช่วยเขียนสคริปต์ Roblox")
@app_commands.describe(prompt="ใส่คำสั่งหรือสิ่งที่คุณต้องการให้ AI ช่วย")
async def ask(interaction: discord.Interaction, prompt: str):
    if interaction.channel.name != ALLOWED_CHANNEL_NAME:
        await interaction.response.send_message(
            f"❌ คำสั่งนี้ใช้ได้เฉพาะในห้อง #{ALLOWED_CHANNEL_NAME} เท่านั้นครับ!", 
            ephemeral=True
        )
        return

    await interaction.response.defer(thinking=True)

    try:
        response = model.generate_content(prompt)
        reply_text = response.text

        if len(reply_text) > 1900:
            chunks = [reply_text[i:i+1900] for i in range(0, len(reply_text), 1900)]
            await interaction.followup.send(chunks[0])
            for chunk in chunks[1:]:
                await interaction.followup.send(chunk)
        else:
            await interaction.followup.send(reply_text)

    except Exception as e:
        await interaction.followup.send("เกิดข้อผิดพลาดในการประมวลผลครับ ลองใหม่อีกครั้งนะ")

# เปิดเว็บเซิร์ฟเวอร์จำลองก่อนรันบอท
keep_alive()
client.run(os.environ["DISCORD_TOKEN"])
