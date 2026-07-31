import os
import io
import discord
from discord import app_commands
import google.generativeai as genai
from flask import Flask
from threading import Thread

# 1. ระบบเว็บเซิร์ฟเวอร์จิ๋วสำหรับ Render
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. ตั้งค่า Gemini AI (ใช้ gemini-3.5-flash ตามที่ต้องการ)
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
generation_config = {
    "temperature": 0.7,
    "max_output_tokens": 4096,
}
model = genai.GenerativeModel(model_name="gemini-3.5-flash", generation_config=generation_config)

# 3. ตั้งค่า Discord Bot
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# กำหนดชื่อห้องที่อนุญาตให้ใช้คำสั่ง
ALLOWED_CHANNEL_NAME = "bot-chat"

@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user} (Ready & Synced)")

@tree.command(name="ask", description="ถาม AI หรือให้ช่วยเขียนสคริปต์ Roblox และส่งมาเป็นไฟล์")
@app_commands.describe(prompt="ใส่คำสั่งหรือสิ่งที่คุณต้องการให้ AI ช่วยเขียนสคริปต์")
async def ask(interaction: discord.Interaction, prompt: str):
    # เช็คชื่อห้อง
    if interaction.channel.name != ALLOWED_CHANNEL_NAME:
        await interaction.response.send_message(
            f"❌ คำสั่งนี้ใช้ได้เฉพาะในห้อง #{ALLOWED_CHANNEL_NAME} เท่านั้นครับ!", 
            ephemeral=True
        )
        return

    # ตอบกลับสถานะกำลังคิด
    await interaction.response.defer(thinking=True)

    try:
        # สั่งให้ Gemini สร้างข้อความตอบกลับ
        response = model.generate_content(prompt)
        reply_text = response.text

        # แปลงข้อความคำตอบให้กลายเป็นไฟล์ .txt ในหน่วยความจำ
        file_bytes = io.BytesIO(reply_text.encode('utf-8'))
        discord_file = discord.File(file_bytes, filename="roblox_script.txt")

        # ส่งไฟล์กลับไปในห้องแชท
        await interaction.followup.send(
            content="📄 นี่คือสคริปต์และคำตอบที่คุณขอครับ สามารถดาวน์โหลดไปเปิดดูได้เลย!", 
            file=discord_file
        )

    except Exception as e:
        print(f"Error detail: {e}")
        await interaction.followup.send(f"⚠️ เกิดข้อผิดพลาด: {str(e)}")

# รันระบบ
keep_alive()
client.run(os.environ["DISCORD_TOKEN"])
