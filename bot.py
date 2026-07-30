import os
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

# 2. ตั้งค่า Gemini AI
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
generation_config = {
    "temperature": 0.7,
    "max_output_tokens": 2048,
}
model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)

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

@tree.command(name="ask", description="ถาม AI หรือให้ช่วยเขียนสคริปต์ Roblox")
@app_commands.describe(prompt="ใส่คำสั่งหรือสิ่งที่คุณต้องการให้ AI ช่วย")
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

        # ตัดแบ่งส่งถ้าข้อความยาวเกินไป
        if len(reply_text) > 1900:
            chunks = [reply_text[i:i+1900] for i in range(0, len(reply_text), 1900)]
            await interaction.followup.send(chunks[0])
            for chunk in chunks[1:]:
                await interaction.followup.send(chunk)
        else:
            await interaction.followup.send(reply_text)

    except Exception as e:
        print(f"Error detail: {e}")
        # ส่งรายละเอียด Error ออกมาโชว์ในดิสคอร์ดเพื่อเช็คอาการ
        await interaction.followup.send(f"⚠️ เกิดข้อผิดพลาด: {str(e)}")

# รันระบบ
keep_alive()
client.run(os.environ["DISCORD_TOKEN"])
